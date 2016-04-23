from socket import * 

#serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

#infinite loops
while 1:
        #asks for the input to send
        ip =input("Enter IP: ")
        username = input('username: ')
        password = input('password: ')
        message = username + ":" + password
        #sends the string message, must be encoded. default utf-8
        clientSocket.sendto(message.encode(),(ip,serverPort))

        #receiving messages from server. Must decode
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())



