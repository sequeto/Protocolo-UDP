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
    udpClient.sendto(packages[index]['data'], DESTINO)

    msgFromServer = udpClient.recvfrom(1024)[0];

    if(index == (len(packages) - 1)):
        if(int(msgFromServer.decode("utf8")) == packages[index]["seq_number"] + len(packages[index]["data"])):
            print("ACK: ", msgFromServer)
            finished = True;
        else:
            print(msgFromServer.decode("utf8"))
            print('tamanho: ',len(packages[index]))
            print("Ocorreu Perda dos Dados")
            print("reenviando Pacote: ", packages[index]["seq_number"])
    elif(int(msgFromServer.decode("utf8")) == packages[index + 1]["seq_number"]):
        print("ACK: ", msgFromServer)
        index = index + 1;
    else:
        print(msgFromServer.decode("utf8"))
        print("Ocorreu Perda dos Dados")
        print("reenviando Pacote: ", packages[index]["seq_number"])

if(finished ):
    udpClient.sendto("FIN".encode("utf8"), DESTINO)

print("\n")
print("Finalizando Conexão")
udpClient.close()