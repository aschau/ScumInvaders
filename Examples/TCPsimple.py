#simpler server TCP?
from socket import *
import threading

class TCP_Server:
    def __init__(self, host,  port):
        self.host = host
        self.port = port
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.connectedSockets = []
        serverPortTaken = True
        while serverPortTaken:
            try:
                self.serverSocket.bind((host, port))
                serverPortTaken = False
                
            except:
                self.port = self.port = self.port + 1
                print(self.port) 
        self.serverSocket.listen(4)
    def run(self):
        while True:
            try:
                connectSocket, clientID = self.serverSocket.accept()
                print("It's not accepting.")
                if connectSocket:
                    if len(self.connectedSockets) < 4:
                        self.connectedSockets.append((connectSocket,clientID[1]))
                        print("Added socket.")
                connectSocket.send("You have connected.".encode())
                while True:
                    try:
                        print("asking for data")
                        data = connectSocket.recv(200)
                        print("Received data")
                        if data:
                            print("reading data?")
                            read = data.decode().split(":")
                            print(read)
                            if read[0] == "TALK":
                                connectSocket.send("WHY YOU NO WORK".encode())
                                self.broadcast(read[1])
                            elif read[0] == "STOP":
                                connectSocket.send(read[0].encode())
                                break
                            else:
                                connectSocket.send("Send again".encode())
                    except:
                        pass
                connectSocket.close()
            except:
                print("The connection failed.")
    def broadcast(self, msg):
        for i in self.connectedSockets:
            print("Is this sending")
            i.send(msg.encode())
if __name__ == "__main__":
    socket = TCP_Server("", 9000)
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
