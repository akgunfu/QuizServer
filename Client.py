from socket import *

serverName='localhost'
multiplexingPort=12000

clientSocket=socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,multiplexingPort))

message='Hello World'.encode()


clientSocket.send(message)

clientSocket.close()