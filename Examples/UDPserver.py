from socket import *
import sqlite3
class Socket:
        def __init__(self, host, port):
                #self.serverPort = port #can be any number > 1024 cuz otherwise reserved
                self.serverSocket = socket(AF_INET, SOCK_DGRAM)
                self.serverSocket.bind((host, port))
                #serverSocket.listen(4) #denotes the number of clients can queue
                #it binds the serverSocket to port number specified in serverPort variable.
                #then when anybody sends anything to server IP address and serverPort the serverSocket will get it.

        print('The UDP server is ready to receive')
        def run():
                while 1:
                        message, clientAddress = self.serverSocket.recfrom(2048) #2048 is bytes of data to be received
                        #when something is recieved through serverSocket, the data will be stored in message.
                        #Also the client IP and port will be extracted and stored in variable clientAddress.
                        #recvfrom is specific to D_GRAMS foor UDP
                        #decodes the message
                        modMessage = message.decode()
                        print(modMessage)
                        read = modMessage.split(":")
                        if read[0] == "LOG":
                                checkLog(read[1], read[2])
                        if read[0] == "END":
                                break
                serverSocket.close()
        def checkLog(username, password):
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
                        serverSocket.sendto("2".encode(), clientAddress)
                if connected == 0: #Username exists and password was entered correctly
                        serverSocket.sendto("0".encode(), clientAddress)
                if connected == 1: #Password is invalid 
                        serverSocket.sendto("1".encode(), clientAddress)
                #sends the moddifiedMessage to client with IP and port stored in clientAddress 

if __name__ == "__main__":
	socket = Socket('localhost', 12000)
	socket.run()
