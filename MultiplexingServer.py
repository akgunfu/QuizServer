from socket import *
import _thread

QuizServerName='localhost'
QuizServerPort=12001

MultiplexingServerName = 'localhost'
MultiplexingServerPort=12000

MultiplexingServerSocket = socket(AF_INET,SOCK_STREAM)
MultiplexingServerSocket.bind((MultiplexingServerName, MultiplexingServerPort))
MultiplexingServerSocket.listen(1)

connections = {}

def handleGetRequest (connectionSocket, address, request):
    questionNumber = request['Path'].split('_')[-1].split('.')[0]
    try:
        QuizServerSocket = socket(AF_INET, SOCK_STREAM)
        QuizServerSocket.connect((QuizServerName, QuizServerPort))
        QuizServerSocket.send(questionNumber.encode())
        try:
            Question = QuizServerSocket.recv(1024)
            connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
            connectionSocket.send('Content-Type: text/html\n'.encode())
            connectionSocket.send('\n'.encode())
            connectionSocket.send(Question)
            connections[address] = 'Active'
        except:
            print('Can not get data from the server')

        QuizServerSocket.close()

    except:
        print('Can not communicate with server')


def handlePostRequest (connectionSocket, address, request, postData):
    questionNumber = request['Path'].split('_')[-1].split('.')[0]
    client = address[0] + ':' + str(address[1])
    data = questionNumber + ',' + postData + ',' + client
    print(data)
    try:
        QuizServerSocket = socket(AF_INET, SOCK_STREAM)
        QuizServerSocket.connect((QuizServerName, QuizServerPort))
        QuizServerSocket.send(data.encode())
        try:
            reply = QuizServerSocket.recv(1024)
            connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
            connectionSocket.send('Content-Type: text/html\n'.encode())
            connectionSocket.send('\n'.encode())
            connectionSocket.send(reply)
        except:
            print('Can not get the correct answer from the server')

        QuizServerSocket.close()

    except:
        print('Can not send answer to the server')


def handleRequest (connectionSocket, address):
    client = address[0] + ':' + str(address[1])
    print('Thread created for', client)
    print ('Connected from', client)
    while True:
        try:
            message = connectionSocket.recv(1024)
        except:
            print ('Time Out')
            connectionSocket.send('Time Out'.encode())
            break

        print (message)
        decoded = message.decode()

        if decoded == '':
            break
        else:
            if (decoded[0] != 'G' and decoded[0] != 'P'):
                continue

        _request, _message = message.decode().split('\r\n', 1)

        request = {}
        request['Method'], request['Path'], request['http-version'] = _request.split(' ')

        if request['Method'] == 'GET':
            handleGetRequest(connectionSocket,address, request)

        if request['Method'] == 'POST' and request['Path'] != '/favicon.ico':
            postData =  message.decode().split('\r\n')[-1].split('=')[-1]
            handlePostRequest(connectionSocket, address, request, postData)

    connectionSocket.close()


while True:

    print ('Ready to serve on port' ,MultiplexingServerPort)

    ConnectionSocket, address =  MultiplexingServerSocket.accept()
    ConnectionSocket.settimeout(10)

    _thread.start_new_thread(handleRequest, (ConnectionSocket, address))



