from cgi import test
import socket
import os

IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5000
DESTINO = (IP_SERVIDOR, PORTA_SERVIDOR)
BUFFER_SIZE = 1

udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tamanho_arquivo = os.path.getsize("teste.txt")
print("tamanho do arquivo em Bytes:", tamanho_arquivo)
mensagem = input()

udpClient.sendto(str.encode(mensagem), DESTINO)

msgFromServer = udpClient.recvfrom(BUFFER_SIZE);
print(msgFromServer)

udpClient.close()