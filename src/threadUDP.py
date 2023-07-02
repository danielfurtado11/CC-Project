import threading
import socket
from Query import Query
from datetime import datetime

class mythreadUDP(threading.Thread):
    
    def __init__(self,nome,porta,cache,file,fileAll,debug):
        threading.Thread.__init__(self)
        self.name = nome
        self.porta = porta
        self.cache = cache
        self.log = file
        self.logAll = fileAll
        self.debug = debug
        
    
    def run(self):
        

        bufferSize = 1024
        bytesToSend = ""
        # Criar um socket
        UDPServerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)

        # Bind para a porta e o ip
        UDPServerSocket.bind(('', self.porta))

        # Espera pelos datagramas
        while(True):
            fileConfig = open(self.log,"a")
            fileConfigAll = open(self.logAll, "a")
            bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAdressPair[0]
            adress = bytesAdressPair[1]

            if (self.debug == "D"):
                print("QUERY   ->   Conection from client: " + str(adress) + "\n             Query: " + message.decode())
            
            
            date = datetime.now()
            time1 = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
            fileConfig.write(time1 + " QR " + str(adress[0]) + ':' + str(adress[1]) + " " + str(message.decode()) + '\n')
            fileConfigAll.write(time1 + " QR " + str(adress[0]) + ':' + str(adress[1]) + " " + str(message.decode()) + '\n')
            if (self.debug == "D"):
                print("QUERY    ->    " + time1 + " QR " + str(adress[0]) + ':' + str(adress[1]) + ' ' + str(message.decode()))
            
            
            messageQuery = message.decode()
            query = Query(messageQuery,self.cache)
            query.makeQuery()
            array = query.parseQuery()
            
            date = datetime.now()
            time1 = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
            fileConfig.write(time1 + " RE " + str(adress[0]) + ':' + str(adress[1]) + " " + str(array) + '\n')
            fileConfigAll.write(time1 + " RE " + str(adress[0]) + ':' + str(adress[1]) + " " + str(array) + '\n')
            
            if (self.debug == "D"):
                print("QUERY    ->    " + time1 + " RE " + str(adress[0]) + ':' + str(adress[1]) + ' ' + str(array))
            
            fileConfig.close()
            fileConfigAll.close()
            
            for l in array:
                bytesToSend = str.encode(l)
                UDPServerSocket.sendto(bytesToSend, adress)
            

            
        
