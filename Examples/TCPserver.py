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
        connectSocket, clientID = self.serverSocket.accept()
        while True:
            data = connectSocket.recv(200)
            if not data: break
            read = data.decode().split(":")
            print(read)
            if read[0] == "LOG":
                self.checkLog(read[1], read[2])
            elif read[0] == "TALK":
                connectSocket.send(read[1].encode())
            elif read[0] == "STOP":
                connectSocket.send(read[0].encode())
                break
            else:
                connectSocket.send("Send again".encode())
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
        if clientAddress not in self.clientAddress.values():
            self.clientAddress[clientAddress] = username
        connected = None
        connection = sqlite.connect("testData.db")
        c = connection.cursor()
        connection.execute('''CREATE TABLE IF NOT EXISTS logins (user TEXT, pass TEXT)''')
        tups = [(username, password)]
        c.execute('SELECT * FROM logins')
        data = c.fetchall()
        print(data)
        un = ""
        for i in data:
            if i[0] == username:
                print("This username exists")
                un = i[0]
if __name__ == "__main__":
    socket = TCP_Server(gethostbyname(gethostname()), 12000)
    print(gethostbyname(gethostname()))
    socket.run()
    socket.serverSocket.close()
