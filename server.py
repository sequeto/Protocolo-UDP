import socket
from collections import deque


MEU_IP = '';
MINHA_PORTA = 5000;
MEU_SERVIDOR = (MEU_IP, MINHA_PORTA)
BUFFER_SIZE = 1024 # Tamanho do Buffer de Recebimento

ACK = str.encode("Retorno Recebido");

udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServer.bind(MEU_SERVIDOR)

print("UDP Server Listening for Packets");

buffer = deque([]);
# buffer.popleft() - Removendo
# received_data_length = 0;
packages_received = 0

while(True):
    Mensagem_Recebida, END_cliente = udpServer.recvfrom(BUFFER_SIZE); # Posição 0 e 1024 do retorno
    if(Mensagem_Recebida.decode("utf8") == "FIN"): break

    buffer.append(Mensagem_Recebida.decode("utf8"))
    for data in buffer:
        print("Recebi = " , data, " , Do Cliente: ", END_cliente)
    udpServer.sendto(str(packages_received).encode("utf8"), END_cliente)
    packages_received = packages_received + 1;
    print(packages_received)

# while(True):
#     Mensagem_Recebida, END_cliente = udpServer.recvfrom(BUFFER_SIZE); # Posição 0 e 1024 do retorno
#     if(Mensagem_Recebida.decode("utf8") == "FIN"): break

#     buffer.append(Mensagem_Recebida.decode("utf8"))
#     received_data_length = received_data_length + len(Mensagem_Recebida);
#     for data in buffer:
#         print("Recebi = " , data, " , Do Cliente: ", END_cliente)
#     udpServer.sendto(str(received_data_length + 1).encode("utf8"), END_cliente)
#     print(received_data_length)

print("\n")
print("Finalizando Conexão")
udpServer.close()
