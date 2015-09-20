import sys
import socket
from sys import argv

#Supports only IPv4 for now
def getHost(hostAddr):
    return socket.gethostbyname(hostAddr)

def clientMain(argv):
    print('Entered Client process !')
    if(len(argv) == 4):
        print('server host : '+argv[1] + ' server port : '+argv[2] + ' filename = '+argv[3])
        hostAddr = getHost(argv[1])
        hostPort = argv[2]
        file = argv[3]
        print('Host is = '+hostAddr)
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSock.connect((hostAddr, int(hostPort)))
        reqString = 'GET '+file +' HTTP/1.1\r\nHost:' + hostAddr +":"+hostPort+'\r\nConnection: keep-alive\r\n \r\n\r\n'
        clientSock.sendall(str.encode(reqString))
        data = clientSock.recv(1024)
        print(str(data))
        clientSock.close()
    else:
        print('Wrong Usage! , please input format sock_client.py [server_host] [server_port] [filename]')

if __name__ == '__main__':
    clientMain(argv)