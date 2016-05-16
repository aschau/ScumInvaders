from socket import *

class TCP_Client:
    def __init__(self):
        self.clientServer = socket(AF_INET, SOCK_STREAM)
        self.running = True
    def run(self, port):
        ip = input("Input IP: ")
        self.clientServer.connect((ip, port))
    def send(self):
        while self.running:
            try:
                data = self.clientServer.recv(1024)
                if data:
                    read = data.decode().split(":")
                    if read[0] == "STOP":
                        self.running = False
                        self.close()
                    else:
                        print(read[0])
                else:
                    message = input("Send a message: ")
                    self.clientServer.send(message.encode())
            except:
                print("Something failed.")
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
print("You have left the server.")
    
