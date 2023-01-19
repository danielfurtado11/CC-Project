import socket



class srConnect:
    
    def __init__(self,ips,message,cache,timeout):
        self.ips = ips
        self.message = message
        self.cache = cache
        self.timeout = timeout
        
    
    def connectTo(self):
        respostaQuery = []
        for ip in self.ips:

            ipS = ip.split((':'))
            ip = ipS[0]
            if len(ipS)>1:
                porta = ipS[1]
            else:
                porta = 53
    
    
            bytesToSend = str.encode(self.message)
            serverAddressPort = (ip, int(porta))
            bufferSize = 1024
            UDPClientSocket = socket.socket(family=socket.AF_INET, type= socket.SOCK_DGRAM)
            UDPClientSocket.settimeout(self.timeout)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            
            try:
                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                cabecalho = msgFromServer[0].decode('utf-8')

                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                responseValues = msgFromServer[0].decode('utf-8')
                #print(responseValues)

                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                authoritiesValues = msgFromServer[0].decode('utf-8')
                #print(authoritiesValues)

                msgFromServer = UDPClientSocket.recvfrom(bufferSize)
                extraValues = msgFromServer[0].decode('utf-8')
                #print(extraValues)


                respostaQuery.extend([cabecalho,responseValues,authoritiesValues,extraValues])
                #print(respostaQuery)

                UDPClientSocket.close()
                return respostaQuery
            
            except socket.timeout:
                continue
        else:
            print("EXCEPTION: Nenhum servidor está ativo.")
            return ["EXCEPTION: Nenhum servidor está ativo."]


                
