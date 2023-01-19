import socket
import threading
import time
from datetime import datetime



class myThreadSP ( threading.Thread):
    
    def __init__(self,nome,cache, file, fileAll, porta, domain, debug):
        threading.Thread.__init__(self)
        self.name = nome
        self.cache = cache
        self.log = file
        self.logAll = fileAll
        self.porta = int(porta)
        self.domain = domain
        self.debug = debug
    
    def stringCache(self, array):
        string = ""
        for l in array:
            string += str(l) + ' '
        return string
        
    
    def run(self):
        
        
        
        sz = "entries: " + str(self.cache.size)
        m = []

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp.bind(('',self.porta))
        while 1:
            
            fileConfig = open(self.log,"a")
            fileConfigAll = open(self.logAll,"a")

            tcp.listen(1)
        
            c, addr = tcp.accept()
            domainSS = c.recv(1024).decode('utf-8')
            
            if (self.debug == "D"):
                print("ZT      ->    " + "Conection from SS: " + str(addr))
                print("              domain: " + domainSS)
            
            if (self.domain == domainSS):
                
                if (self.debug == "D"):
                    print("              Domain Accepted.")
                    
                c.send(sz.encode('utf-8'))
                msg = c.recv(1024).decode('utf-8')
            
                if (self.debug == "D"):
                    print("              " + msg)



                # envia os da cache para o SS
                for line in self.cache.tabela:
                    l = self.stringCache(line)
                    c.send(l.encode('utf-8'))
                    time.sleep(0.03)

            c.close()
            date = datetime.now()
            time1 = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
            fileConfig.write(time1 + " ZT " + str(addr[0]) + ':' + str(addr[1])+ " SP\n")
            fileConfigAll.write(time1 + " ZT " + str(addr[0]) + ':' + str(addr[1])+ " SP\n")
            if (self.debug == "D"):
                print("ZT      ->    " + time1 + " ZT " + str(addr[0]) + ':' + str(addr[1]) + " SP")
            fileConfig.close()
            fileConfigAll.close()
