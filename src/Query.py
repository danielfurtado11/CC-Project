from Cache import Cache
from parseDB import parseDB


class Query: 

    
    def __init__(self,line,cache):
        split = line.split(';')
        header = split[0].split(',')
        queryInfo = split[1].split(',')
        self.messageID = header[0]
        self.flags = header[1]
        self.responseCode = int(header[2])
        self.nValues = int(header[3]) # PASSAR PARA INT
        self.nAuthorities = int(header[4])
        self.nExtraValues = int(header[5])
        self.name = queryInfo[0]        # domínio passado na query
        self.type = queryInfo[1]
        self.responseValues = []
        self.authoritiesValues = []
        self.extraValues = []
        self.cache = cache
        self.domain = False
        self.bestSuffix = "."
        
        
        
            
            
    def makeQuery(self):

        tabela = self.cache.tabela
        for l in tabela:
            
            if self.name.endswith(l[0]):
                if (self.name != "." and l[0] == "."):
                    continue
                self.domain = True 
                
            string = l[0] + ' ' + l[1] + ' ' + l[2] + ' ' + l[3]
            if l[4] != '-':
                string += ' ' + l[4]  # caso tenha prioridade temos que adicionar à query
            if l[1] == self.type and l[0] == self.name: # tipo = l[1] , name = l[0]
                self.responseValues.append(string)
                self.nValues+=1
                
                                   ##############
            if l[1] == "NS" and self.name.endswith(l[0]) :  # NS = Authorities Values
                if (len(l[0])>len(self.bestSuffix)):
                    self.bestSuffix = l[0]
                    self.authoritiesValues.clear()
                    self.nAuthorities = 0
                self.authoritiesValues.append(string)
                self.nAuthorities+=1
            
        for l in tabela:
            if l[1] == "A":     # if type = "A"
                string = l[0] + ' ' + l[1] + ' ' + l[2] + ' ' + l[3]
                if l[4] != '-':
                    string += ' ' + l[4]
                for x in self.responseValues:
                    parse = x.split(" ")
                    if l[0] == parse[2]:
                        self.extraValues.append(string)
                        self.nExtraValues+=1
                for z in self.authoritiesValues:
                    parse = z.split(" ")
                    #print("A " + parse[2])
                    if l[0] == parse[2]:
                        self.extraValues.append(string)
                        self.nExtraValues+=1
                        
        
        if 'R' in self.flags:
            self.flags = "R+A"
        else:
            self.flags = "A"
        
        if (self.nValues == 0 and self.domain == True):    # caso o domínio do servidor seja zigual ao da query mas não existem valores do que era pretendido
            self.responseCode = 1
        if (self.domain == False):    # caso o domínio do servidor seja diferente do da query
            self.responseCode = 2

        
                
            
    def parseQuery(self):
        array = []
        string1 = str(self.messageID) + ',' + self.flags + ',' + str(self.responseCode) + ',' + str(self.nValues) + ',' + str(self.nAuthorities) + ',' + str(self.nExtraValues) +';'              
        array.append(string1)
        string2 = ""
        for l in self.responseValues:
            string2 += str(l) + ','
        string2 = string2[:-1]
        string2 += ';'
        array.append(string2)
        string3 = "" 
        for l in self.authoritiesValues:
            string3 += str(l) + ','
        string3 = string3[:-1]
        string3 += ';'
        array.append(string3)
        string4 = ""
        for l in self.extraValues:
            string4 += str(l) + ','
        string4 = string4[:-1]
        string4 += ';'
        array.append(string4)
        return array
        

    
        
        
        
    

        
        

class daniel:
    def main():
        cache = Cache()
        parse = parseDB("dbs/grandeguaxinim.db",cache)
        parse.converte()
        for l in cache.tabela:
           print(l)
        x = "5291,Q+R,0,0,0,0;www.grande.guaxinim.,A;"
        query = Query(x,cache)
        query.makeQuery()
        array = query.parseQuery()
        for l in array:
            print(l)
        
        
        
        
    if __name__ == "__main__":
        main()