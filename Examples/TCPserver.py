from socket import *
import sqlite3
import hashlib
import os

class TCP_Server:
    def __init__(self, host, port):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(("", port))
        print("It binded.")
        print("Fail before listen.")
        self.serverSocket.listen(4)
        print("it can listen")
        #self.serverSocket.settimeout(0.0)
        self.connectSocket = None
        self.clientAddresses = {}
    def test(self):
        word = input("Enter a pasword: ")
        salt = "thisissalty"
        hashed = hashlib.md5()
        hashed.update((salt + word).encode())
        again = input("Type again: ")
        check = hashlib.md5()
        check.update((salt + again).encode())
        if hashed.hexdigest() == check.hexdigest():
            print("The values match")
        else:
            print("You failed.")
        
    def run(self):
        #conn, clientID = self.serverSocket.accept()
        self.connectSocket, clientID = self.serverSocket.accept()
        while True:
            data = self.connectSocket.recv(200)
            if not data: break
            read = data.decode().split(":")
            print(read)
            if read[0] == "LOG":
                self.checkLog(read[1], read[2], clientID)
            elif read[0] == "TALK":
                self.connectSocket.send(read[1].encode())
            elif read[0] == "STOP":
                self.connectSocket.send(read[0].encode())
                break
            else:
                self.connectSocket.send("Send again".encode())
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
    def checkLog(self,username, password, clientAddress):
        if clientAddress not in self.clientAddresses.values():
            self.clientAddresses[clientAddress] = username
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
                    self.connectSocket.send("Login success.".encode())
                else:
                    self.connectSocket.send("Login failed.".encode())
        '''hashing password'''
        if un == "":
            print("Creating username.")
            hashed = hashlib.md5()
            hashed.update((salt + password).encode())
            hashedPassword = str(hashed.hexdigest())
            tups = (username, hashedPassword)
            c.execute("INSERT INTO logins VALUES (?,?)", (username, hashedPassword))
            self.connectSocket.send("Username created.".encode())
            print("Created username.")
            connection.commit()
        c.execute('SELECT * FROM logins')
        data = c.fetchall()
        print(data)
            
if __name__ == "__main__":
    socket = TCP_Server(gethostbyname(gethostname()), 12000)
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
