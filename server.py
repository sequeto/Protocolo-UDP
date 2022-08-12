import socket


MEU_IP = '';
MINHA_PORTA = 5000;
MEU_SERVIDOR = (MEU_IP, MINHA_PORTA)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(MEU_SERVIDOR)

Mensagem_Recebida, END_cliente = udp.recvfrom(1024);

print("Recebi = " , Mensagem_Recebida, " , Do Cliente: ", END_cliente)


udp.close()
