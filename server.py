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
    
    # finalizando Servidor
    if(Mensagem_Recebida.decode("utf8") == "FIN"): break

    # Quebra dos Dados Recebidos
    payload = Mensagem_Recebida[1: len(Mensagem_Recebida)]
    ack = Mensagem_Recebida[0]

    # Validando se Pacot recebido está na ordem, caso não esteja, descarta e retorna ACK anterior (Tratativa Go-Back-N (ACK cumulativo))
    if(ack == packages_received + 1):
        buffer.append(payload.decode("utf8"))
        for data in buffer:
            print("Recebi = " , data, " , Do Cliente: ", END_cliente)
        udpServer.sendto(ack.to_bytes(1, byteorder='big'), END_cliente)
        packages_received = packages_received + 1;
        print(packages_received)

    else:
        udpServer.sendto(packages_received.to_bytes(1, byteorder='big'), END_cliente)


print("\n")
print("Finalizando Conexão")
udpServer.close()
