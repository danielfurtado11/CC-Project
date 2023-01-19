from parseDB import parseDB
from Cache import Cache
from parseConfig import parseConfig
import sys
import os
from datetime import datetime
import socket
from Query import Query
from datetime import datetime


class st:



    s = len(sys.argv)
    
    if s == 5:
        txt = sys.argv[1]   # ficheiro de configuração 
        porta = int(sys.argv[2])    # porta
        timeout = sys.argv[3]   # tempo de timeout
        debug = sys.argv[4]     # debug opção
    if s == 4:
        txt = sys.argv[1]
        porta = 53
        timeout = int(sys.argv[2])
        debug = sys.argv[3]
        
    bufferSize = 1024
    
    config = parseConfig(txt)
    config.fileopen()
    date = datetime.now()
    time = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
    
    db = config.database
    log = config.lg[0]

    
    
    
    
    if os.path.exists(log):
        fileConfigAll = open(log, "a")
    else:
        fileConfigAll = open(log,"x")
        

    if (debug == "D"):
        fileConfigAll.write(str(time) + " ST 127.0.0.1 " + str(porta) + " " + str(timeout) + " shy\n")
        print("LOGS    ->    " + str(time) + " 127.0.0.1 " + str(porta) + " " + str(timeout) + " shy")
    else:
        fileConfigAll.write(str(time) + " ST 127.0.0.1 " + str(porta) + " " + str(timeout) + "\n")
    fileConfigAll.write(str(time) + " EV " + "conf-file-read " + txt +'\n')  
    
    
    if (debug == "D"):
        print("LOGS    ->    " + str(time) + " EV log-file-create " + log)
        
    cache = Cache()
    parse = parseDB(db,cache)
    parse.converte()
    


    date = datetime.now()
    time = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
    
    
    fileConfigAll.write(str(time) + " EV " + "db-file-read " + db + '\n')

    if (debug == "D"):
        print("LOGS    ->    " + str(time) + " EV db-file-read " + db)
    

    
    
    bytesToSend = ""
    # Criar um socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
    # Bind para a porta e o ip
    UDPServerSocket.bind(('', porta))
    
    while(True):
        

        bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAdressPair[0]
        adress = bytesAdressPair[1]
        if (debug == "D"):
            print("QUERY   ->   Conection from client: " + str(adress) + "\n             Query: " + message.decode())
        
        
        date = datetime.now()
        time1 = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
        fileConfigAll.write(time1 + " QR " + str(adress[0]) + ':' + str(adress[1]) + " " + str(message.decode()) + '\n')
        
        if (debug == "D"):
            print("QUERY    ->    " + time1 + " QR " + str(adress[0]) + ':' + str(adress[1]) + ' ' + str(message.decode()))
        
        
        messageQuery = message.decode()
        query = Query(messageQuery,cache)
        query.makeQuery()
        array = query.parseQuery()
        
        date = datetime.now()
        time1 = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
        fileConfigAll.write(time1 + " RE " + str(adress[0]) + ':' + str(adress[1]) + " " + str(array) + '\n')
        
        if (debug == "D"):
            print("QUERY    ->    " + time1 + " RE " + str(adress[0]) + ':' + str(adress[1]) + ' ' + str(array))
        
        #fileConfigAll.close()
        
        for l in array:
            bytesToSend = str.encode(l)
            UDPServerSocket.sendto(bytesToSend, adress)
    
        
    
