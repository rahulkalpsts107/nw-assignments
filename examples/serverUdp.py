from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
while 1:
	message,clientAddress = serverSocket.recvfrom(2048)
	mod = message.upper()
	serverSocket.sendto(mod,clientAddress)
