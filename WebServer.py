from socket import *
import sys
import re

QuizServerName = 'localhost'
QuizServerPort = 12001

QuizServerSocket = socket(AF_INET,SOCK_STREAM)
QuizServerSocket.bind(('localhost', QuizServerPort))
QuizServerSocket.listen(1)

Answers = ['trump', 'staryu', 'oak', 'rengar', 'hioneum', 'dubrovnik', '97', 'depp', 'tail', 'franklin']
AnswerInfo = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]

clients = []

clientsAnswers = []

clientPoints = 0


def handleRequest(connectionSocket, address):
    client = address[0] + ':' + str(address[1])
    #print('Connected from:', client)

    try:
        message = connectionSocket.recv(1024)
    except:
        print ('Connection Lost')
        connectionSocket.close()
        return

    print("Message recieved from multiplexer server:",message.decode())
    decoded = message.decode()
    if(decoded == "/favicon"):
        print("This server architechture is not compatible with this browser. Please try another browser.")
        print("Closing server...")
        sys.exit()
    if (decoded[0] == "1" and decoded[1]!="0"):
        clients.append(decoded[1:])
        print(decoded[1:],"is appended to clients list.")
        decoded = decoded[0]
        FileName = 'Questions/Question_1.html'
    if(len(decoded)!=1):
        NextQuestionNumber, Answer, Client = decoded.split(',')
        FileName = 'Questions/Question_' + NextQuestionNumber + '.html'


        clientsAnswers.append(Answer)
        print("Given answer:",Answer)
        global clientPoints

        if(Answer == "trump"):clientPoints += 10
        if (Answer == "staryu"):clientPoints += 10
        if (Answer == "oak"):clientPoints += 10
        if (Answer == "rengar"):clientPoints += 10
        if (Answer == "hioneum"):clientPoints += 10
        if (Answer == "dubrovnik"):clientPoints += 10
        if (Answer == "97"):clientPoints += 10
        if (Answer == "depp"):clientPoints += 10
        if (Answer == "tail"):clientPoints += 10
        if (Answer == "franklin"):clientPoints += 10

        print("Points of client",Client,":",clientPoints)

    SendData = ''
    try:
        with open(FileName, 'r') as MyFile:
            SendData = MyFile.read().replace('\n', '')
    except:
        print ('Requested file can not be opened or found')
        SendData = 'not-found'


    connectionSocket.send(SendData.encode())


    #connectionSocket.close()


while True:

    #print ('Ready to serve on port', QuizServerPort)
    connectionSocket,address =  QuizServerSocket.accept()
    handleRequest(connectionSocket,address)

#QuizServerSocket.close()