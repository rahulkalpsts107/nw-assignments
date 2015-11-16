from socket import *
import os
import sys
import struct
import time
import select
import binascii
import socket
import ctypes

MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2
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

def build_packet():
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    ID = os.getpid() & 0xFFFF
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, ICMP_ECHO_REQUEST_CODE, myChecksum, ID, 1)
    data = struct.pack("d",time.time() )
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
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    done =0
    print ("trace route " + socket.gethostbyname(hostname) + ' aka '+hostname+" using Python:")
    for ttl in range(1,MAX_HOPS+1):#xrange is removed from python 3.0
        timeTaken =[-1,-1,-1]
        name=''
        for tries in range(0,TRIES+1):#xrange is removed from python 3.0
            #Fill in start
            # Make a raw socket named mySocket
            destAddr = socket.gethostbyname(hostname)
            icmp = socket.getprotobyname("icmp")
            mySocket =socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            #Fill in end
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                recvPacket, addr = mySocket.recvfrom(1024)
                try:
                    host = socket.gethostbyaddr(addr[0])
                    name  = '{0} ({1})'.format(addr[0] , host[0])
                except Exception:
                    name  = '{0} (host name/IP not found)'.format(addr[0])
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
            except socket.timeout:
                continue
            else:
                #Fill in start
                # Fetch the icmp type from the IP packet
                icmpHeaderContent = recvPacket[20:28]
                type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeaderContent)
                #Fill in end
                if type == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    timeTaken[tries] = (timeReceived -t)*1000
                    #print (" %d rtt=%.0f ms %s" %(ttl, (timeReceived -t)*1000, addr[0]),socket.gethostbyaddr(addr[0])[0])
                elif type == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    timeTaken[tries] =(timeReceived-t)*1000
                    #print (" %d rtt=%.0f ms %s" %(ttl, (timeReceived-t)*1000, addr[0]),socket.gethostbyaddr(addr[0])[0])
                elif type == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    timeTaken[tries]=(timeReceived - timeSent)*1000
                    #print (" %d rtt=%.0f ms %s" %(ttl, (timeReceived - timeSent)*1000, addr[0]),socket.gethostbyaddr(addr[0])[0])
                    done = 1
                else:
                    print ("error")
                    break
            finally:
                mySocket.close()
        i=0
        a= ['*','*','*']
        if timeTaken[i] != -1:
            a[i] = int(timeTaken[i])
        if timeTaken[i+1] != -1:
            a[i+1] = int(timeTaken[i+1])
        if timeTaken[i+2] != -1:
            a[i+2] = int(timeTaken[i+2])
        if timeTaken[i] == timeTaken[i+1] == timeTaken[i+2] == -1:
            print(" %d rtt=%s ms rtt=%s ms rtt=%s ms %s" %(ttl, a[i],a[i+1],a[i+2] ,'Request Timed out.'))
        else:
            print(" %d rtt=%s ms rtt=%s ms rtt=%s ms %s" %(ttl, a[i],a[i+1],a[i+2] ,name))
        if done == 1:
            print('Trace Complete.')
            return

#get_route("google.com")
#get_route("smtp-pulse.com")
#get_route("yahoo.com")
get_route("gmail.com")