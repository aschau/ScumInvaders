from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
#it binds the serverSocket to port number specified in serverPort variable.
#then when anybody sends anything to server IP address and serverPort the serverSocket will get it.

serverSocket.listen(1)
#server listens to TCP connection waiting for client requests.
#the 1 specifies the max number of queued connections(at least 1)

print 'The TCP server is ready to receive'
while 1:
#While 1 is an infinite loop. server is always waiting for requests

	connectionSocket, addr = serverSocket.accept()
	#when a client reaches to server the accept method for serverSocket creates a new socket in server called connectionSocket.
	#the connectionSocket is dedicated to that client. Then the clientSocket and the connectionSocket will do a handshaking to create a TCP connection.
	sentence = connectionSocket.recv(1024)
	capitalizedSentence = sentence.upper()
	connectionSocket.send(capitalizedSentence)
	connectionSocket.close()
	#the connectionSocket will be closed after the modified sentence is sent back.(new sentence new connectionSocket)
