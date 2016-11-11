from socket import *

serverPort=12001
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)

answers = ['trump', 'staryu', 'oak', 'rengar']

answer_info = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]

while True:

    print ('Ready to serve on port', serverPort)
    connectionSocket,addr =  serverSocket.accept()
    print ('connected from',addr)

    message = connectionSocket.recv(1024)
    print(message)

    if message.decode() == '' or message.decode() == '/favicon':
        continue

    else:
        if message.decode().isdigit():
            fileName = 'Questions/Question_' + str(message.decode()) + '.html'

            sendData = ''
            with open(fileName, 'r') as myfile:
                sendData = myfile.read().replace('\n', '')

            connectionSocket.send(sendData.encode())  # Use triple-quote string.

        else:
            answer = message.decode().split('.')[0]
            q_number = message.decode().split('.')[1]
            client = message.decode().split('.')[2]

            fileName = 'Questions/Question_' + (q_number) + '.html'
            with open(fileName, 'r') as myfile:
                sendData = myfile.read().replace('\n', '')

            if answer in answers:
                answer_info[int(q_number) - 1][client] = 'true'
            else:
                answer_info[int(q_number) - 1][client] = 'false'

            connectionSocket.send(sendData.encode())

    connectionSocket.close()

serverSocket.close()