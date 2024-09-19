import socket
import time
from threading import Thread, Lock

# Define as rotas disponíveis com seus respectivos segmentos e assentos:
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

# Dicionário para armazenar reservas confirmadas dos clientes:
client_reserves = {}

# Dicionário para armazenar reservas temporárias, antes da confirmação:
temporary_reserves = {}

# Lock para garantir segurança em acessos concorrentes aos dados compartilhados:
lock = Lock()

# Função para lidar com as conexões dos clientes:
def handle_client(connection, address):
  print(f"Established Connection with ({address})")

  # Recebe o ID do cliente e o registra:
  id_client = connection.recv(4096).decode().strip()
  print(f"Client ({id_client}) connected from {address}")

  # Garantir que o cliente tenha um local reservado na lista de reservas:
  with lock:
    if id_client not in client_reserves:
      client_reserves[id_client] = []

  while True:
    try:
      # Envia o menu de opções para o cliente:
      menu = "\n1. Make a Reserve\n2. Confirm Reserves\n3. View my Reserves\n4. Exit"
      print(f"Sending menu to client {id_client}: {menu}")
      connection.sendall(menu.encode())

      # Recebe a opção escolhida pelo cliente:
      option = connection.recv(4096).decode().strip()
      print(f"({id_client}) selected option {option}")

      # Opção 1 - Fazer uma reserva:
      if option == "1":
        # Envia ao cliente as rotas disponíveis:
        available_routes = "\n".join([f"{id}: {route['name']}" for id, route in routes.items()])
        connection.sendall(f"\nAvailable Routes:\n{available_routes}\n".encode())

        # Recebe a rota escolhida:
        id_route = connection.recv(4096).decode().strip()
        if id_route in routes:
          # Envia ao cliente os segmentos e assentos disponíveis para a rota escolhida:
          segments = "\n".join([f"{id}: {segment['name']} - Seats: {', '.join(map(str, segment['seats']))}" for id, segment in routes[id_route]["segments"].items()])
          connection.sendall(f"\nAvailable Segments for Route {routes[id_route]['name']}:\n{segments}\n".encode())

          # Recebe o segmento escolhido:
          id_segment = connection.recv(4096).decode().strip()
          if id_segment in routes[id_route]["segments"]:
            connection.sendall(f"\nYou Have Selected Segment {routes[id_route]['segments'][id_segment]['name']}.".encode())

            # Recebe o número do assento escolhido:
            seat = connection.recv(4096).decode().strip()

            # Verifica se o assento está disponível e faz uma reserva temporária:
            with lock:
              if int(seat) in routes[id_route]["segments"][id_segment]["seats"]:
                routes[id_route]["segments"][id_segment]["seats"].remove(int(seat))
                temporary_reserves[id_client] = {"route": routes[id_route]["name"], "segment": routes[id_route]["segments"][id_segment]["name"], "seat": seat, "id_route": id_route, "id_segment": id_segment}
                connection.sendall(f"\nTemporarily Reserved Seat: {seat} in Segment {routes[id_route]['segments'][id_segment]['name']} of Route {routes[id_route]['name']}. \nConfirm within 30 seconds.\n".encode())
                
                # Inicia a thread para cancelar a reserva temporária após 30 segundos:
                Thread(target=cancel_temporary_reserve, args=(id_client, id_route, id_segment, seat)).start()
              else:
                connection.sendall("\n** SEAT UNAVAILABLE **\n".encode())
          else:
              connection.sendall("\n** INVALID SEGMENT **\n".encode())
        else:
          connection.sendall("\n** INVALID ROUTE **\n".encode())

      # Opção 2 - Confirmar a reserva temporária:
      elif option == "2":
        with lock:
          if id_client in temporary_reserves:
            reserve = temporary_reserves.pop(id_client)
            client_reserves[id_client].append(reserve)
            connection.sendall(f"\nConfirmed Reserve for the Route {reserve['route']} in Segment {reserve['segment']} and Seat {reserve['seat']}.\n".encode())
            print(f"({id_client}) confirmed a Reserve in the Seat {reserve['seat']} in Segment {reserve['segment']} of the Route {reserve['route']}.")
          else:
            connection.sendall("\nYou don't Have a Temporary Reserve to Confirm.\n".encode())

      # Opção 3 - Visualizar reservas confirmadas:
      elif option == "3":
        if client_reserves[id_client]:
          my_reserves = "\n".join([f"- Route: {reserve['route']}, Segment: {reserve['segment']}, Seat: {reserve['seat']}" for reserve in client_reserves[id_client]])
          connection.sendall(f"\nYour Confirmed Reserves:\n{my_reserves}\n".encode())
        else:
          connection.sendall("\nYou don't Have a Confirmed Reserve.\n".encode())
        print(f"({id_client}) Viewed Your Reserves.")

      # Opção 4 - Desconectar o cliente:
      elif option == "4":
        connection.sendall("\nDisconnecting...\n".encode())
        print(f"({id_client}) Has Been Disconnected.")
        break

    except Exception as error:
      print(f"Client Error: {error}")
      break

  connection.close()

# Função que cancela a reserva temporária após 30 segundos se não for confirmada:
def cancel_temporary_reserve(id_client, id_route, id_segment, seat):
  time.sleep(30)
  with lock:
    if id_client in temporary_reserves:
      temporary_reserves.pop(id_client)
      routes[id_route]["segments"][id_segment]["seats"].append(int(seat))
      print(f"Temporary Reserve from ({id_client}) expired. Seat {seat} in segment {routes[id_route]['segments'][id_segment]['name']} available.")

# Função que inicializa o servidor e aceita conexões de clientes:
def start_server():
  host = 'localhost'
  port = 12345

  # Configuração do socket do servidor:
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen()

  print("\nServer Started...\n")

  # Aceita conexões de clientes e cria uma nova thread para cada cliente:
  while True:
    connection, address = server_socket.accept()
    Thread(target=handle_client, args=(connection, address)).start()

# Início da execução do servidor:
if __name__ == "__main__":
  start_server()
