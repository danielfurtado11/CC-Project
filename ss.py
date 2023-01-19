from threadSS import myThreadSS
from Cache import Cache
import sys
from parseConfig import parseConfig
from threadUDP import mythreadUDP
import os
from datetime import datetime

class servidorSecundario:
    
    
    s = len(sys.argv)
    if s == 5:
        txt = sys.argv[1]
        porta = int(sys.argv[2])
        timeout = sys.argv[3]
        debug = sys.argv[4]
    if s == 4:
        txt = sys.argv[1]
        porta = 53
        timeout = int(sys.argv[2])
        debug = sys.argv[3]
        
    
    cache = Cache()
    
    
    
    config = parseConfig(txt)
    config.fileopen()
    
    date = datetime.now()
    time = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
    
    
    domain = config.domain    
    sp = config.sp
    log = config.lg
    fileLocal = log[0]
    fileLogsAll = log[1]
        

 

    if os.path.exists(fileLocal):
         fileConfig = open(fileLocal,"a")
 
    else:
         fileConfig = open(fileLocal,"x")
 
    if os.path.exists(fileLogsAll):
         fileConfigAll = open(fileLogsAll, "a")
 
    else:
         fileConfigAll = open(fileLogsAll,"x")
    
    
    fileConfig.write(str(time) + " EV " + "conf-file-read " + txt +'\n')
    fileConfigAll.write(str(time) + " EV " + "conf-file-read " + txt +'\n')   

 
    if (debug == "D"):
        print("LOGS    ->    " + str(time) + " EV conf-file-read " + txt) 
        print("LOGS    ->    " + str(time) + " EV conf-file-read " + txt)
    
    date = datetime.now()
    time = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
    fileConfig.write(str(time) + " EV log-file-create " + fileLocal + '\n')
    fileConfigAll.write(str(time) + " EV log-file-create " + fileLogsAll + '\n')
    
    if (debug == "D"):
        print("LOGS    ->    " + str(time) + " EV log-file-create " + fileLocal)  
        print("LOGS    ->    " + str(time) + " EV log-file-create " + fileLogsAll)
    
    fileConfig.close()
    fileConfigAll.close()
    
    
    # Prints para debug
    # print("O domínio é: " + domain)
    # print("O SP respetivo é: " + sp)
    
    
    # cria a thread para a transferência de zona
    ss = myThreadSS(1,sp,cache,domain, fileLocal, fileLogsAll, debug)
    ss.start()

    cl = mythreadUDP(2,porta,cache, fileLocal, fileLogsAll, debug)
    cl.start()
    
