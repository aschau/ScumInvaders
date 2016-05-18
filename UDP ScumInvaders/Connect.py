'''This is a class that hold all the information needed to send and receive things from the server'''
from socket import *

class Connect:
    def __init__(self):
        self.serverName = '0.0.0.0'
        self.port = 12000
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
    def send(self,message):
        self.clientSocket.sendto((message).encode(), (self.serverName, self.port))