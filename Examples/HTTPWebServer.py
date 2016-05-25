#Elaine Chieng 55852758
#Jessica Lim 49545398

import os
from socket import *

serverPort = 6789 #from instructions
serverSocket = socket(AF_INET, SOCK_STREAM)
#serverHost = serverSocket.gethostname() 
serverSocket.bind(('', serverPort)) #making a connection to that port, don't put ip


serverSocket.listen(1) #allow only 1 connection

while True:
    #Establish connection
    print('Ready to serve...')

    connectionSocket, addr = serverSocket.accept() #client sends a message and server accepts connection
    print('Received connection from ', addr) #checking

    try:
        message = connectionSocket.recv(6000) #max amount of data to be received at once
        #if len(message) > 1: #don't split an empty string
        if not message:
            break
        filename = message.split()[1]
        #print(filename[1:])
        if (filename.find('html') != -1): #is an html file
            f = open(filename[1:])
        else: #image
            f = open(filename[1:], 'rb')
        #outputdata = f.readlines()[:-1]
        outputdata = f.read()

        #send one HTTP header line into socket
        #connectionSocket.send(message.split()[0] + ' 200 OK \r\n\r\n')
        connectionSocket.send('HTTP/1.1 200 OK \r\n\r\n')

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
##        #send the content of the requested file to the client
##        pic = ''
##        for i in range(0, len(outputdata)):
##            if (outputdata[i].find('img src=".') != -1): #finding an image if any
##                picstart = outputdata[i].find('img src=".') + len('img src=".')
##                picend = outputdata[i].find('" width')
##                for p in range(0, picend-picstart):
##                    pic += outputdata[i][picstart + p]
##                pic = pic.replace('/', '\\')
##                currentpath = os.getcwd()
##                print(currentpath+pic)
##                with open(currentpath+pic, 'rb') as image:
##                    imgdata = image.read(1024)
##                    while (imgdata):
##                        connectionSocket.send(imgdata)
##                        imgdata = image.read(1024)
####                    while True:
####                        img = image.read()
####                        print('string: ', strng) #something weird
####                        if not strng:
####                            print('failed')
####                            break
####                        connectionSocket.send(img)
####                        print('did not break') #dies somewhere here)
####                        image.write(strng)
####                        #connectionSocket.send(strng)
####                        image.close()
####                except:
####                    connectionSocket.send('Failed to open image file')
##            else:
##                connectionSocket.send(outputdata[i])

        f.close()
        connectionSocket.close()

    except IOError:
        #send response message for file not found
        print('IOError')
        print('404 Not Found')
        connectionSocket.send('404 Not Found')
        #close client socket
        connectionSocket.close()
        #serverSocket.close() #close socket if fails just in case
serverSocket.close() #closes outside loop
