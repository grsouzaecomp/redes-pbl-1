<div align="center">
  <h1>
      Relatório do problema 1: Sistema de Reservas de Assentos
  </h1>

  <h3>
    Gabriel Ribeiro Souza & Kevin Cordeiro Borges
  </h3>

  <p>
    Engenharia de Computação – (UEFS)
    Av. Transnordestina, s/n, Novo Horizonte
    Feira de Santana – Bahia, Brasil – 44036-900
  </p>

  <center>gabasribeirosz@gmail.com & kcordeiro539@gmail.com</center>

</div>

# 1. Introdução

<p style="text-align: justify;">
  A gestão eficiente de reservas é essencial para diversos serviços de transporte. A falta de um sistema automatizado dificulta a alocação de assentos em rotas segmentadas, gerando problemas de disponibilidade e controle de reservas. Este projeto apresenta um sistema de servidor para gerenciar reservas de assentos em rotas de transporte segmentadas, utilizando comunicação via TCP/IP e controle de concorrência com threads e locks, garantindo segurança e integridade dos dados.
</p>

<p style="text-align: justify;">
  O sistema foi implementado em Python, utilizando sockets TCP/IP para comunicação entre o cliente e o servidor. A arquitetura permite múltiplas conexões simultâneas e o gerenciamento independente de cada cliente através de threads. O servidor mantém um controle seguro das reservas temporárias e confirmadas, automatizando o processo e melhorando a experiência do usuário.
</p>

# 2. Metodologia

<p style="text-align: justify;">
  O sistema é composto por duas partes principais: o cliente e o servidor. O cliente se conecta ao servidor via um socket TCP/IP, permitindo a comunicação bidirecional e a interação com o usuário para realizar reservas de assentos. A arquitetura suporta múltiplas conexões simultâneas, e cada cliente é gerenciado por uma thread dedicada no servidor, garantindo que as operações sejam executadas de forma independente e segura. Foi utilizado
o padrão TCP/IP onde o TCP garante a entrega ordenada e confiável dos pacotes de dados, enquanto o IP define o endereço dos dispositivos na rede e roteia os pacotes para o destino correto. Juntos, eles formam a base da comunicação na internet. Seguindo a seguinte estrutura demonstrada na imagem abaixo:
</p>

![Explicação do TCP/IP.](https://github.com/grsouzaecomp/redes-pbl-1/blob/main/images/explicacao_tcp_ip.png)

<p style="text-align: justify;">
  <b>Implementação do TCP/IP:</b> O padrão TCP/IP desempenha um papel central na comunicação entre cliente e servidor. As funções principais utilizadas incluem:
</p>

<ul>
  <li><b>Socket TCP/IP:</b> Criação de um socket TCP para estabelecer uma conexão de fluxo de dados entre o cliente e o servidor, garantindo a entrega ordenada e confiável dos pacotes.</li>
  <li><b>Conexão (connect):</b> Utilizada pelo cliente para se conectar ao endereço e porta especificados do servidor, estabelecendo uma sessão de comunicação.</li>
  <li><b>Bind (bind):</b> O servidor associa seu socket a um endereço IP específico e uma porta, preparando-se para escutar conexões de entrada.</li>
  <li><b>Escuta de Conexões (listen):</b> Habilita o servidor a escutar conexões dos clientes na porta especificada, transformando o socket em um socket de "escuta".</li>
  <li><b>Aceitação de Conexões (accept):</b> O servidor aceita novas conexões de clientes, criando um novo socket dedicado para gerenciar a comunicação com cada cliente individual.</li>
  <li><b>Envio de Dados (sendall):</b> Usado para enviar dados entre o cliente e o servidor, garantindo que todos os dados sejam transmitidos corretamente.</li>
  <li><b>Recebimento de Dados (recv):</b> Recebe mensagens e comandos através do socket, bloqueando a execução até que os dados estejam disponíveis.</li>
  <li><b>Fechamento da Conexão (close):</b> Utilizada para encerrar a comunicação e liberar os recursos associados aos sockets.</li>
</ul>

<p style="text-align: justify;">
  A estruturação do Código foi previamente discutida em sala, e baseando-se nas ideias iniciais e de outros colegas, foi feita uma representação visual do funcionamento do código:
</p>

![Estruturação do Código.](https://github.com/grsouzaecomp/redes-pbl-1/blob/main/images/estrutura_codigo.png)

<p style="text-align: justify;">
  <b>Funcionalidades Implementadas:</b> O sistema oferece funcionalidades como fazer reservas, confirmar reservas temporárias, visualizar reservas confirmadas e controle de segurança utilizando locks para evitar conflitos durante operações concorrentes.
</p>

# 3. Resultados

<p style="text-align: justify;">
  Durante a execução dos testes, o sistema demonstrou ser capaz de gerenciar múltiplos clientes simultaneamente, mantendo a integridade das reservas. Também foram implementadas funcionalidades de reserva temporária e confirmação de assentos, com o cancelamento automático de reservas temporárias após o tempo limite de 30 segundos. O cliente interage com o sistema a partir de um menu, conforme a imagem abaixo:
</p>

![Menu do Cliente](https://github.com/grsouzaecomp/redes-pbl-1/blob/main/images/menu_principal.png)

<p style="text-align: justify;">
Caso o cliente não confirme sua reserva em um período de 30 segundos, é exibida para o servidor a mensagem de que a reserva foi expirada, conforme a imagem abaixo:
</p>

![Reserva Expirada](https://github.com/grsouzaecomp/redes-pbl-1/blob/main/images/reserva_expirada.png)

<p style="text-align: justify;">
O uso de locks garantiu que operações críticas fossem executadas corretamente, sem que vários clientes pudessem selecionar o mesmo assento. Caso outro cliente com outro ID tente selecionar o mesmo assento, é apresentado para ele que o assento em questão está indisponível, conforme a imagem abaixo:
</p>

![Assento Indisponível](https://github.com/grsouzaecomp/redes-pbl-1/blob/main/images/assento_indisponivel.png)

<p style="text-align: justify;">
Confirmando sua reserva, o cliente terá suas reservas confirmadas na opção três, onde o mesmo pode visualizar suas reservas confirmadas, conforme a imagem abaixo:
</p>

![Reservas Confirmadas](https://github.com/grsouzaecomp/redes-pbl-1/blob/main/images/reserva_confirmada.png)

<p style="text-align: justify;">
  O servidor gerencia de forma eficiente as conexões e reservas, proporcionando uma experiência de usuário intuitiva e segura. A arquitetura permite escalabilidade e pode ser adaptada para ambientes com maior volume de acessos.
</p>

# 4. Conclusão

<p style="text-align: justify;">
  O projeto do servidor de reservas mostrou-se eficaz para o gerenciamento de reservas de assentos em rotas segmentadas, com um sistema robusto que atende a requisitos de concorrência e segurança. Os testes demonstraram que o sistema pode lidar com múltiplos usuários simultâneos sem comprometer a integridade dos dados. O aprendizado adquirido com o desenvolvimento deste sistema pode ser aplicado em projetos futuros de gestão de recursos e reservas, especialmente em ambientes que demandam alta disponibilidade e controle rigoroso de acesso concorrente.
</p>

<p style="text-align: justify;">
  Futuras melhorias podem incluir a otimização da gestão de threads no servidor para melhorar o desempenho em ambientes com um número ainda maior de clientes e também uma opção para que o cliente cancele suas reservas já feitas, além da criação de uma interface gráfica de usuário para tornar o sistema mais acessível e fácil de usar.
</p>

# Referências

<p style="text-align: justify;">
  Introdução a Sockets em Python. Disponível em: https://medium.com/@urapython.community/introdu%C3%A7%C3%A3o-a-sockets-em-python-44d3d55c60d0. Acesso em: 17 de agosto de 2024.
</p>

<p styler="text-align: justify;">
  Arquitetura TCP/IP: o que é, protocolos, camadas e conceitos, 2024. Disponível em: https://www.eletronet.com/blog/arquitetura-tcp-ip/. Acesso em: 20 de agosto de 2024.
</p>

<p style="text-align: justify;">
  threading — Thread-based parallelism. Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/threading.html. Acesso em: 20 de agosto de 2024.
</p>

<p style="text-align: justify;">
  ANDRADE, Thiago. Programação Concorrente Utilizando Múltiplas Threads em Python. Revelo Community. 2023. Disponível em: https://community.revelo.com.br/programacao-concorrente-utilizando-multiplas-threads-em-python/. Acesso em: 1 de setembro de 2024.
</p>

<p style="text-align: justify;">
  socket — Low-level networking interface. Python Software Foundation. 2023. Disponível em: https://docs.python.org/3/library/socket.html. Acesso em: 8 de setembro de 2024.
</p>
