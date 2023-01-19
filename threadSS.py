import threading
import socket
import time
from datetime import datetime

class myThreadSS (threading.Thread):
   
   def __init__(self,nome,portaIP,cache,dominio,file, fileAll, debug):
      threading.Thread.__init__(self)
      portaIP = portaIP.split(':')
      self.name = nome
      self.ip = portaIP[0]
      self.cache = cache
      self.domain = dominio
      self.soaRetry = 0
      if len(portaIP)>1:
         self.porta = int(portaIP[1])
      else:
         self.porta = 53
      self.log = file
      self.logAll = fileAll
      self.debug = debug
   
      
   def setSOARETRY(self, cache):
      tabela = cache.tabela
      for l in tabela:
         if l[1] == "SOARETRY":
            self.soaRetry = int(l[2])
   

         
      
   
   def run(self):
      i = 0
      while 1:
         fileConfig = open(str(self.log),"a")
         fileConfigAll = open(str(self.logAll),"a")
         
         tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

         tcp.connect((self.ip,self.porta))
         
         print("ZT      ->    " + "Conection for SP: " + '(' +self.ip + ":" + str(self.porta)+ ')')
         #pega o ip do cliente que conectou
         #dom = f"domain: \"{self.domain}\""
         tcp.send(self.domain.encode('utf-8'))


         msg = tcp.recv(1024).decode('utf-8')
         if (self.debug == "D"):
            print("              " + msg)
         par = msg.split(' ')



         data = msg.split(' ')
         print(msg)
         m = "ok: " + str(data[1])      
         tcp.send(m.encode('utf-8'))
         self.cache.freeSP()
         while msg: 
            msg = tcp.recv(1024)
            line = msg.decode('utf-8')
            if (line != ''):
               data = line[:-1].split(' ')
               self.cache.updateCache(data[0], data[1], data[2], data[3], data[4], "SP", data[6], "VALID")
                  #print(line)   # teste para ver se a mensagem está a chegar correta
         
         #print("Transferência de Zona Concluída")
         self.setSOARETRY(self.cache)
         tcp.close()
         
         date = datetime.now()
         time1 = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
         fileConfig.write(time1 + " ZT " + self.ip + ':' + str(self.porta)  +" SS\n")
         fileConfigAll.write(time1 + " ZT " + self.ip + ':' + str(self.porta)  +" SS\n")
         if (self.debug == "D"):
            print("ZT      ->    " + time1 + " ZT " + self.ip + ":" + str(self.porta) + " SS")
         fileConfig.close()
         fileConfigAll.close() 

         
         # valor do intervalo para ele atualizar a sua base de dados
         time.sleep(self.soaRetry)
      
      

