import asyncio

from pickle import FALSE
import socket
from collections import deque
import random


def congestion_avoidance_RED(free_windows_size, buffer_size):
    if(free_windows_size < buffer_size / 2):
        valor_acima_metade = (free_windows_size - buffer_size/2)
        probabilidade_descarte = (valor_acima_metade*200)/buffer_size
        chance = random.randint(0,100)
        if(probabilidade_descarte > chance):
            return True
    return FALSE

MEU_IP = ''
MINHA_PORTA = 5001;
MEU_SERVIDOR = (MEU_IP, MINHA_PORTA)
BUFFER_SIZE = 1024 # Tamanho do Buffer de Recebimento
WINDOW_PACKAGES_SIZE = 10 # Tamanho da Janela Deslizante

async def ola_mundo():
   print('Olá ...')
   await asyncio.sleep(5)
   print('... Mundo!')

udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServer.bind(MEU_SERVIDOR)

print("UDP Server Listening for Packets");

receive_window = deque([])
free_window_size = WINDOW_PACKAGES_SIZE
# receive_window.popleft() - Removendo
# received_data_length = 0;
packages_received = 0

while(True):
    Mensagem_Recebida, END_cliente = udpServer.recvfrom(BUFFER_SIZE); # Posição 0 e 1024 do retorno
    
    # finalizando Servidor
    #if(Mensagem_Recebida.decode("utf8") == "FIN"): break
            
        
    print("Tamanho da Janela de Recepção", free_window_size)
    # Quebra dos Dados Recebidos
    payload = Mensagem_Recebida[1: len(Mensagem_Recebida)]
    ack = Mensagem_Recebida[0]

    print("ack", ack);
    print("janela", free_window_size)
    print("recebidos", packages_received)


    # Validando se Pacote recebido está na ordem, caso não esteja, descarta e retorna ACK anterior (Tratativa Go-Back-N (ACK cumulativo))
    if(ack == packages_received + 1 and free_window_size > 0 and congestion_avoidance_RED(free_window_size, 10)):
        receive_window.append(payload)
        #free_window_size = free_window_size - 1
        packages_received = packages_received + 1;
        if(packages_received == 255):
            packages_received = 0
        # for package in receive_window:
            # print("Recebi = " , package, " , Do Cliente: ", END_cliente)
        udpServer.sendto(ack.to_bytes(1, byteorder='big') + free_window_size.to_bytes(1, byteorder='big'), END_cliente)
        print(packages_received)

    else:
        print("Pacote Faltando")
        #if(free_window_size == 0):
            #free_window_size = free_window_size + 5
        #break
        udpServer.sendto(packages_received.to_bytes(1, byteorder='big') + free_window_size.to_bytes(1, byteorder='big'), END_cliente)


print("\n")
print("Finalizando Conexão")
udpServer.close()


