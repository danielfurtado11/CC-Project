class Cache:
    
    def __init__(self):
        self.size = 1
        self.posicao = 2
        self.tabela = [["-","-","-","-","-","-","-",1,"FREE"]]

        
        
        
        
    def updateCache(self, nome, tipo, valor, ttl, prio, origem, time, state):
        new = [nome, tipo, valor, ttl, prio, origem, time, self.posicao, state]
        i = 0
        
        if (origem == "OTHERS"):
            for i,linha in enumerate(self.tabela):
                if (nome == linha[0] and tipo == linha[1] and  valor == linha[2] and ttl == linha[3] and prio == linha[4] and linha[5] == "OTHERS"):
                    linha[6] = time
                    self.tabela[i] = linha
                    return
                
                if (nome == linha[0] and tipo == linha[1] and valor == linha[2] and ttl == linha[3] and prio == linha[4] and (linha[5] == 'SP' or linha[5] == 'FILE')):
                    return
            
            
            if(self.cacheFree()):
                for i,linha in enumerate(self.tabela):
                    if (linha[8] == "FREE"):
                        linha = [nome, tipo, valor, ttl, prio, origem, time, linha[7], state]
                        self.tabela[i] = linha
                        return
            else:
                self.tabela.append(new)
                self.size += 1
                self.posicao += 1
        
        
        
        
        else:
            if (self.cacheFree()):
                for i, linha in enumerate(self.tabela):
                    if (linha[8] == "FREE"):
                        self.tabela[i] = [nome, tipo, valor, ttl, prio, origem, time, linha[7], state]
                        return
                
            else:
                self.tabela.append(new)
                self.size += 1
                self.posicao += 1

        
                
    def cacheFree(self):
        for linha in self.tabela:
            if(linha[8] == "FREE"):
                return True
        return False
        
        
        
        
        
        
    def freeCache(self, domain, time):
        
        for i,linha in enumerate(self.tabela):
            if (domain in linha[0] and time > int(linha[3])):
                linha[8] = "FREE"
                self.tabela[i] = linha

    def freeSP(self):
        for i,linha in enumerate(self.tabela):
            if (linha[5] == "SP"):
                linha[8] = "FREE"
                self.tabela[i] = linha

                
                
                 
        
            
            
            
        

        
        
        
        
    
    # MUDAR A CACHE
    def search(self, index, name, type, time):

        if (index == 1):
            array = []
            for linha in self.tabela:
                if (linha[5] == "OTHERS" and time < int(linha[3])):
                    linha = ["-","-","-","-","-","-","-",linha[7],"FREE"]
                if (linha[0] == name and linha[1] == type and time < int(linha[3]) and linha[8] == "VALID"):
                    array.append(linha[7])
            return array

        else:
            for linha in  self.tabela:
                if (linha[5] == "OTHERS" and time < int(linha[3])):
                    linha = ["-","-","-","-","-","-","-",linha[7],"FREE"]
                if (linha[0] == name and linha[1] == type and time < int(linha[3]) and linha[8] == "VALID" and index <= linha[7]):
                    print(linha)
                    return [linha[7]]
        







        
        

    



    