from parseDB import parseDB
from Cache import Cache
from parseConfig import parseConfig
from threadSP import myThreadSP
from threadUDP import mythreadUDP
import sys
import os
from datetime import datetime


class Server:

    
    
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
        
    
    # definido por defeito    
    bufferSize = 1024
        
    # faz o parse do ficheiro de configuração
    config = parseConfig(txt)
    config.fileopen()
    date = datetime.now()
    time = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]

    
    domain = config.domain
    db = config.database
    ss = config.secondary
    dd = config.dd
    log = config.lg
    st = config.lg
    

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
    

    fileConfig.write(str(time) + " EV " + "log-file-create " + fileLocal + '\n')
    fileConfigAll.write(str(time) + " EV " + "log-file-create " + fileLocal + '\n')
    
    if (debug == "D"):
        print("LOGS    ->    " + str(time) + " EV log-file-create " + fileLocal)    
        print("LOGS    ->    " + str(time) + " EV log-file-create " + fileLogsAll    )
    
    # faz o parse da DB e cria a cache
    cache = Cache()
    parse = parseDB(db,cache)
    parse.converte()
    # transfere o parse da DB para a cache

    
    date = datetime.now()
    time = date.strftime("%d:%m:%Y.%H:%M:%S:%f")[:-3]
    
    fileConfig.write(str(time) + " EV " + "db-file-read " + db + '\n')
    fileConfigAll.write(str(time) + " EV " + "db-file-read " + db + '\n')

    if (debug == "D"):
        print("LOGS    ->    " + str(time) + " EV db-file-read " + db)
    
    
    
    # for l in cache.tabela:         # teste para ver como está a cache
    #     print(l)
    
    # abc = cache.search(1,"grande.guaxinim.","NS",1)
    # print(abc)
    
    
    
    
    fileConfig.close()
    fileConfigAll.close()
    

    # inicia a thread da transferência de zona
    ss = myThreadSP(1,cache, fileLocal, fileLogsAll, porta,domain,debug)
    ss.start()

    # inicia a thread para comunicar com os clientes
    cl = mythreadUDP(2,porta,cache, fileLocal, fileLogsAll, debug)
    cl.start()
    
