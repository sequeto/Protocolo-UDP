#Equação de Controle de Congestionamento - Técnica Slow Start

import socket
import os
import utils
import time
import select

def sendData(packages, wnd_start, quantity, udpClient, destiny):
    for data in packages[wnd_start: send_window_finish]:
        print("Enviando Pacote: ", data['seq_number'])
        udpClient.sendto(data['seq_number'].to_bytes(1, byteorder='big') + data["data"], destiny)

# Constantes
IP_SERVIDOR = '127.0.0.1'
PORTA_SERVIDOR = 5001
DESTINO = (IP_SERVIDOR, PORTA_SERVIDOR)

MSS = 1000

# Inicializando UDP Socket
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Realizando Quebra do arquivo em Chunks de Acordo com o MSS (Maximun Segment Size)
tamanho_arquivo = os.path.getsize("teste.txt")
print("tamanho do arquivo em Bytes:", tamanho_arquivo)
packages = utils.breakChunks('teste.txt', MSS)
print("Quantidade de Pacotes: ", len(packages))
#print(packages)

# Realizando Comunicação
# Numero de Sequencia baseado em Inteiros
resending = 0
limit = 0

waiting_ack = 0
send_window_start = 0 # Variáveis de Controle da Janela Deslizante
send_window_finish = 1 # Variáveis de Controle da Janela Deslizante
finished = False

# Enviando primeiro conjunto de Pacotes
print("Enviando ", send_window_finish - send_window_start, " Pacotes de Tamanho: " ,  MSS)
sendData(packages, send_window_start, send_window_finish, udpClient, DESTINO)

while(not finished):

    returned, write, err = select.select([udpClient],[],[],3)

    #print("Esperando", packages[waiting_ack]["seq_number"])
    #print("Inicio", send_window_start)
    #print("Fim", send_window_finish)

    if(resending > 10):
        send_window_finish = send_window_start + 2; 

    elif(returned and len(returned) > 0):
        msgFromServer = udpClient.recvfrom(1024)[0];

        print("Recebendo")
        ack = msgFromServer[0]
        free_window = msgFromServer[1]

        print("Janela: ", free_window);

        if(waiting_ack == (len(packages) - 1)):
            if(ack == packages[waiting_ack]["seq_number"]):
                print("ACK: ", ack)
                finished = True;
        

        if(ack == packages[waiting_ack]["seq_number"]):
            resending = 0
            print("ACK: ", ack)
            waiting_ack = waiting_ack + 1
            send_window_start = send_window_finish;
            
            if(send_window_finish <= len(packages) - 1):
                if(send_window_finish * 2 < len(packages) - 1):
                    send_window_finish = send_window_finish * 2;

                else:
                    send_window_finish = send_window_finish + (len(packages) - send_window_finish);
                    
                if(free_window == 0):
                    print("Aguardando Janela de Pacotes Liberar Espaço")
                    time.sleep(5)
                # udpClient.sendto(packages[send_window_finish]['seq_number'].to_bytes(1, byteorder='big') + packages[send_window_finish]["data"], DESTINO)
                sendData(packages, send_window_start, send_window_finish, udpClient, DESTINO)

        elif(ack < packages[waiting_ack]["seq_number"]):
            print("ACK: ", ack)
            if(free_window == 0):
                print("Aguardando Janela de Pacotes Liberar Espaço")
                time.sleep(5)
            resending = resending + 1
            print("Reenviando")
            sendData(packages, send_window_start, send_window_finish, udpClient, DESTINO)
    else:
        print("TimeOut: Reenviando")
        resending = resending + 1
        sendData(packages, send_window_start, send_window_finish, udpClient, DESTINO)

        
    
if(finished):
    udpClient.sendto("FIN".encode("utf8"), DESTINO)


print("\n")
print("Finalizando Conexão")
udpClient.close()