import socket
import time
from threading import Thread, Lock

routes = {
  "1": {"name": "Belem-Curitiba", "segments": {
    "1": {"name": "Belem to Sao Luis", "seats": [1, 2, 3]},
    "2": {"name": "Sao Luis to Fortaleza", "seats": [1, 2, 3]},
    "3": {"name": "Fortaleza to Curitiba", "seats": [1, 2, 3]}
  }},
  "2": {"name": "São Paulo-Rio de Janeiro", "segments": {
    "1": {"name": "São Paulo to Campinas", "seats": [1, 2, 3, 4]},
    "2": {"name": "Campinas to São José dos Campos", "seats": [1, 2, 3, 4]},
    "3": {"name": "São José dos Campos to Rio de Janeiro", "seats": [1, 2, 3, 4]}
  }},
  "3": {"name": "Porto Alegre-Salvador", "segments": {
    "1": {"name": "Porto Alegre to Curitiba", "seats": [1, 2]},
    "2": {"name": "Curitiba to São Paulo", "seats": [1, 2]},
    "3": {"name": "São Paulo to Salvador", "seats": [1, 2]}
  }},
}

client_reserves = {}
temporary_reserves = {}
lock = Lock()

def handle_client(connection, address):
  print(f"Established Connection with ({address})")

  id_client = connection.recv(4096).decode().strip()
  print(f"Client ({id_client}) connected from {address}")

  with lock:
    if id_client not in client_reserves:
      client_reserves[id_client] = []

  while True:
    try:
      menu = "\n1. Make a Reserve\n2. Confirm Reserves\n3. View my Reserves\n4. Exit"
      print(f"Sending menu to client {id_client}: {menu}")
      connection.sendall(menu.encode())

      option = connection.recv(4096).decode().strip()
      print(f"({id_client}) selected option {option}")

      # Make a Reserve:
      if option == "1":
        available_routes = "\n".join([f"{id}: {route['name']}" for id, route in routes.items()])
        connection.sendall(f"\nAvailable Routes:\n{available_routes}\n".encode())

        id_route = connection.recv(4096).decode().strip()
        if id_route in routes:
          segments = "\n".join([f"{id}: {segment['name']} - Seats: {', '.join(map(str, segment['seats']))}" for id, segment in routes[id_route]["segments"].items()])
          connection.sendall(f"\nAvailable Segments for Route {routes[id_route]['name']}:\n{segments}\n".encode())

          id_segment = connection.recv(4096).decode().strip()
          if id_segment in routes[id_route]["segments"]:
            connection.sendall(f"\nYou Have Selected Segment {routes[id_route]['segments'][id_segment]['name']}.".encode())
            seat = connection.recv(4096).decode().strip()

            with lock:
              if int(seat) in routes[id_route]["segments"][id_segment]["seats"]:
                routes[id_route]["segments"][id_segment]["seats"].remove(int(seat))
                temporary_reserves[id_client] = {"route": routes[id_route]["name"], "segment": routes[id_route]["segments"][id_segment]["name"], "seat": seat, "id_route": id_route, "id_segment": id_segment}
                connection.sendall(f"\nTemporarily Reserved Seat: {seat} in segment {routes[id_route]['segments'][id_segment]['name']} of route {routes[id_route]['name']}. \nConfirm within 30 seconds.\n".encode())
                Thread(target=cancel_temporary_reserve, args=(id_client, id_route, id_segment, seat)).start()
              else:
                connection.sendall("\n** SEAT UNAVAILABLE **\n".encode())
          else:
            connection.sendall("\n** INVALID SEGMENT **\n".encode())
        else:
          connection.sendall("\n** INVALID ROUTE **\n".encode())

      # Confirm a Reserve:
      elif option == "2":
        with lock:
          if id_client in temporary_reserves:
            reserve = temporary_reserves.pop(id_client)
            client_reserves[id_client].append(reserve)
            connection.sendall(f"\nConfirmed Reserve for the Route {reserve['route']} in Segment {reserve['segment']} and Seat {reserve['seat']}.\n".encode())
            print(f"({id_client}) confirmed a Reserve in the Seat {reserve['seat']} in Segment {reserve['segment']} of the Route {reserve['route']}.")
          else:
            connection.sendall("\nYou don't Have a Temporary Reserve to Confirm.\n".encode())

      # View Reserves:
      elif option == "3":
        if client_reserves[id_client]:
          my_reserves = "\n".join([f"Route: {reserve['route']}, Segment: {reserve['segment']}, Seat: {reserve['seat']}" for reserve in client_reserves[id_client]])
          connection.sendall(f"\nYour Confirmed Reserves:\n{my_reserves}\n".encode())
        else:
          connection.sendall("\nYou don't Have a Confirmed Reserve.\n".encode())
        print(f"({id_client}) Viewed Your Reserves.")

      # Disconnect of Server:
      elif option == "4":
        connection.sendall("\nDisconnecting...\n".encode())
        print(f"({id_client}) Has Been Disconnected.")
        break

    except Exception as error:
      print(f"Client Error: {error}")
      break

  connection.close()

def cancel_temporary_reserve(id_client, id_route, id_segment, seat):
  time.sleep(30)
  with lock:
    if id_client in temporary_reserves:
      temporary_reserves.pop(id_client)
      routes[id_route]["segments"][id_segment]["seats"].append(int(seat))
      print(f"Temporary Reserve from ({id_client}) expired. Seat {seat} in segment {routes[id_route]['segments'][id_segment]['name']} available.")

def start_server():
  host = 'localhost'
  port = 12345

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen()

  print("\nServer Started...\n")

  while True:
    connection, address = server_socket.accept()
    Thread(target=handle_client, args=(connection, address)).start()

if __name__ == "__main__":
  start_server()
