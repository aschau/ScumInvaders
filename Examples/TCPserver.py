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
        self.connection = None
        self.c = None

    def run(self):
        #self.setUp()
        while True:
            self.connectSocket, clientID = self.serverSocket.accept()
            print("...connected from: ", clientID)
            conSock = clientChannel(self.connectSocket, clientID[0])
            conSock.run()
            self.threads.append(conSock)
        self.connectSocket.close()
        for c in self.threads:
            c.join()

class clientChannel(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.username = ''
        self.running = True
    def run(self):
        try:
            while self.running:
                data = self.client.recv(200)
                if not data: break
                read = data.decode().split(":")
                print(read)
                if read[0] == "LOG":
                    self.checkLog(read[1], read[2])
                elif read[0] == "TALK":
                    self.client.send(read[1].encode())
                elif read[0] == "INPUT":
                    self.insertScore(read[1])
                    self.client.send("Score recorded".encode())
                elif read[0] == "STOP":
                    self.client.send(read[0].encode())
                    self.running = False
                else:
                    self.client.send("Send again".encode())
        finally:
            self.client.close()
        self.client.close()
    def insertScore(self, score):
        self.connection.execute('''UPDATE logins SET score=? WHERE user=?''', (score, self.username))
        self.connection.commit()
        self.c.execute('SELECT * FROM logins')
        data = self.c.fetchall()
        print("The data:")
        print(data)
        
    def checkLog(self,username, password):
        connected = None
        self.connection = sqlite3.connect("newData.db")
        self.c = self.connection.cursor()
        self.connection.execute('''CREATE TABLE IF NOT EXISTS logins (user TEXT, pass TEXT, score TEXT)''')
        self.username = username
        tups = [(username, password)]
        self.c.execute('SELECT * FROM logins')
        data = self.c.fetchall()
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
            self.c.execute("INSERT INTO logins VALUES (?,?, '0')", (username, hashedPassword))
            self.client.send("Username created.".encode())
            print("Created username.")
            self.connection.commit()
        self.connection.execute('SELECT * FROM logins')
        data = self.c.fetchall()
        print(data)
if __name__ == "__main__":
    socket = TCP_Server("", 9000)
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
