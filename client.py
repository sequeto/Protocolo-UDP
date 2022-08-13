from lib2to3.pgen2.token import EQUAL
import socket
import os
import utils

# Constantes
IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5000
DESTINO = (IP_SERVIDOR, PORTA_SERVIDOR)
MSS = 10


# Inicializando UDP Socket
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Realizando Quebra do arquivo em Chunks de Acordo com o MSS (Maximun Segment Size)
tamanho_arquivo = os.path.getsize("teste.txt")
print("tamanho do arquivo em Bytes:", tamanho_arquivo)
packages = utils.breakChunks('teste.txt', MSS)
print("Quantidade de Pacotes: ", len(packages))

# Realizando Comunicação
index = 0
finished = False


while(not finished):
    print("Enviando Pacote de Tamanho: " ,  MSS)
    udpClient.sendto(packages[index], DESTINO)

    msgFromServer = udpClient.recvfrom(1024)[0];
    print(msgFromServer)
    index = index +1;

    if index == len(packages):
        finished = True;

    # if(int(msgFromServer.decode("utf8")) == len(packages[index]) + 1):
    #     print("ACK: ", msgFromServer)
    #     index = index +1;
    # else:
    #     print("Ocorreu Perda dos Dados")

udpClient.close()