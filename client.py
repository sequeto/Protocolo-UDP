import socket

IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5000
DESTINO = (IP_SERVIDOR, PORTA_SERVIDOR)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mensagem = input()

udp.sendto(bytes(mensagem, "utf-8"), DESTINO)

udp.close()