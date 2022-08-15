import socket
import os
import utils
import time

def sendData(packages, wnd_start, wnd_finish, udpClient, destiny):
    for data in packages[wnd_start: wnd_finish + 1]:
        udpClient.sendto(data['seq_number'].to_bytes(1, byteorder='big') + data["data"], destiny)

# Constantes
IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5000
DESTINO = (IP_SERVIDOR, PORTA_SERVIDOR)

MSS = 1

# Inicializando UDP Socket
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Realizando Quebra do arquivo em Chunks de Acordo com o MSS (Maximun Segment Size)
tamanho_arquivo = os.path.getsize("teste.txt")
print("tamanho do arquivo em Bytes:", tamanho_arquivo)
packages = utils.breakChunks('teste.txt', MSS)
print("Quantidade de Pacotes: ", len(packages))
print(packages)

# Realizando Comunicação
# Numero de Sequencia baseado em Inteiros

send_window_start = 0 # Variáveis de Controle da Janela Deslizante
send_window_finish = 0 # Variáveis de Controle da Janela Deslizante

finished = False
acks_received = []

payload = b''

# Enviando primeiro conjunto de Pacotes
print("Enviando 5 Pacote de Tamanho: " ,  MSS)
sendData(packages, send_window_start, send_window_finish, udpClient, DESTINO)

while(not finished):

    msgFromServer = udpClient.recvfrom(1024)[0];

    ack = msgFromServer[0]
    free_window = msgFromServer[1]

    if(send_window_start == (len(packages) - 1)):
        if(ack == packages[send_window_start]["seq_number"]):
            print("ACK: ", ack)
            finished = True;

    if(ack == packages[send_window_start]["seq_number"]):
        print("ACK: ", ack)
        send_window_start = send_window_start + 1;
        
        if(send_window_finish < len(packages) - 1):
            send_window_finish = send_window_finish + 1;
            udpClient.sendto(packages[send_window_finish]['seq_number'].to_bytes(1, byteorder='big') + packages[send_window_finish]["data"], DESTINO)
    
    elif(ack < packages[send_window_start]["seq_number"]):
        print("ACK: ", ack)
        print("Reenviando")
        break
        sendData(packages, send_window_start, send_window_finish, udpClient, DESTINO)
    
if(finished ):
    udpClient.sendto("FIN".encode("utf8"), DESTINO)




# Numero de Sequencia baseado em Fluxo de Bytes
# index = 0
# finished = False

# while(not finished):
#     print("Enviando Pacote de Tamanho: " ,  MSS)
#     udpClient.sendto(packages[index]['data'], DESTINO)

#     msgFromServer = udpClient.recvfrom(1024)[0];

#     if(index == (len(packages) - 1)):
#         if(int(msgFromServer.decode("utf8")) == packages[index]["seq_number"] + len(packages[index]["data"])):
#             print("ACK: ", msgFromServer)
#             finished = True;
#         else:
#             # print(msgFromServer.decode("utf8"))
#             # print('tamanho: ',len(packages[index]))
#             print("Ocorreu Perda dos Dados")
#             print("reenviando Pacote: ", packages[index]["seq_number"])
#     elif(int(msgFromServer.decode("utf8")) == packages[index + 1]["seq_number"]):
#         print("ACK: ", msgFromServer)
#         index = index + 1;
#     else:
#         # print(msgFromServer.decode("utf8"))
#         print("Ocorreu Perda dos Dados")
#         print("reenviando Pacote: ", packages[index]["seq_number"])

# if(finished ):
#     udpClient.sendto("FIN".encode("utf8"), DESTINO)

print("\n")
print("Finalizando Conexão")
udpClient.close()