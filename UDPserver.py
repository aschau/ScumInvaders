from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
#it binds the serverSocket to port number specified in serverPort variable.
#then when anybody sends anything to server IP address and serverPort the serverSocket will get it.

print "The UDP server is ready to receive"
while 1:
#While 1 is an infinite loop. server is always waiting for requests

	message, clientAddress = serverSocket.recvfrom(2048)
	#when something is recieved through serverSocket, the data will be stored in message.
	#Also the client IP and port will be extracted and stored in variable clientAddress.

	modifiedMessage = message.upper()
	#transformes the message to uppercase 
	print modifiedMessage

	serverSocket.sendto(modifiedMessage, clientAddress)
	#sends the moddifiedMessage to client with IP and port stored in clientAddress 

