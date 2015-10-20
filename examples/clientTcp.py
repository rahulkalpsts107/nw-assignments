from socket import *
serverName="localhost"
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
msg = input("Input Text")
msg1 = bytes(msg,'UTF-8')
clientSocket.send(msg1)
msg=clientSocket.recv(2048)
print(msg)
clientSocket.close()
