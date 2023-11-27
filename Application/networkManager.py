import socket
from package import *
import json

class server:
    HOST : str
    PORT : int
    conn : socket.socket
    temp : str
    chkStr : str
    chkStrIndex : int
    chktemp : str

    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.temp = ""
        self.chktemp = ""
        self.chkStr = "ENDCOMMUNICATION"
        self.chkStrIndex = 0


    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(5)
        print('server start at: %s:%s' % (self.HOST, self.PORT))
        print('wait for connection...')
        self.conn, addr = s.accept()
        print('connected by ' + str(addr))            
        s.close()
        pkgChk = 0
        return True
    
    def listenPackage(self):
        try:
            indata = self.conn.recv(1024)
        except:
            print("connection closed")
            return "close"
        
        if(len(indata) == 0):
            print("connection closed")
            return "close"
        receive = indata.decode()
        jsondata = None
        print('recv: ' + receive)
        for t in receive:
            if t == self.chkStr[self.chkStrIndex]:
                self.chkStrIndex += 1
                self.chktemp += t
            else:
                self.temp = self.temp + self.chktemp + t
                self.chktemp = ""
                self.chkStrIndex = 0

            if self.chkStrIndex == len(self.chkStr):
                self.chkStrIndex = 0
                self.chktemp = ""

                jsondata = json.loads(self.temp)
                self.temp = ""
                package = Package(jsondata["ACTION"],jsondata["restaurantRequestName"],jsondata["requestLocation"],jsondata["requestTarget"], jsondata["restaurantData"], jsondata["restaurantNeed"], jsondata["randomNeed"])
                return package
        return None
        #self.packageAnalyze(package)
        #self.conn.close()

    def sendPackage(self, package):
        for restaurant in package.restaurantData:
            restaurant.review = ""
        outdata = (json.dumps(package, default=Package.obj2Json).encode().decode('unicode-escape') + 'ENDCOMMUNICATION')
        print(outdata)
        self.conn.send(outdata.encode('utf-8', 'replace'))


    
    