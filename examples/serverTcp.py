from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
while 1:
	connSocket ,addr = serverSocket.accept()
	msg = connSocket.recv(1024)
	msg = msg.upper()
	connSocket.send(msg)
	connSocket.close()