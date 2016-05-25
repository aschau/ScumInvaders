from socket import *

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver

mailserver = 'smtp.gmail.com' #not too sure
mailport = 465 #for SSL

# Create socket called clientSocket and establish a TCP connection with mailserver

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((mailserver, mailport))

recv = clientSocket.recv(1024)
print(recv)

if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.

heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print(recv1)

if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
##start = 'STARTTLS\r\n'
##clientSocket.send(start)
##revc1 = clientSocket.recv(1024)
##print(recv1) #reponse

mailFrom = 'MAIL FROM: <sender@'+mailserver+'>\r\n'
clientSocket.send(mailFrom)
revc1 = clientSocket.recv(1024)
print(recv1) #reponse

if recv1[:3] != '250':
    print('250 reply not received from server.')
    
# Send RCPT TO command and print server response.
rcptTo = 'RCPT TO: <received@'+mailserver+'>\r\n'
clientSocket.send(rcptTo)
revc1 = clientSocket.recv(1024)
print(recv1) #response

if recv1[:3] != '250':
    print('250 reply not received from server.')
    
# Send DATA command and print server response.
data = 'DATA'
clientSocket.send(data)
revc1 = clientSocket.recv(1024)
print(recv1) #response

if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send message data.
message = raw_input('Enter Message: ')

# Message ends with a single period.
endmessage = '\r\n\r\n'
clientSocket.send(message + endmessage)
revc1 = clientSocket.recv(1024)
print(recv1) #response

if recv1[:3] != '250':
    print('250 reply not received from server.')
    
# Send QUIT command and get server response.
quitout = 'Quit\r\n'
clientSocket.send(quitout)
revc1 = clientSocket.recv(1024)
print(recv1) #response

if recv1[:3] != '250':
    print('250 reply not received from server.')
