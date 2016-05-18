'''This is a class that hold all the information needed to send and receive things from the server'''
from socket import *
import os

class Connect:
    def __init__(self, ip, port):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((ip, port))
        self.clientSocket.setblocking(False)
        self.bufferSize = 9

    def send(self, message):
        self.clientSocket.send(("SIZE:" + str(len(message)) + ("~" * (4 - len(str(len(message)))))).encode())
        self.clientSocket.send(message.encode())
        #print("sent")

    def receive(self):
        try:
            message = self.clientSocket.recv(self.bufferSize).decode().split(":")
            self.bufferSize = 9
            if message[0] == "SIZE":
                self.bufferSize = int(message[1][:-message[1].count("~")])
            
            else:
                if message[0] == "STOP":
                    self.clientSocket.close()

                return message

        except Exception as error:
            pass

    def close(self):
        self.clientSocket.close()