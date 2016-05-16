#Elaine Chieng 55852758
#Jessica Lim 49545398

from socket import *

serverPort = 6789 #from instructions
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort)) #making a connection to that port
# 128.238.251.26
#192.168.1.57
serverSocket.listen(1) #allow only 1 connection

while True:
    #Establish connection
    print('Ready to serve...')

    connectionSocket, addr = serverSocket.accept() #client sends a message and server accepts connection
    print('Recieved connection from ', addr) #checking

    try:
        message = connectionSocket.recv(6789)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        #send one HTTP header line into socket

        #connectionSocket.send(message.split()[0] + ' 200 OK \r\n\r\n')
        connectionSocket.send('HTTP/1.1 200 OK \r\n\r\n')

        #send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        connectionSocket.close()

    except IOError:
        #send response message for file not found
        connectionSocket.send('404 Not Found')
        #close client socket
        connectionSocket.close()
serverSocket.close()
