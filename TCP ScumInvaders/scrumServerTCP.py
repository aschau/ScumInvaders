from socket import *
import sqlite3
import hashlib
import os
import threading
import json
import random

class TCP_Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serverSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        self.serverSocket.setblocking(False)
        serverPortTaken = True
        while serverPortTaken:
            try:
                self.serverSocket.bind((host, port))
                serverPortTaken = False
                
            except:
                self.port = self.port + 1
                print(self.port)
        self.serverSocket.listen(4)
        self.connectSocket = None
        self.threads = []
        self.rooms = {}
        self.gameGrids = {}

    def setGrid(self, host):
        self.gameGrids[host] = {}

        typeList = []
        posList = []
        for row in range(5):
            typeList.append([])
            for column in range(10):
                typeList[row].append(random.randint(1, 100))
                posList.append([32 + (column * 96), (row * 64) - 5 * 64])
                
        self.gameGrids[host]["TYPES"] = typeList
        self.gameGrids[host]["POS"] = posList
        
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
                    message = self.threads[numThreads].run()
                    if message != None:
                        output = message.split(":")
                        if output[0] == "DISCONNECT":
                            self.threads.pop(numThreads)

                        elif output[0] == "CREATE":
                            self.rooms[self.threads[numThreads].username] = {}
                            self.rooms[self.threads[numThreads].username][self.threads[numThreads].username] = [False, "Room"]

                        elif output[0] == "JOIN":
                            self.rooms[output[1]][self.threads[numThreads].username] = [False, "Room"]

                        elif output[0] == "LEAVE ROOM":
                            del self.rooms[self.threads[numThreads].room][self.threads[numThreads].username]
                            
                            if len(self.rooms[self.threads[numThreads].room]) == 0:
                                del self.rooms[self.threads[numThreads].room]

                            else:
                                if self.threads[numThreads].username in self.rooms:
                                    room = list(self.rooms[self.threads[numThreads].room].items())
                                    del self.rooms[self.threads[numThreads].room]
                                    self.rooms[room[0][0]] = dict(room)
##                                    print(room[0][0])

                                    for thread in self.threads:
                                        if thread.room == self.threads[numThreads].room and thread.username != self.threads[numThreads].username:
                                            thread.room = room[0][0]
                                            thread.send("ROOM:" + room[0][0])

                                    self.threads[numThreads].room = None                                    
                            
                        elif output[0] == "READY":
                            self.rooms[self.threads[numThreads].room][self.threads[numThreads].username][0] = not self.rooms[self.threads[numThreads].room][self.threads[numThreads].username][0]

                        elif output[0] == "START":
                            self.setGrid(self.threads[numThreads].room)
                            data = json.dumps(list(self.rooms[self.threads[numThreads].username].keys()))
                            data2 = json.dumps(self.gameGrids[self.threads[numThreads].room])
                            for thread in self.threads:
                                if thread.room == self.threads[numThreads].room:
                                    thread.send("START:" + data)
                                    thread.send("GRID:"+data2)
                                    self.rooms[thread.room][thread.username][0] = False
                                    self.rooms[thread.room][thread.username][1] = "Game"

                            for thread in self.threads:
                                if thread.room == self.threads[numThreads].room:
                                    thread.send("GAMESTART")

                        elif output[0] == "GETGRID":
                            data = json.dumps(self.gameGrids[self.threads[numThreads].room])
                            self.threads[numThreads].send("GRID:"+data)

                        elif output[0] == "NEXTLEVEL":
                            ready = True
                            self.rooms[self.threads[numThreads].room][self.threads[numThreads].username][0] = True
                            for player in self.rooms[self.threads[numThreads].room].values():
                                if player == [False, "Game"]:
                                    print("CHECK", self.threads[numThreads].username)
                                    ready = False

                            if ready:
                                print("NEXTLEVEL FINALLY")
                                self.setGrid(self.threads[numThreads].room)
                                data = json.dumps(self.gameGrids[self.threads[numThreads].room])
                                for thread in self.threads:
                                    if thread.room == self.threads[numThreads].room:
                                        thread.send("GRID:" + data)
                                        self.rooms[thread.room][thread.username][0] = False

                                for thread in self.threads:
                                    if thread.room == self.threads[numThreads].room:
                                        thread.send("GAMESTART")

                                print("FINISHED NEXTLEVEL")

                        elif output[0] == "REFRESH":
                            data = json.dumps(self.rooms)
                            self.threads[numThreads].send("Lobby:"+data)
##                            self.threads[numThreads].send("CHAT:Server: "+str(random.randint(1, 100)))

                        elif output[0] == "RETURN":
                            self.rooms[self.threads[numThreads].room][self.threads[numThreads].username][1] = "Room"

                        elif output[0] == "STOP":
                            self.threads.pop(numThreads)
                        
                        else:
                            for thread in self.threads:
                                if thread.username != self.threads[numThreads].username and thread.room == self.threads[numThreads].room:
                                    thread.send(message)
                            
                    numThreads += 1

        self.connectSocket.close()
        
class clientChannel(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.username = None
        self.bufferSize = 9
        self.loggedIn = False
        self.room = None
        
    def run(self):
        try:
            data = self.client.recv(self.bufferSize)
            self.bufferSize = 9
            read = data.decode()
            readList = read.split(":")
            if readList[0] == "SIZE":
                self.bufferSize = int(readList[1][:-readList[1].count("~")])

            else:
                if readList[0] == "LOG":
                    self.checkLog(readList[1], readList[2])

                elif readList[0] == "CHECKLOG":
                    if self.loggedIn:
                        self.send("Success")

                    else:
                        self.send("Invalid Password")

                elif readList[0] == "CREATE":
                        self.room = self.username
                        return readList[0]

                elif readList[0] == "JOIN":
                        self.room = readList[1]
                        return read

                elif readList[0] == "STOP":
                    self.send(readList[0])
                    print(self.address, "DISCONNECTED")
                    self.client.close()
                    return "Disconnect"

                else:
                    return read

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
##        print("This is the data:")
##        print(data)
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
                    self.username = username
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
##        print(data)
if __name__ == "__main__":
    port = input("Port #: ")
    socket = TCP_Server("", int(port))
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
