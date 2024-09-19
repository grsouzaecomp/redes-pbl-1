import socket

# Função para solicitar uma reserva ao servidor
def request_reserve(server_host, server_port):
  # Cria um socket TCP/IP e conecta ao servidor
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.connect((server_host, server_port))

    # Solicita o ID do cliente e envia para o servidor
    id_client = input("Enter Your Client ID: ")
    server.sendall(id_client.encode())

    while True:
      try:
        # Recebe o menu de opções do servidor e exibe para o cliente
        menu = server.recv(4096).decode()
        print(menu)

        # Cliente escolhe uma opção do menu
        option = input("\nSelect an Option: ")
        server.sendall(option.encode())

        # Recebe a resposta do servidor após a escolha da opção
        answer = server.recv(4096).decode()
        print(answer)

        # Se o cliente escolher a opção de fazer uma reserva
        if option == "1":
          # Solicita ao cliente o número da rota e envia para o servidor
          route = input("\nEnter a Number of the Route: ")
          server.sendall(route.encode())

          # Recebe e exibe as informações dos segmentos disponíveis
          segment_message = server.recv(4096).decode()
          print(segment_message)
          
          # Solicita ao cliente o número do segmento e envia para o servidor
          segment = input("\nEnter a Number of the Segment: ")
          server.sendall(segment.encode())

          # Recebe e exibe as informações dos assentos disponíveis
          seat_message = server.recv(4096).decode()
          print(seat_message)
          
          # Solicita ao cliente o número do assento e envia para o servidor
          seat = input("\nEnter a Number of the Seat: ")
          server.sendall(seat.encode())

          # Recebe a confirmação da reserva temporária do servidor
          confirmation = server.recv(4096).decode()
          print(confirmation)
        
        # Se o cliente escolher a opção de sair
        elif option == "4":
          break

      except Exception as error:
        # Tratamento de exceção para erros de conexão ou transmissão
        print(f"An error occurred: {error}")
        break

# Configurações do servidor (host e porta)
if __name__ == "__main__":
  server_host = "localhost"
  server_port = 12345
  request_reserve(server_host, server_port)
