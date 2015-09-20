import socket
from threading import Thread

notFoundResponse = """HTTP/1.1 404 Not Found\r\n Content-type: text/html\r\n \n
<html>\r\n
<body>\r\n
  <h1>404 Not Found</h1>\r\n
  <p>The requested URL was not found on this server.</p>\r\n
 </body>\r\n
</html>\r\n"""

foundResponse = """HTTP/1.1 200 OK\r\n Content-type: text/html\r\n
"""

# Once Server accepts connection it post's to worker thread to
# provide response of HTML File.

def worker(connectionSocket,addr):
    print('Received'+str(addr))
    try:
        message = connectionSocket.recv(1024)
        filename = str(message,"utf-8").split()[1]
        f = open(filename[1:])
        content = f.read()
        outputdata = bytearray()
        outputdata.extend(map(ord, content))

        #Send one HTTP header line into socket
        connectionSocket.send(foundResponse.encode('utf-8'))

        #Send the content of the requested file to the client
        connectionSocket.send(outputdata)

        #Close client socket
        connectionSocket.close()
        f.close()

    except (IOError,IndexError):
        #Send response message for file not found
        connectionSocket.send(notFoundResponse.encode('utf-8'))
        #Close client socket
        connectionSocket.close()

def serverMain():
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind(('localhost',81))
    print('Main Server Started !')
    while True:
        serverSocket.listen(5)
        print('Ready to serve ..')
        connectionSocket, addr = serverSocket.accept()

        #Post it to worker thread to unblock this thread
        w = Thread(target=worker, args=(connectionSocket,addr))
        w.start()
    serverSocket.close()

if __name__ == '__main__':
    serverMain()