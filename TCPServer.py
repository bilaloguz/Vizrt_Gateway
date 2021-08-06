import socket 
from threading import Thread 
from socketserver import ThreadingMixIn 

class TCPServer:

    def __init__(self, port, onDataReceive):
        self.port = port
        self.onDataReceive = onDataReceive
        self.tcpServer = None
    
    def run(self):
        TCP_IP = '0.0.0.0' 
        TCP_PORT = self.port 
        BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.tcpServer.bind((TCP_IP, TCP_PORT)) 
        threads = [] 
 
        while True: 
            self.tcpServer.listen(4) 
            (conn, (TCP_IP, TCP_PORT)) = self.tcpServer.accept() 
            newthread = ClientThread(TCP_IP, TCP_PORT, conn, self.onDataReceive) 
            newthread.start()

    
    def stop(self):     
        print("TCPServer.stop")
        try:
            self.tcpServer.shutdown()
        except Exception as e:
            print(str(e))
        try:
            self.tcpServer.close()
        except Exception as e:
            print(str(e))

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port, conn, onDataReceive): 
        self.terminated = False
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        self.conn = conn
        self.onDataReceive = onDataReceive


    def run(self): 
        print("TCP client thread started. ID: " + str(self.ident))
        
        while True : 
            readBytes = []
            char = 0
            
            data = self.conn.recv(1)
            if data:
                char = data[0]
            else:
                break
            
            while (char != 0):
                readBytes.append(char)
                data = self.conn.recv(1)
                if data:
                    char = data[0]
                else:
                    char = 0
            
            if len(readBytes) == 0:
                break

            rawData = bytes(readBytes)
            rawString = str(rawData, encoding='utf-8')
            dataToSend = []
            if rawString != "":
                self.onDataReceive(rawString, dataToSend)
                if len(dataToSend)>0 and dataToSend[0]:
                    self.conn.send(bytes(dataToSend[0], encoding="utf-8"))
                    self.conn.send(bytes([0]))
        
        print("TCP client thread stoppped. ID: " + str(self.ident))
