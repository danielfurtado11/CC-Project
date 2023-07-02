import sys


class parseConfig: 


    def __init__(self, filename):
        self.m_name = "configs/" + str(filename)
        self.domain = ""
        self.database = ""
        self.secondary = []
        self.dd = {}
        self.lg = []
        self.st = ""
        self.sp = ""



    def fileopen(self):
        
        file = open(self.m_name, 'r')
        read = file.readlines()
        completas = []
        
        for line in read:

            if (line[0] != "#" and line != "\n"):
                line = line[:-1]
                completas.append(line)
                data = line.split()

                
                match data[1]:
                    case "DB":
                        self.database = data[2]
                    case "SS": 
                        self.secondary.append(data[2])
                    case "DD":
                        if (data[0] not in self.dd):
                            self.dd[data[0]] = data[2]
                    case "LG":
                        if (data[0]) != "all":
                            self.domain = data[0]
                        self.lg.append(data[2])
                    case "ST":
                        self.st = data[2]
                    case "SP":
                        self.sp = data[2]



        file.close()

        


