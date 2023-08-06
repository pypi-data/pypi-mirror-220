import socket
class NrcDevice:
    def __init__(self,config):
        (ip,port,username,password)=config
        self.ip=ip
        self.port=port
        self.username=username
        self.password=password
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def disconnect(self):
        self.socket.close()

    def send(self,command):
        try:
            self.socket.sendall(str(command).encode())
            response = self.socket.recv(1024).decode()
            return response
        except:
            self.socket.close()

    def login(self):
        response=self.send(self.username+":"+self.password)
        return response=="Successful Login"

    def relayContact(self,relayCode,delay_ms=None):
        cmd="%RCT"+str(relayCode)
        if(delay_ms!=None):
            cmd+=":"+str(delay_ms)
        self.send(cmd)

    def relayOn(self,relayCode):
        self.send("%RON"+str(relayCode))

    def relayOff(self,relayCode):
        self.send("%ROF"+str(relayCode))

    def getBit(self,num, index):
        return (num >> index) & 1


    def getRelaysValues(self):
        response=self.send("%RST")
        if response.endswith("h"):
            return int(response[:-1], 16)
        raise Exception("Invalid Response! Response must end with 'h'")

    def getRelayValue(self,relayCode):
        return self.getBit(self.getRelaysValues(),relayCode-1)

    def getSwInputsValues(self):
        response=self.send("%ISW")
        if(response=="Error"):
            raise Exception("Device not support feature!")
        if response.endswith("h"):
            return int(response[:-1], 16)
        raise Exception("Invalid Response! Response must end with 'h'")

    def getSwInputValue(self,inputCode):
        return self.getBit(self.getSwInputsValues(),inputCode-1)

    def getHvInputsValues(self):
        response=self.send("%IHV")
        if(response=="Error"):
            raise Exception("Device not support feature!")
        if response.endswith("h"):
            return int(response[:-1], 16)
        raise Exception("Invalid Response! Response must end with 'h'")

    def getHvInputValue(self,inputCode):
        return self.getBit(self.getHvInputsValues(),inputCode-1)