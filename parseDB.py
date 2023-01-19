from Cache import Cache

import sys
from time import perf_counter

class parseDB:
    
    def __init__(self,filename, cache):
        self.f = filename
        self.nome = "-"
        self.tipo = "-"
        self.valor = "-"
        self.TTL  = "-"
        self.prioridade = "-"
        self.origem = "FILE"
        self.timestamp = 0.0
        self.index = 0
        self.status = "VALID"
        self.cache = cache
        self.domain = "---"

# nome, tipo, valor, TTL, prioridade, origem de entrada, timestamp, index, status

    def converte(self):
        start = perf_counter()

        with open(self.f,"r") as file: # Forma mais segura de abrir ficheiros
            macros = {}

            for linha in file:
                if linha[0] != '#' and linha[0] != '\n': 
                    
                    data = linha.split(' ') # Separa por espaços
                    
                    if data[1]== "DEFAULT" and data[0] == "@":
                        self.domain = data[2][:-1]
                        
                    
                    if data[1]=="DEFAULT":
                        macros[data[0]] = data[2][:-1] # Adicionar ao dictionary o macro
                        self.nome = data[0]
                        self.tipo = data[1]
                        self.valor = data[2][:-1]
                        stop = perf_counter()
                        self.timestamp = (stop-start)
                        self.cache.updateCache(self.nome,self.tipo, self.valor, self.TTL, self.prioridade, self.origem, str(self.timestamp), self.status)
                        
                    else:
                        l = linha
                        for key in macros: # Verificar se é possível trocar na string por qualquer tipo de macro 
                            l = l.replace(key, macros[key])
                            
                        l = l[:-1] # Necessário para tirar o "\n" no final da string
                        data = l.split(' ')
                        
                        self.tipo = data[1]
                        if (self.tipo) == "A" and self.domain != ".":
                            self.nome = data[0] + "." +  self.domain
                        elif (self.tipo) == "A" and self.domain == ".":
                            self.nome = data[0] + self.domain
                        else: 
                            self.nome = data[0]
                        length = len(data)
                        self.valor = data[2]
                        if (length>3):
                            self.TTL = data[3]
                        if (length>4):
                            self.prioridade = data[4]
                        stop = perf_counter()
                        self.timestamp = (stop-start)
                        self.cache.updateCache(self.nome, self.tipo, self.valor, self.TTL, self.prioridade, self.origem, str(self.timestamp), self.status)
                        self.prioridade = "-"

                



def main(): 
    cache = Cache()
    #cache.updateCache('sp123','CNAME','ns1','86400','-','OTHERS','33','VALID') # TESTE
    #cache.updateCache('sp123','CNAME','ns1','86400','-','OTHERS','3333','VALID') # TESTE
    parse = parseDB("dbs/database.db",cache)
    parse.converte()
    #cache.freeCache("example.com.",333333333)
    #parse.converte()
    for l in cache.tabela:
        print(l)

    
if __name__ == "__main__":
    main()
    

