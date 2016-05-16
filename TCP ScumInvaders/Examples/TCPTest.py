from socket import *

TCP_IP = gethostbyname(gethostname())
TCP_PORT = 12000

s = socket(AF_INET, SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(2)

print(TCP_IP)
conn, addr = s.accept()
print("Connection address: ", addr)
while 1:
    data = conn.recv(200)
    if not data: break
    print("Received data: ", data)
    conn.send(data)
conn.close()
