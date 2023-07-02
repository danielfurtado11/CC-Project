import threading
import socket
from Query import Query
from srConnect import srConnect
from time import perf_counter
from datetime import datetime


class mythreadSR(threading.Thread):
    
    def __init__(self,nome,porta,cache,file,debug,dd,st,timeout):
        threading.Thread.__init__(self)
        self.name = nome
        self.porta = porta
        self.cache = cache
        self.log = file
        self.debug = debug
        self.dd = dd
        self.st = st
        self.timeout = timeout
        self.sdt = {}
    
            
        
    
    
    
    def run(self):
        start = perf_counter()
        bufferSize = 1024
        bytesToSend = ""
        UDPServerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
        
        UDPServerSocket.bind(('',self.porta))
        
        
        while(True):
            fileConfig = open(self.log,"a")
            bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAdressPair[0]
            address = bytesAdressPair[1]
            messageQuery = message.decode()
            query = Query(messageQuery,self.cache)
            query.makeQuery()
            array = query.parseQuery()
            
            date = datetime.now()
            time = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
            
            if (self.debug == "D"):
                print("QUERY    ->    " + time + " QR " + str(address[0]) + ':' + str(address[1]) + ' ' + str(message.decode()))
            fileConfig.write(time + " QR " + str(address[0]) + ':' + str(address[1]) + " " + str(message.decode()) + '\n')
            

            if (query.responseCode == 0):
                self.debugPrint(responseQuery,address,fileConfig,self.debug)
                for l in array:
                    bytesToSend = str.encode(l)
                    UDPServerSocket.sendto(bytesToSend, address)
                

            
            validDD = False
            ipDD = []
            for (key,values) in self.dd.items():
                
                d1 = messageQuery.split(";")
                domain = d1[1].split(",")
                domain = domain[0]
                if(domain.endswith(key)):
                    validDD = True
                    ipDD.append(values)
                    #ip = values
                    break
                
            if domain.endswith("reverse."):

                output = srConnect(self.st,messageQuery,self.cache,self.timeout)
                responseQuery = output.connectTo()
                stReverse = []
                for response in responseQuery[1:]:
                    responseValues = response[:-1].split(",")       # separa o array onde tem a resposta da query
                    for values in responseValues:
                        values = values.split(" ")
                                                 
                        if len(values) > 1:
                            if values[1] == "A":
                             stReverse.append(values[2])
                
                output = srConnect(stReverse,messageQuery,self.cache,self.timeout)
                responseQuery = output.connectTo()
                sdtReverse = []
                for response in responseQuery[1:]:
                    responseValues = response[:-1].split(",")       # separa o array onde tem a resposta da query
                    for values in responseValues:
                        values = values.split(" ")
                                                 
                        if len(values) > 1:
                            if values[1] == "A":
                             sdtReverse.append(values[2])
                             
                output = srConnect(sdtReverse,messageQuery,self.cache,self.timeout)
                responseQuery = output.connectTo()
                spReverse = []
                
                for response in responseQuery[1:]:
                    responseValues = response[:-1].split(",")       # separa o array onde tem a resposta da query
                    for values in responseValues:
                        values = values.split(" ")
             
                        if len(values) > 1:
                            if values[1] == "A":
                             spReverse.append(values[2])
                             
                output = srConnect(spReverse,messageQuery,self.cache,self.timeout)
                responseQuery = output.connectTo()
                          
                self.debugPrint(responseQuery,address,fileConfig,self.debug)
                self.adicionaRespostaCache(responseQuery,start)
                for l in responseQuery:
                    bytesToSend = str.encode(l)
                    UDPServerSocket.sendto(bytesToSend, address)
                
                         
            else:
                
                if(validDD == True and query.responseCode != 0):        # quando não encontra a resposta na cache
                    
                    
                    output = srConnect(ipDD,messageQuery,self.cache,self.timeout)
                    responseQuery = output.connectTo()
                    if len(responseQuery) == 1:
                       responseCode = 1
                    if len(responseQuery) != 1:
                      responseCode = int((responseQuery[0]).split(",")[2])  
                             
    
                      if (responseCode == 0):
                          self.adicionaRespostaCache(responseQuery,start)
                          self.debugPrint(responseQuery,address,fileConfig,self.debug)
                          for l in responseQuery:
                              bytesToSend = str.encode(l)
                              UDPServerSocket.sendto(bytesToSend, address)
                            
                
                
                
                if (validDD == False or responseCode != 0):
                
                    output = srConnect(self.st,messageQuery,self.cache,self.timeout)
                    responseQuery = output.connectTo()
                    if len(responseQuery) == 1:
                         bytesToSend = str.encode(responseQuery[0])
                         UDPServerSocket.sendto(bytesToSend, address)
                         UDPServerSocket.sendto(bytesToSend,address)
                         UDPServerSocket.sendto(bytesToSend,address)
                         UDPServerSocket.sendto(bytesToSend,address)
                    else:
                      responseCode = int((responseQuery[0]).split(",")[2])
    
    
    
                      for response in responseQuery[1:]:
                          responseValues = response[:-1].split(",")       # separa o array onde tem a resposta da query
                          for values in responseValues:
                              values = values.split(" ")
                                                     
                              if len(values) > 1:
                                  if values[1] == "A":
                                   self.sdt[values[0]] = values[2]
    
    
                                
                      if (responseCode == 0 or responseCode == 2):
                          self.debugPrint(responseQuery,address,fileConfig,self.debug)
                          self.adicionaRespostaCache(responseQuery,start)
                          for l in responseQuery:
                              bytesToSend = str.encode(l)
                              UDPServerSocket.sendto(bytesToSend, address)
                            
                    
                      else:
                    
                          ipS = []
                          for (ns,ips) in self.sdt.items():                  
                              server = ns.split(".")
                              ns = server[1]
                              if ns in domain:
                                  ipS.append(ips)
    
    
                          output = srConnect(ipS,messageQuery,self.cache,self.timeout)
                          responseQuery = output.connectTo()
                          if (len(responseQuery) == 1):
                            bytesToSend = str.encode(responseQuery[0])
                            UDPServerSocket.sendto(bytesToSend, address)
                            UDPServerSocket.sendto(bytesToSend,address)
                            UDPServerSocket.sendto(bytesToSend,address)
                            UDPServerSocket.sendto(bytesToSend,address)
                          else:
                            responseCode = int((responseQuery[0]).split(",")[2])    # codigo da resposta da query [0|1|2|3]
    
    
    
                          # Quando não há SP na query quer dizer que não há servidor do subdomínio na Query por isso não é suposto ligar ao subdomínio
                          # Por exemplo quando o cliente pede uma query errada no entanto não há alternativa então tem que enviar com o resultado a 1 
                            if  ("sp" not in responseQuery[3]):
                                self.adicionaRespostaCache(responseQuery,start)
                                self.debugPrint(responseQuery,address,fileConfig,self.debug)
                            
                                for l in responseQuery:
                                    bytesToSend = str.encode(l)
                                    UDPServerSocket.sendto(bytesToSend, address)
                        
                        
                            else:
                                ipS = []
                                ipS.append( ((responseQuery[3][:-1]).split(" "))[2])
                                output = srConnect(ipS,messageQuery,self.cache,self.timeout) 
                                responseQuery = output.connectTo()
                                if len(responseQuery) == 1:
                                    bytesToSend = str.encode(responseQuery[0])
                                    UDPServerSocket.sendto(bytesToSend,address)
                                    UDPServerSocket.sendto(bytesToSend,address)
                                    UDPServerSocket.sendto(bytesToSend,address)
                                    UDPServerSocket.sendto(bytesToSend,address)
                                    
                                else:
                                    responseCode = int((responseQuery[0]).split(",")[2])            
                                    self.debugPrint(responseQuery,address,fileConfig,self.debug)
                                    self.adicionaRespostaCache(responseQuery,start)
                                    for l in responseQuery:
                                        bytesToSend = str.encode(l)
                                        UDPServerSocket.sendto(bytesToSend, address)
                                    


                        
                        
                        
    def debugPrint(self,message,address,file,debug):
        date = datetime.now()
        time1 = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
        file.write(time1 + " RE " + str(address[0]) + ':' + str(address[1]) + " " + str(message) + '\n')
        if (debug == "D"):
           print("QUERY    ->    " + time1 + " RE " + str(address[0]) + ':' + str(address[1]) + ' ' + str(message))
                        

    def adicionaRespostaCache(self,responseQuery,start):
        for response in responseQuery[1:]:
            responseValues = response[:-1].split(",")       # separa o array onde tem a resposta da query
            for values in responseValues:
                values = values.split(" ")
                stop = perf_counter()
                timestamp = stop-start
                if len(values) == 4:
                    self.cache.updateCache(values[0],values[1],values[2],values[3],"-","OTHERS",str(timestamp),"VALID")
                elif len(values) == 5:
                    self.cache.updateCache(values[0],values[1],values[2],values[3],values[4],"OTHERS",str(timestamp),"VALID")
