from socket import *
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)# IP_V4 and data gram
message= input("Enter the text")
msg1 = bytes(message, 'UTF-8')
clientSocket.sendto(msg1,(serverName,serverPort))
modifiedMessage,serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)
clientSocket.close()