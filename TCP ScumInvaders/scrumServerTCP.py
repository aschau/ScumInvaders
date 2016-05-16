from socket import *
import sqlite3
import hashlib
import os
import threading

class TCP_Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverSocket.setblocking(False)
        serverPortTaken = True
        while serverPortTaken:
            try:
                self.serverSocket.bind((host, port))
                serverPortTaken = False
                
            except:
                self.port = self.port = self.port + 1
                print(self.port)
        self.serverSocket.listen(4)
        self.connectSocket = None
        self.clientAddresses = {}
        self.threads = []

    def run(self):
        #self.setUp()
        while True:
            try:
                self.connectSocket, clientID = self.serverSocket.accept()
                print("...connected from: ", clientID)
                conSock = clientChannel(self.connectSocket, clientID[0])
                self.threads.append(conSock)
            except:
                for c in self.threads:
                    output = c.run()
                    if output != None:
                        for c in self.threads:
                            c.client.send(output.encode())

        self.connectSocket.close()
        
class clientChannel(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
    def run(self):
        try:
            data = self.client.recv(200)
            read = data.decode().split(":")
            if read[0] == "LOG":
                self.checkLog(read[1], read[2])

            elif read[0] == "STOP":
                self.client.send(read[0].encode())
            else:
                return read[0]
##                self.client.send(read[1].encode())
        except:
            pass

    def checkLog(self,username, password):
        connected = None
        connection = sqlite3.connect("testData.db")
        c = connection.cursor()
        connection.execute('''CREATE TABLE IF NOT EXISTS logins (user TEXT, pass TEXT)''')
        tups = [(username, password)]
        c.execute('SELECT * FROM logins')
        data = c.fetchall()
        print("This is the data:")
        print(data)
        un = ""
        salt = "thisissalty" #for hashing
        for i in data:
            if i[0] == username:
                un = username
                print("This username exists")
                hashed = hashlib.md5()
                hashed.update((salt + password).encode())
                if hashed.hexdigest() == i[1]:
                    self.client.send("Login success.".encode())
                else:
                    self.client.send("Login failed.".encode())
        '''hashing password'''
        if un == "":
            print("Creating username.")
            hashed = hashlib.md5()
            hashed.update((salt + password).encode())
            hashedPassword = str(hashed.hexdigest())
            tups = (username, hashedPassword)
            c.execute("INSERT INTO logins VALUES (?,?)", (username, hashedPassword))
            self.client.send("Username created.".encode())
            print("Created username.")
            connection.commit()
        c.execute('SELECT * FROM logins')
        data = c.fetchall()
        print(data)
if __name__ == "__main__":
    socket = TCP_Server("", 9000)
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
