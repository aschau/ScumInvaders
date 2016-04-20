from socket import *
import sqlite3
connection = sqlite3.connect("scoreTable.db")
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('localhost', serverPort))
#it binds the serverSocket to port number specified in serverPort variable.
#then when anybody sends anything to server IP address and serverPort the serverSocket will get it.

print('The UDP server is ready to receive')
while 1:
#While 1 is an infinite loop. server is always waiting for requests

        message, clientAddress = serverSocket.recvfrom(2048)
        #when something is recieved through serverSocket, the data will be stored in message.
        #Also the client IP and port will be extracted and stored in variable clientAddress.

        #decodes the message
        modifiedMessage = message.decode()
        print(modifiedMessage)

        #finds the username message from what was received
        c = connection.cursor()
        connection.execute('''CREATE TABLE scores
                    (user text, pass text)''')
        indexstring = modifiedMessage.split(':')
        tups = [(indexstring[0], indexstring[1])]
        c.executemany("INSERT INTO scores VALUES (?,?)", tups)
        c.execute("SELECT * FROM scores")
        print(c.fetchone())
        
        connection.commit()
        connection.close()
        #if indexstring[0] == 'username':
        #        print('username is:' + indexstring[1])
        #else:
        #        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        #sends the moddifiedMessage to client with IP and port stored in clientAddress 

