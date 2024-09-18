import socket

def request_reserve(server_host, server_port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect((server_host, server_port))

    id_client = input("Enter Your Client ID: ")
    server.sendall(id_client.encode())

    while True:
      try:
        menu = server.recv(4096).decode()
        print(menu)

        option = input("\nSelect an Option: ")
        server.sendall(option.encode())

        answer = server.recv(4096).decode()
        print(answer)

        if option == "1":
          route = input("\nEnter a Number of the Route: ")
          server.sendall(route.encode())

          segment_message = server.recv(4096).decode()
          print(segment_message)
          segment = input("\nEnter a Number of the Segment: ")
          server.sendall(segment.encode())

          seat_message = server.recv(4096).decode()
          print(seat_message)
          seat = input("\nEnter a Number of the Seat: ")
          server.sendall(seat.encode())

          confirmation = server.recv(4096).decode()
          print(confirmation)
        
        elif option == "4":
          break

      except Exception as e:
        print(f"An error occurred: {e}")
        break

if __name__ == "__main__":
  server_host = "localhost"
  server_port = 12345
  request_reserve(server_host, server_port)
