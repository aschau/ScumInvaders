from socket import *
import sqlite3
import json
import random
from datetime import datetime
import time


class Socket:
        def __init__(self, host, port):
                #self.serverPort = port #can be any number > 1024 cuz otherwise reserved
                self.serverSocket = socket(AF_INET, SOCK_DGRAM)
                self.serverSocket.bind((host, port))
                self.serverSocket.settimeout(0.0)
                self.clientAddress = {}
                self.players = 0
                self.rooms = []
                self.roomIPList = {}
                self.gameUpdates = {}
                self.gameGridTypes = {}
                self.gameGrids = {}
                self.offsets = {} # username:[serverclientoffset, clientserveroffset]
                self.serversentcheck = False #maybe loss of packets, keep sending
                self.clientoffsetcheck = False
                self.serverreceivecheck = False
                random.seed(datetime.now())
                #serverSocket.listen(4) #denotes the number of clients can queue
                #it binds the serverSocket to port number specified in serverPort variable.
                #then when anybody sends anything to server IP address and serverPort the serverSocket will get it.

        print('The UDP server is ready to receive')
        print(gethostbyname(gethostname()))
        def run(self):
                while 1:
                        try:
                                message, clientID = self.serverSocket.recvfrom(2048) #2048 is bytes of data to be received
                                #when something is recieved through serverSocket, the data will be stored in message.
                                #Also the client IP and port will be extracted and stored in variable clientAddress.
                                #recvfrom is specific to D_GRAMS foor UDP
                                #decodes the message
                                if clientID not in self.offsets: #appends clientID as key if not in dictionary already
                                        self.offsets[clientID] = [] #empty list
        
                                serverreceivetime = time.time() #for offset calculation
                                modMessage = message.decode()
##                                print(modMessage)
                                read = modMessage.split(":")
        ##                        if read[0] == "TALK":
        ##                                for i in self.clientAddress.values():
        ##                                        self.serverSocket.sendto((read[1] + ": " + read[2]).encode(), i)
                                if 'serverclientoffset' in read:
                                        self.serversentcheck = True
                                        self.clientoffsetcheck = True
                                        print('server received message')
                                        if len(self.offsets[clientID]) == 0: #if values has empty list
                                                self.offsets[clientID] = [read[read.index('serverclientoffset') + 1]]
                                        #finds the index (+1) of where the the offset value is in the message
                                if 'clientsendtime' in read:
                                        if len(self.offsets[clientID]) == 1: #has s->c offset in value list
                                                self.serverreceivecheck = True
                                                clientsendtime = read[read.index('clientsendtime') + 1] #don't assume timestamp is last
                                                clientserveroffset = abs(double(serverreceivetime) - double(clientsendtime)) #in case it's the otherway and is negative
                                                self.offsets[clientID].append(clientserveroffset) #sets second value of tuple client to server offset
                                
                                if read[0] == "LOG":
                                        self.checkLog(read[1], read[2], clientID)

                                if read[0] == "CREATE":
                                        self.rooms.append({})
                                        self.gameUpdates[self.clientAddress[clientID]] = []
                                        self.rooms[-1][str(self.clientAddress[clientID])] = False
                                        self.rooms[-1]["HOST"] = self.clientAddress[clientID]
                                        self.roomIPList[self.clientAddress[clientID]] = [clientID]

                                if read[0] == "JOIN":
                                    for room in self.rooms:
                                        if room["HOST"] == read[1]:
                                            room[str(self.clientAddress[clientID])] = False
                                            self.roomIPList[read[1]].append(clientID)
                                            
                                if read[0] == "REFRESH":
                                        data = json.dumps(self.rooms)
                                        self.serverSocket.sendto(("Lobby:"+data).encode(), clientID)
                                        
                                if read[0] == "READY":
                                        for room in self.rooms:
                                                if room["HOST"] == read[1]:
                                                        room[self.clientAddress[clientID]] = not room[self.clientAddress[clientID]]     
                                if read[0] == "START":
                                        for room in self.rooms:
                                                if room["HOST"] == read[1]:
                                                        for username in room.keys():
                                                                if username != "HOST":
                                                                        room[username] = False

                                                        data = json.dumps(list(room.keys()))
                                                        for client in self.roomIPList[read[1]]:
                                                                self.serverSocket.sendto(("Start:" + data).encode(), client)
                                if read[0] == "LEAVE ROOM":
                                         for room in self.rooms:
                                                 if room["HOST"] == read[1]:
                                                         del room[self.clientAddress[clientID]]
                                                         self.roomIPList[read[1]].pop(self.roomIPList[read[1]].index(clientID))
                                                         if self.clientAddress[clientID] == room["HOST"]:
                                                                 room["HOST"] = list(room.keys())[0]
        ##                              deleting rooms with no one left inside
                                         roomNum = 0
                                         while roomNum < len(self.rooms):
                                             if len(self.rooms[roomNum]) == 1:
                                                 self.rooms.pop(roomNum)
                                                 del self.gameUpdates[read[1]]
                                        
                                if read[0] == "END":
                                        break
                                
##                                if read[0] == "RECEIVE":
##                                        if len(self.gameUpdates[read[1]]) > 0:
##                                                event = self.gameUpdates[read[1]].pop(0)
##                                                for room in self.rooms:
##                                                        if room["HOST"] == read[1]:
##                                                                for client in self.roomIPList[read[1]]:
##                                                                        self.serverSocket.sendto(event.encode(), client)
                                if read[0] == "HIT":
                                        for client in self.roomIPList[read[1]]:
                                                self.serverSocket.sendto(message, client)

                                
                                if read[0] == "SETGRID":
                                        setRNums = ""
                                        for row in range(int(read[2])):
                                                for column in range(int(read[3])):
                                                        setRNums += str(random.randint(1, 100)) + ":"

                                        self.gameGridTypes[read[1]] = setRNums

                                if read[0] == "GETGRIDTYPES":
                                        if read[1] in self.gameGridTypes.keys():
                                                self.serverSocket.sendto(("GRID:" + self.gameGridTypes[read[1]]).encode(), clientID)

##                                if read[0] == "ENEMYGRID":
##                                        print("ENEMYGRID")
##                                        self.gameGrids[read[1]] = read[2]
##                                        print("GG?")
##                                        for client in self.roomIPList[read[1]]:
##                                                self.serverSocket.sendto(("ENEMYGRID:" + read[2]).encode(), client)
##                                                print("TROOLOLOL")
                                
                                if read[0] == "GAMEREADY":
                                        for room in self.rooms:
                                                if room["HOST"] == read[1]:
                                                        room[self.clientAddress[clientID]] = True
                                                        self.serverSocket.sendto("GAMEREADY".encode(), clientID)
                                                        
                                if read[0] == "GETGAMESTART":
                                        for room in self.rooms:
                                                if room["HOST"] == read[1]:
                                                        if False not in room.values():
                                                                for client in self.roomIPList[read[1]]:
                                                                        self.serverSocket.sendto("GAMESTART".encode(), client)
                                 
                                if read[0] == "MOV":
                                    self.gameUpdates[read[1]].append(read[0] + ":" + read[2]+":"+read[3])

                                if read[0] == "SHOOT":
                                    self.gameUpdates[read[1]].append(read[0] + ":" + read[2] + ":" + read[3] + ":" + read[4])
                                if read[0] == "SCORE":
                                    '''This function does not accomodate for multiple hosts and rooms yet'''
                                    print("I received score")
                                    self.score(self.clientAddress[clientID], str(read[2]))
                                    #self.serverSocket.sendto(("SCORE:" + str(self.clientAddress[clientID]) + ":" + str(read[2])).encode(),client)
                                    #self.players -= 1
                                    #if self.players <= 0:
                                        #self.serverSocket.sendto("SCORE:sendScore".encode(), client)


                                print('serversend: '+self.serversendcheck) #did not even print...
                                print('serversend: '+self.clientoffsetcheck)
                                print('serversend: '+self.serverreceivecheck)
                                self.serverSocket.sendto(("serversendtime: " + str(time.time())).encode(), clientAddress) #send serversend time
                                print('server sent message: ' + str(time.time()))


##                                #testing
##                                if bool(self.offsets) == True: #if the dictionary is not empty
##                                        print('Offsets dictionary: ')
##                                        print(self.offsets.items())
##                                        print('keys: ')
##                                        print(self.offsets.keys())
##                                        print('values: ')
##                                        print(self.offsets.values())

                        except:
                                for room in self.gameUpdates.keys():
                                    if len(self.gameUpdates[room]) > 0:
                                        for event in self.gameUpdates[room]:
                                            for client in self.roomIPList[room]:
                                                self.serverSocket.sendto(event.encode(), client)
                                        self.gameUpdates[room] = []

                #self.serverSocket.close()
        def score(self,id, score):
            print("Is this working?")
            database = sqlite3.connect("scoreTable.db")
            d = database.cursor()
            print(id, score)
            database.execute("UPDATE scores set score = {sc} where user= {un}".format(sc = score, un = id))
            database.commit()
            d.execute("SELECT * FROM scores")
            data = d.fetchall()
            print(data)
        def checkLog(self,username, password, clientAddress):
                if clientAddress not in self.clientAddress.values():
##                        if self.players < 5:
                        self.clientAddress[clientAddress] = username
##                        else:
##                                print("The server is full. Please leave.")
                #clientSocket, addr = serverSocket.accept()
                connected = None
                #opens connection to SQLite database file database and returns a connection object
                connection = sqlite3.connect("scoreTable.db")
                #finds the username message from what was received
                c = connection.cursor()
                #executes the SQL statement 
                connection.execute('''CREATE TABLE IF NOT EXISTS scores
                            (user TEXT, pass TEXT, score TEXT, wins REAL)''')
                tups = [(username, password)]
                c.execute("SELECT * FROM scores")
                #returns a list of the results
                data = c.fetchall()
                print(data)
                un = ""
                for i in data:
                        if i[0] == username:
                                print("This username exists")
                                un = i[0]
                                if password == i[1]:
                                        connected = 0
                                        self.players += 1
                                else:
                                        connected = 1
                if un == "":
                        c.executemany("INSERT INTO scores VALUES (?,?,None,0)", tups)
                        connected = 0
                        self.players += 1
                        connection.commit()
                #commits the action to the database?
                
                if connected == 0: #Successfully logged in
                        print('IS THIS WORKING?!') #testing, works
                        self.serverSocket.sendto("Success".encode(), clientAddress)
                        print('HOW ABOUT NOW?!') #testing two, works
##                        while self.serversentcheck == False: #keep sending until received
                        print('ARE WE HERE?!') #wth
                        self.serverSocket.sendto(("serversendtime: " + str(time.time())).encode(), clientAddress) #send serversend time
                                #it does send but refuses to print out the statement after....
                                #if commented out, it's stuck in a loop
                                #so apparently it's been sending and catching maybe...?
                                #print('Sending?!?') #does not get here.... and not looping
                        print('server sent message: ' + str(time.time()))
                if connected == 1: #Password is invalid 
                        self.serverSocket.sendto("Invalid Password".encode(), clientAddress)
                #sends the modifiedMessage to client with IP and port stored in clientAddress 
                

            
if __name__ == "__main__":
        socket = Socket('0.0.0.0', 12000)
        socket.run()
        socket.close
