import socket

IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5000
DESTINO = (IP_SERVIDOR, PORTA_SERVIDOR)
BUFFER_SIZE = 1024

udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mensagem = input()

udpClient.sendto(str.encode(mensagem), DESTINO)

msgFromServer = udpClient.recvfrom(BUFFER_SIZE);
print(msgFromServer)

udpClient.close()