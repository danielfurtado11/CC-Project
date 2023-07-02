from datetime import datetime 
import os
import sys
from Cache import Cache
from parseConfig import parseConfig
from threadSR import mythreadSR

class servidorResolver:
    
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
    
    dd = config.dd
    log = config.lg[0]
    st = config.st
    listST = []
    
    
    # Adiciona a um array todos os ip's dos root servers
    fileST = open(st,"r")
    for line in fileST:
        listST.append(line[:-1])



    if os.path.exists(log):
        fileConfig = open(log,"a")
    else:
        fileConfig = open(log,"x")
        

    fileConfig.write(str(time) + " EV " + "conf-file-read " + txt +'\n')
    
    if (debug == "D"):
        print("LOGS    ->    " + str(time) + " EV conf-file-read " + txt)
        
    fileConfig.close()
    
    
    
    
    sr = mythreadSR(1,porta,cache,log,debug,dd,listST,timeout)
    sr.start()
    
    
    
    
    