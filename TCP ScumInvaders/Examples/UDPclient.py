from socket import * 

#serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
ip =input("Enter IP: ")
username = input('username: ')
password = input('password: ')
message = "LOG:" + username + ":" + password
#sends the string message, must be encoded. default utf-8
clientSocket.sendto(message.encode(),(ip,serverPort))

#receiving messages from server. Must decode
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())

#infinite loops
while 1:
        replies = input('Talk about something: ')
        if replies == "quit":
                break
        clientSocket.sendto(("TALK:" + username + ":" + replies).encode(), (ip, serverPort))
        newMessage, serverAddress = clientSocket.recvfrom(2048)
        print(newMessage.decode())
##        #asks for the input to send
##        ip =input("Enter IP: ")
##        username = input('username: ')
##        password = input('password: ')
##        message = "LOG:" + username + ":" + password
##        #sends the string message, must be encoded. default utf-8
##        clientSocket.sendto(message.encode(),(ip,serverPort))
##
##        #receiving messages from server. Must decode
##        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
##        print(modifiedMessage.decode())
##
clientSocket.close()
