from socket import *
import ssl
import base64

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"


#temp Username and Password for sending the message
username = "tempUserCPSC471@gmail.com"
password = "pswd1!@#"

ToUser = "sami.halwani1@gmail.com"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("smtp.gmail.com", 587)


# Create socket called clientSocket and establish a TCP connection with mailserver
# Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
# Fill in end


recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')


# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')


#Start TLS connection
TLS = "STARTTLS\r\n"
clientSocket.sendall(TLS.encode())
recvTLS = clientSocket.recv(1024)
print(f"StartTLS Response: {recvTLS.decode()}")

#ssl
clientSocketSSL = ssl.wrap_socket(clientSocket)

#Authorize User Credentials
userAuth = "AUTH LOGIN\r\n"
clientSocketSSL.sendall(userAuth.encode())
recvUserAuth = clientSocketSSL.recv(1024).decode()
print(f"AUTH LOGIN Reponse: {recvUserAuth}")

EnUsername = base64.b64encode(username.encode())
clientSocketSSL.sendall(EnUsername + "\r\n".encode())
recvUserAuth2 = clientSocketSSL.recv(1024).decode()
print(f"Username Authorization Response: {recvUserAuth2}")

EnPassword = base64.b64encode(password.encode())
clientSocketSSL.sendall(EnPassword + "\r\n".encode())
recvPassAuth = clientSocketSSL.recv(1024).decode()
print(f"Username Authorization Response: {recvPassAuth}")


# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <{username}> \r\n"
clientSocketSSL.sendall(mailFrom.encode())
recvMailReponse = clientSocketSSL.recv(1024).decode()
print(f"MAIL FROM response: {recvMailReponse}")



# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <sami.halwani1@gmail.com> \r\n"
clientSocketSSL.sendall(rcptTo.encode())
recvRCPT = clientSocketSSL.recv(1024).decode()
print(f" RCPT TO: {recvRCPT}")


# Send DATA command and print server response.
data = "DATA\r\n"
clientSocketSSL.sendall(data.encode())
clientSocketSSL.sendall(f"{msg}{endmsg}".encode())
recvData = clientSocketSSL.recv(1024).decode()
print(f"DATA Reponse: {recvData}")


# Send QUIT command and get server response.
clientSocketSSL.sendall("QUIT \r\n".encode())
recvQuit = clientSocketSSL.recv(1024).decode()
print(f"QUIT: {recvQuit}")
clientSocket.close()