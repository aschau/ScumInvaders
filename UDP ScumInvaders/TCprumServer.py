from socket import *
import sqlite3
import json
import random
from datetime import datetime
from TClientServer import clientChannel

class TCP_Socket:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.serverSocket = socket(AF_INET, SOCK_STREAM)
            self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            serverPortTaken = True
            while serverPortTaken:
                try:
                    self.serverSocket.bind((host, port))
                    serverPortTaken = False
                except:
                    self.port += 1
                    print(self.port)
            self.serverSocket.listen(4)
            self.connectSocket = None
            print('The TCP server is ready to receive')
            print(gethostbyname(gethostname()))
            '''a list of connections with different clients'''
            self.threads = []
            #self.serverPort = port #can be any number > 1024 cuz otherwise reserved
            self.clientAddress = {}
            self.players = 0
            self.rooms = []
            self.roomIPList = {}
            self.gameUpdates = {}
            self.gameGridTypes = {}
            self.gameGrids = {}
            random.seed(datetime.now())
            #serverSocket.listen(4) #denotes the number of clients can queue
            #it binds the serverSocket to port number specified in serverPort variable.
            #then when anybody sends anything to server IP address and serverPort the serverSocket will get it.

        def run(self):
            while True:
                self.connectSocket, clientID = self.serverSocket.accept()
                print("...connected from: ", clientID)
                conSock = clientChannel(self.connectSocket, clientID[0])
                conSock.run()
                self.threads.append(conSock)
            self.connectSocket.close()
            for c in self.threads:
                c.join()

if __name__ == "__main__":
    socket = TCP_Socket('0.0.0.0', 9000)
    socket.run()
    socket.close
