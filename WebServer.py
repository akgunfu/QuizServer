from socket import *
import re

QuizServerName = 'localhost'
QuizServerPort = 12001

QuizServerSocket = socket(AF_INET,SOCK_STREAM)
QuizServerSocket.bind(('localhost', QuizServerPort))
QuizServerSocket.listen(1)

Answers = ['trump', 'staryu', 'oak', 'rengar', 'hioneum', 'dubrovnik', '97', 'depp', 'tail', 'franklin']
AnswerInfo = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]


def handleRequest(connectionSocket, address):
    client = address[0]
    print('Quiz Server Connected From', client)

    try:
        message = connectionSocket.recv(1024)
    except:
        print ('Connection Lost')
        connectionSocket.close()
        return

    print(message)
    decoded = message.decode()

    if decoded[0] == '/':
        if re.search(r"/Results*", decoded):
            Client = decoded.split(',')[-1]
            print('Results are requested by', Client)
            ClientPoints = 0
            for k in AnswerInfo:
                if Client in k:
                    if k[Client] == 'true':
                        ClientPoints += 1
                else:
                    print('Client did not participate in this question.')
                    continue
            Results = """<html><head><title>Results</title></head><body>
                    <h1>Results</h1><p>Connected from {}<p>Total Points = {}</body></html>""".format(Client,ClientPoints)
            connectionSocket.send(Results.encode())
        else:
            print ('Bad Request')
            connectionSocket.close()
            return

    else:
        try:
            integer = int(decoded)
            FileName = 'Questions/Question_' + decoded + '.html'
        except:
            NextQuestionNumber, Answer, Client = decoded.split(',')
            FileName = 'Questions/Question_' + NextQuestionNumber + '.html'

            if Answer in Answers:
                AnswerInfo[int(NextQuestionNumber) - 2][Client] = 'true'
            else:
                AnswerInfo[int(NextQuestionNumber) - 2][Client] = 'false'

        SendData = ''
        try:
            with open(FileName, 'r') as MyFile:
                SendData = MyFile.read().replace('\n', '')
        except:
            print ('Requested file can not be opened or found')
            SendData = 'not-found'

        connectionSocket.send(SendData.encode())

    connectionSocket.close()


while True:

    print ('Ready to serve on port', QuizServerPort)
    connectionSocket,address =  QuizServerSocket.accept()
    handleRequest(connectionSocket,address)

QuizServerSocket.close()