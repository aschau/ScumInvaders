from socket import *

class TCP_Client:
    def __init__(self):
        self.clientServer = socket(AF_INET, SOCK_STREAM)
        self.running = True
        self.bufferSize = 9
    def run(self, port):
        ip = input("Input IP: ")
        self.clientServer.connect((ip, port))
    def send(self):
        message = input("Send a message: ")
        self.clientServer.send(message.encode())
        data = self.clientServer.recv(self.bufferSize)
        if data:
            data = data.decode()
            print(data)
            if "SIZE" in data:
                message = data[5:]
                print(message)
                size = data.count("~")
                message = message[:-size]
                print(message)
                self.bufferSize = int(message)
            else:
                self.bufferSize = 9
                recvMessage = data.split(":")
                if recvMessage[0] == "STOP":
                    self.running = False
                    self.close()
                else:
                    print(recvMessage)
    def close(self):
        self.clientServer.close()
##if __name__ == "__main__":
##    socket = TCP_Client()
##    socket.run(12000)
##    while socket.running == True:
##        socket.send()
##    print("The server has closed")
socket = TCP_Client()
socket.run(9000)
while socket.running == True:
    socket.send()
print("The server has closed")
    
