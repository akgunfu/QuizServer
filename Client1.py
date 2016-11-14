from socket import *
import webbrowser

serverName='localhost'
multiplexingPort=12000

#clientSocket=socket(AF_INET,SOCK_STREAM)

#clientSocket.connect((serverName,multiplexingPort))

new = 2 # open in a new tab, if possible
url = "http://localhost:12000/Question_1.html"
webbrowser.open(url, new=new)

while True:
    message = input('Type message:')
    message = message.encode()

    #clientSocket.send(message)

    message = message.decode()

    if message=="exit":
        #clientSocket.close()
        exit(0)
    else :
        print ("message is sent")

