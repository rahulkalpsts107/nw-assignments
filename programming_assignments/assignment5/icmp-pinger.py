from socket import *
import os
import sys
import struct
import time
import select
import binascii
import socket
import ctypes
import math

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_ECHO_REQUEST_CODE = 0
ICMP_ECHO_REPLY_CODE = 0

def checksum(str):
    #print(str)
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = str[count+1] * 256 + str[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(str):
        csum = csum + ord(str[len(str) - 1])
        csum = csum & 0xffffffff
        csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        timeLeft = timeout
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        #if whatReady[0] == []: # Timeout
            #return "#Request timed out."
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        #Fill in start
        #Fetch the ICMP header from the IP packet
        psize= len(recPacket)
        #advance to 128th byte coz thats where ICMP starts
        icmp_header = struct.unpack("bbHHhd",recPacket[psize-16:])
        print('icmp response recvd type - '+str(icmp_header[0])+' code - '+str(icmp_header[1])+
          ' checksum - '+str(icmp_header[2])+' ID - '+str(icmp_header[3])+' seq - '+str(icmp_header[4])+' EPOCH - '+str(icmp_header[5]))
        #Fill in end

        timeLeft = timeLeft - howLongInSelect
        timeLeft = math.ceil(timeLeft)
        if timeLeft <= 0:
            return "#Request timed out."
        else:
            return timeLeft

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, ICMP_ECHO_REQUEST_CODE, myChecksum, ID, 1)
    tim = time.time()
    data = struct.pack("d",tim )
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, ICMP_ECHO_REQUEST_CODE, myChecksum, ID, 1)
    packet = header + data
    print('icmp request type - '+str(ICMP_ECHO_REQUEST)+' code - '+str(ICMP_ECHO_REQUEST_CODE)+
          ' checksum - '+str(myChecksum)+' ID - '+str(ID)+' seq - '+str(1)+' EPOCH - '+str(tim))
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")
    #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.org/papers/sock_raw
    #Fill in start
    #Create Socket here
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)
    #Fill in end
    myID = os.getpid() & 0xFFFF #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def ping(host, timeout=1):
    #timeout=1 means: If one second goes by without a reply from the server,
    #the client assumes that either the client’s ping or the server’s pong is lost
    dest = socket.gethostbyname(host)
    print ("Pinging " + dest + ' aka '+host+" using Python:")
    print ("")
    #Send ping requests to a server separated by approximately one second
    i = 5
    while i :
        delay = doOnePing(dest, timeout)
        print('Ping times '+str(i)+' RTT = '+str(delay))
        i-=1
    return delay

ping("www.google.com")
ping("www.facebook.com")
ping("www.yahoo.com")
ping("www.gmail.com")
