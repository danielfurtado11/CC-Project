import socket
import sys
import random


class Client:

    recursive = ""
    ipPorta = str(sys.argv[1])
    dominio = (sys.argv[2])
    type = str(sys.argv[3])
    recurse = ""
    
    if len(sys.argv)>4:
        recurse = str(sys.argv[4])
    
    ipS = ipPorta.split(':')  

    ip = ipS[0]     # Ip do servidor
    porta = ipS[1]  # porta do servidor

    id = random.randint(1,65535)
    
    
    
    if recurse == 'R':
        flags = "Q+R"
    else:
        flags = "Q"
    
    query = str(id)+','+ flags + ',' + '0,0,0,0;'+ str(dominio) + ',' + str(type) + ';'
    print("Pedido de Query :  " + query + '\n')
    
    bytesToSend = str.encode(query)
    
    serverAddressPort = (ip, int(porta))
    
    bufferSize = 1024
    
    # Criar um socket UDP no lado do cliente 
    UDPClientSocket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)
    
    
    # Enviar ao servidor usando o socket UDP
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    
    print("         #-------------#         Resultado da Query         #-------------#     ")
    
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print(msgFromServer[0].decode('utf-8'))
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print(msgFromServer[0].decode('utf-8'))
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print(msgFromServer[0].decode('utf-8'))
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    print(msgFromServer[0].decode('utf-8'))
    UDPClientSocket.close()
    
    print("         #----------------------------------------------------------------#     ")
    
    
    # EXEMPLO DE QUERY:    
    # python3.10 cliente.py 127.0.0.1:2000 www.grande.guaxinim. A R
    # python3.10 cliente.py 127.0.0.1:2000 grande.guaxinim MX R
