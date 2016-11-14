from socket import *
import _thread

QuizServerName='localhost'
QuizServerPort=12001

MultiplexingServerName = 'localhost'
MultiplexingServerPort=12000

MultiplexingServerSocket = socket(AF_INET,SOCK_STREAM)
MultiplexingServerSocket.bind((MultiplexingServerName, MultiplexingServerPort))
MultiplexingServerSocket.listen(1)


def handleGetRequest (connectionSocket, address, request):
    print("Handling GET request:")
    client = address[0] + ':' + str(address[1])
    print(" Connected client(browser) address:",client)
    try:
        questionNumber = request['Path'].split('_')[-1].split('.')[0]
    except:
        print ('Invalid Request')
        #connectionSocket.send('HTTP/1.0 404 NOT-FOUND'.encode())
        return

    try:
        QuizServerSocket = socket(AF_INET, SOCK_STREAM)
        QuizServerSocket.connect((QuizServerName, QuizServerPort))
        QuizServerSocket.send(questionNumber.encode())
        print(" Request for question number:",questionNumber,"is sent to quiz server")
        if(questionNumber=="1"):
            print(" We must send this client address:",client,"to the web server, create a container to contain the answers and points.")
            QuizServerSocket.send(client.encode())
        try:
            Question = QuizServerSocket.recv(1024) #Question is the HTML file
            print(" HTML page for Question", questionNumber, "is received from quiz server.")
            connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
            connectionSocket.send('Content-Type: text/html\n'.encode())
            connectionSocket.send('\n'.encode())
            connectionSocket.send(Question)
            print(" HTML page for Question",questionNumber,"is sent to client(browser):",client)
        except:
            print('Can not get data from the server')

        #QuizServerSocket.close()

    except:
        print('Can not communicate with server')


def handlePostRequest (connectionSocket, address, request, postData):
    print("Handling POST request")
    questionNumberOrPath = request['Path'].split('_')[-1].split('.')[0]
    #client = address[0]
    client = address[0] + ':' + str(address[1])
    data = questionNumberOrPath + ',' + postData + ',' + client
    try:
        QuizServerSocket = socket(AF_INET, SOCK_STREAM)
        QuizServerSocket.connect((QuizServerName, QuizServerPort))
        QuizServerSocket.send(data.encode())
        print(" Data that is sent to the web server:", data)
        try:
            reply = QuizServerSocket.recv(1024)
            connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
            connectionSocket.send('Content-Type: text/html\n'.encode())
            connectionSocket.send('\n'.encode())
            connectionSocket.send(reply)
        except:
            print('Can not get the correct answer from the server')

        #QuizServerSocket.close()

    except:
        print('Can not send answer to the server')


def handleRequest (connectionSocket, address):
    print("Handling request:")
    global how_many_clients
    client = address[0] + ':' + str(address[1])
    print("    Web page opened, thread created for client(browser):", client)
    while True:
        try:
            message = connectionSocket.recv(1024)
        except:
            print ('Time Out')
            #connectionSocket.send('Time Out'.encode()) You can't send a message to a client that you're not connected to
            break

        print ("    Message recieved from client(browser)",client,":",message.decode())
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
            break

        if request['Method'] == 'POST' and request['Path'] != '/favicon.ico':
            postData =  message.decode().split('\r\n')[-1].split('=')[-1]
            handlePostRequest(connectionSocket, address, request, postData)
            break

    #connectionSocket.close()


while True:

    print ('Ready to serve on port' ,MultiplexingServerPort)

    ConnectionSocket, address =  MultiplexingServerSocket.accept()
    ConnectionSocket.settimeout(30)

    print("Web page opened, attempting to start a new thread for adress:",address)
    if(address!=""):
        _thread.start_new_thread(handleRequest, (ConnectionSocket, address))





