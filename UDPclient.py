from socket import * 

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = raw_input('input Lowercase sentence:')
clientSocket.sendto(message,(serverName,serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print modifiedMessage

from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print "The UDP server is ready to receive"

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	modifiedMessage = message.upper()

	print modifiedMessage
	serverSocket.sendto(modifiedMessage, clientAddress)

