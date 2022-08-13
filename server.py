import socket


MEU_IP = '';
MINHA_PORTA = 5000;
MEU_SERVIDOR = (MEU_IP, MINHA_PORTA)

ACK = str.encode("Retorno Recebido");

udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServer.bind(MEU_SERVIDOR)

print("UDP Server Listening for Packets");

while(True):
    Mensagem_Recebida, END_cliente = udpServer.recvfrom(1024); # Posição 0 e 1 do retorno
    print("Recebi = " , Mensagem_Recebida, " , Do Cliente: ", END_cliente)
    udpServer.sendto(ACK, END_cliente)

udpServer.close()
