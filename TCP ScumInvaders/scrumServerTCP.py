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
                numThreads = 0
                while numThreads < len(self.threads):
                    output = self.threads[numThreads].run()
                    if output == "DISCONNECT":
                        self.threads.pop(numThreads)

                    numThreads += 1

        self.connectSocket.close()
        
class clientChannel(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.bufferSize = 9
        self.loggedIn = False
        
    def run(self):
        try:
            data = self.client.recv(self.bufferSize)
            self.bufferSize = 9
            read = data.decode()
            readList = read.split(":")
            if readList[0] == "SIZE":
##                print(readList[1][:-readList[1].count("~")])
                self.bufferSize = int(readList[1][:-readList[1].count("~")])
##                print(self.bufferSize)

            else:
                if readList[0] == "LOG":
                    self.checkLog(readList[1], readList[2])

                elif readList[0] == "CHECKLOG":
                    if self.loggedIn:
                        self.send("Success")

                    else:
                        self.send("Invalid Password")

                elif readList[0] == "STOP":
                    self.send(readList[0])
                    print(self.address, "DISCONNECTED")
                    self.client.close()
                    return "Disconnect"

##                self.send(read[1].encode())
        except:
            pass

    def send(self, message):
        self.client.send(("SIZE:" + str(len(message)) + ("~" * (4 - len(str(len(message)))))).encode())
        self.client.send(message.encode())

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
                    self.loggedIn = True
                    self.send("Success")
                    print("Success")
                else:
                    self.send("Invalid Password")
                    print("Invalid Password")

        '''hashing password'''
        if un == "":
            print("Creating username.")
            hashed = hashlib.md5()
            hashed.update((salt + password).encode())
            hashedPassword = str(hashed.hexdigest())
            tups = (username, hashedPassword)
            c.execute("INSERT INTO logins VALUES (?,?)", (username, hashedPassword))
            self.loggedIn = True
            self.send("Success")
            print("Created username.")
            connection.commit()
        c.execute('SELECT * FROM logins')
        data = c.fetchall()
        print(data)
if __name__ == "__main__":
    port = input("Port #: ")
    socket = TCP_Server("", int(port))
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
