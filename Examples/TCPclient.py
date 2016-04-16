from socket import *
#The socket module forms the basis of all network communication
serverName = 'localhost'
serverPort = 12000
#Firstline specifies the address of the server. it can be an IP or servername. 
	#e.g. "128.138.32.126" or "yourserver.eng.uci.edu"
#second line shows which port your server will be working on(usually we use high number)

clientSocket = socket(AF_INET, SOCK_STREAM)
#this line creats a socket called clientSocket. 
#AF_INET specifies address family which is IPv4
#SOCK_STREAM shows the protocol for the socket which is TCP here.

clientSocket.connect((serverName,serverPort))
#initiates the TCP connection between the server and client. 3way handshake is established.

sentence = raw_input('Input lowercase sentence:')
clientSocket.send(sentence)
#this linse sends the sentence through the client's socket into TCP connection.
#here we dont have to specify the address explicitly like UDP. 
#Instead we simply drop the packet to established TCP connection.
modifiedSentence = clientSocket.recv(1024)
#now when a message is recieved from internet to the client socket we will get it here.
#then we will put the message in modifiedMessage. 
#2048 here is the size of the buffer for receiving data

print 'From Server:', modifiedSentence
clientSocket.close()