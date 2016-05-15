from socket import *
import sqlite3
import hashlib
import os
import threading

class TCP_Server:
    def __init__(self, host, port):
        self.host = ''
        self.port = 12000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(4)
        #self.serverSocket.settimeout(0.0)
        self.connectSocket = None
        self.clientAddresses = {}
        self.threads = []
##    def setUp(self):
##        try:
##            self.serverSocket = socket(AF_INET, SOCK_STREAM)
##            self.serverSocket.bind((self.host, self.port))
##            self.serverSocket.listen(self.backLog)
##        except:
##            if self.serverSocket:
##                self.serverSocket.close()
##            print("Socket coulnd't be opened.")
        ##                connectSocket, clientID = self.serverSocket.accept()
        ##                print("It accepted.")
        ##                connectSocket.send("You have connected.".encode()) 
        ##                message = connectSocket.recv(1024)
        ##                read = message.decode().split(":")
        ##                print(read)
        ##                if read[0] == "LOG":
        ##                    self.checkLog(read[1], read[2], clientID)
        ##                elif read[0] == "TALK":
        ##                    connectSocket.send(read[1].encode())
        ##                elif read[0] == "STOP":
        ##                    connectSocket.send(read[0].encode())
        ##                    break
        ##                else:
        ##                    connectSocket.send("Send again".encode())

    def run(self):
        #self.setUp()
        while True:
            #conn, clientID = self.serverSocket.accept()
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
    def run(self):
        try:
            while True:
                data = self.client.recv(200)
                if not data: break
                read = data.decode().split(":")
                print(read)
                if read[0] == "LOG":
                    self.checkLog(read[1], read[2])
                elif read[0] == "TALK":
                    self.client.send(read[1].encode())
                elif read[0] == "STOP":
                    self.client.send(read[0].encode())
                    break
                else:
                    self.client.send("Send again".encode())
        finally:
            self.client.close()
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
    socket = TCP_Server("", 12000)
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
