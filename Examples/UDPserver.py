from socket import *
import sqlite3
class Socket:
        def __init__(self, host, port):
                #self.serverPort = port #can be any number > 1024 cuz otherwise reserved
                self.serverSocket = socket(AF_INET, SOCK_DGRAM)
                self.serverSocket.bind((host, port))
                self.clientAddress = {}
                self.players = 0
                #serverSocket.listen(4) #denotes the number of clients can queue
                #it binds the serverSocket to port number specified in serverPort variable.
                #then when anybody sends anything to server IP address and serverPort the serverSocket will get it.

        print('The UDP server is ready to receive')
        print(gethostbyname(gethostname()))
        def run(self):
                while 1:
                        message, clientId = self.serverSocket.recvfrom(2048) #2048 is bytes of data to be received
                        #when something is recieved through serverSocket, the data will be stored in message.
                        #Also the client IP and port will be extracted and stored in variable clientAddress.
                        #recvfrom is specific to D_GRAMS foor UDP
                        #decodes the message
                        modMessage = message.decode()
                        print(modMessage)
                        read = modMessage.split(":")
##                        if read[0] == "TALK":
##                                for i in self.clientAddress.values():
##                                        self.serverSocket.sendto((read[1] + ": " + read[2]).encode(), i)
                        if read[0] == "LOG":
                                self.players += 1
                                self.checkLog(read[1], read[2], clientId)
                        if read[0] == "END":
                                break
                        #MOV:playerNumber:playerPosX:playerPosY
                        if read[0] == "MOV":
                                for i in self.clientAddress.values():
                                        self.serverSocket.sendto(modMessage.encode(),i)
                #self.serverSocket.close()
        def checkLog(self,username, password, clientAddress):
                if clientAddress not in self.clientAddress.values():
                        if self.players < 5:
                                self.clientAddress[self.players] = clientAddress
                        else:
                                print("The server is full. Please leave.")
                #clientSocket, addr = serverSocket.accept()
                connected = None
                #opens connection to SQLite database file database and returns a connection object
                connection = sqlite3.connect("scoreTable.db")
                #finds the username message from what was received
                c = connection.cursor()
                #executes the SQL statement 
                connection.execute('''CREATE TABLE IF NOT EXISTS scores
                            (user text, pass text, score real, wins real)''')
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
                                else:
                                        connected = 1
                if un == "":
                        c.executemany("INSERT INTO scores VALUES (?,?,0,0)", tups)
                        connected = 2
                #commits the action to the database?
                connection.commit()
                if connected == 2: #Username does not exist
                        self.serverSocket.sendto("Username does not exist".encode(), clientAddress)
                if connected == 0: #Successfully logged in 
                        self.serverSocket.sendto("Success".encode(), clientAddress)
                if connected == 1: #Password is invalid 
                        self.serverSocket.sendto("Invalid Password".encode(), clientAddress)
                #sends the moddifiedMessage to client with IP and port stored in clientAddress 
                
                
if __name__ == "__main__":
        socket = Socket('0.0.0.0', 12000)
        socket.run()
        socket.close
