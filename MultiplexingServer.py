from socket import *
import _thread

serverName='localhost'
multiplexingPort=12000
serverPort=12001


multiplexingSocket = socket(AF_INET,SOCK_STREAM)
multiplexingSocket.bind(('localhost', multiplexingPort))
multiplexingSocket.listen(1)


def handleRequest (connectionSocket, address):
    print ('Connected from', address)
    while True:
        try:
            message = connectionSocket.recv(1024)
        except:
            print ('Time Out')
            connectionSocket.send('Time Out'.encode())
            break

        print (message)

        if message.decode() == '':
            break
        else:
            if (message.decode()[0] != 'G' and message.decode()[0] != 'P'):
                continue

        request, _message = message.decode().split('\r\n', 1)

        m = {}
        m['Method'], m['Path'], m['http-version'] = request.split(' ')

        if m['Method'] == 'GET':
            questionNumber = m['Path'].split('_')[-1].split('.')[0]
            try:
                serverSocket = socket(AF_INET, SOCK_STREAM)
                serverSocket.connect(('localhost', serverPort))
                serverSocket.send(questionNumber.encode())
                try:
                    Question = serverSocket.recv(1024)
                    connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
                    connectionSocket.send('Content-Type: text/html\n'.encode())
                    connectionSocket.send('\n'.encode())
                    connectionSocket.send(Question)
                    connections[address] = 'Active'
                except:
                    print('Can not get data from the server')
            except:
                print ('Can not communicate with server')

            serverSocket.close()


        if m['Method'] == 'POST' and m['Path'] != '/favicon.ico':
            answer = message.decode().split('\r\n')[-1].split('=')[-1]
            questionNumber = m['Path'].split('_')[-1].split('.')[0]
            client = address[0] + ':' + str(address[1])
            data = answer + '.' + questionNumber + '.' + client
            print(data)
            try:
                serverSocket = socket(AF_INET, SOCK_STREAM)
                serverSocket.connect(('localhost', serverPort))
                serverSocket.send(data.encode())
                try:
                    reply = serverSocket.recv(1024)
                    connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
                    connectionSocket.send('Content-Type: text/html\n'.encode())
                    connectionSocket.send('\n'.encode())
                    connectionSocket.send(reply)
                except:
                    print ('Can not get the correct answer from the server')
            except:
                print ('Can not send answer to the server')

            serverSocket.close()

    connectionSocket.close()

connections = {}

while True:

    print ('Ready to serve on port' ,multiplexingPort)
    connectionSocket, address =  multiplexingSocket.accept()
    connectionSocket.settimeout(10)
    connections[address] = 'Idle'

    client = address[0] + ':' + str(address[1])
    print ('Thread created for', client)
    _thread.start_new_thread(handleRequest, (connectionSocket, address))

    for keys, values in connections.items():
        print(keys)
        print(values)



