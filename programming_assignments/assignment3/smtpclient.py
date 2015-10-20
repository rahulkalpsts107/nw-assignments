from socket import *
begmsg="From: alice@crepes.fr\nTo: bob@hamburger.edu\nSubject: Searching for the meaning of life.\n"
msg = "I Love computer networks!"
endmsg = "\r\n.\r\n"

nyu_usn = "cnJrMzEwQG55dS5lZHU=\r\n"
nyu_pass = "ZGJETEd0VFJXTlRzbUY=\r\n"

pulsesmtpserver = "smtp-pulse.com"
pulsesmtpport = 2525

clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
clientSocket.connect((pulsesmtpserver,pulsesmtpport))

print('Client: -connect done !')
recve = clientSocket.recv(1024)
recv = recve.decode('utf-8')
print ('Server: -'+recv)
if recv.split(' ',1)[0] != '220':
    print ('Client: -220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'EHLO rahul\r\n'
clientSocket.send(bytes(heloCommand,'UTF-8'))
recv1 = clientSocket.recv(1024)
recv = recv1.decode('utf-8')
print ('Server: -'+recv)

#Send AUTH command and print server response.
print ("Sending AUTH Command")
#AUTH with base64 encoded user name password
clientSocket.send(bytes("AUTH LOGIN\r\n",'ascii'))
recv2 = clientSocket.recv(1024)
recv = recv2.decode('utf-8')
print ('Server: -'+recv)
if recv.split(' ',1)[0] != '334':
    print ('Client: -334 reply not received from server.')

clientSocket.send(bytes(nyu_usn,'utf-8'))
recv3 = clientSocket.recv(1024)
recv = recv3.decode('utf-8')
print ('Server: -'+recv)
if recv.split(' ',1)[0] != '334':
    print ('Client: -334 reply not received from server.')

clientSocket.send(bytes(nyu_pass,'utf-8'))
recv4 = clientSocket.recv(1024)
recv = recv4.decode('ascii')
print ('Server: -'+recv)
if recv.split(' ',1)[0] != '235':
    print ('Client: -334 reply not received from server.')

#Send MAIL FROM command and print server response.
print ("Sending MAIL FROM Command")
clientSocket.send(bytes("MAIL FROM:<rrk310@nyu.edu>\r\n",'UTF-8'))
recv5 = clientSocket.recv(1024)
recv = recv5.decode('utf-8')
print ('Server: -'+recv)
if recv.split(' ',1)[0] != '250':
    print ('Client: -250 MAIL FROM failed.')


#Send RCPT TO command and print server response.
print ("Sending RCPT TO Command")
clientSocket.send(bytes("RCPT TO:<rahul.ramesh89@yahoo.co.in>\r\n",'UTF-8'))
recv6 = clientSocket.recv(1024)
recv = recv6.decode('utf-8')
print ('Server: -'+recv)
if recv.split(' ',1)[0] != '250':
    print ('Client: -250 RCPT TO Failed.')


#Send DATA command and print server response.
print ("Sending DATA Command")
clientSocket.send(bytes("DATA\r\n",'UTF-8'))
recv7 = clientSocket.recv(1024)
recv = recv7.decode('utf-8')
print ('Server: -'+recv)
if recv.split(' ',1)[0] != '354':
    print ('Client: --354 DATA Ready failed.')


#Send Data and print server response.
print ("Sending Data")
clientSocket.send(bytes(begmsg+msg+endmsg,'UTF-8'))
recv8 = clientSocket.recv(1024)
recv = recv8.decode('utf-8')
print ('Server: -'+recv)

#Send QUIT and print server response.
print ("Sending QUIT")
clientSocket.send(bytes("QUIT\r\n",'UTF-8'))
recv9 = clientSocket.recv(1024)
recv = recv9.decode('utf-8')
print ('Server: -'+recv)

print ("Client: -Mail Sent")
clientSocket.close()