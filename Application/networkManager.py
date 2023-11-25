import socket
from package import *
import json

class server:
    HOST : str
    PORT : int
    conn : socket.socket
    temp : str

    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.temp = ""


    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(5)
        print('server start at: %s:%s' % (self.HOST, self.PORT))
        print('wait for connection...')
        self.conn, addr = s.accept()
        print('connected by ' + str(addr))            
        s.close()
        return True
    
    def listenPackage(self):
        indata = self.conn.recv(1024)
        if(len(indata) == 0):
            print("connection closed")
            return "close"
        receive = indata.decode()
        jsondata = None
        print('recv: ' + receive)
        for t in receive:
            if t != '#':
                self.temp = self.temp + t
            else:
                jsondata = json.loads(self.temp)
                self.temp = ""
                package = Package(jsondata["ACTION"],jsondata["restaurantRequestName"],jsondata["requestLocation"],jsondata["requestTarget"])
                return package
        return None
        #self.packageAnalyze(package)
        #self.conn.close()

    def sendPackage(self, package):
        outdata = (json.dumps(package, default=Package.obj2Json).encode().decode('unicode-escape') + '#')
        #print(outdata)
        self.conn.send(outdata.encode('utf-8', 'replace'))


    
    