from socket import * 
from threading import *
fileStorage = {}
userLoginInfo = {}
def NewClient(clientSocket,address):
    global fileStorage
    global userLoginInfo
    while True:
        IncomingCommand = clientSocket.recv(1024).decode()
        if IncomingCommand == 'login':
            clientSocket.send('username'.encode())
            userName = clientSocket.recv(1024).decode()
            clientSocket.send('password'.encode())
            userPass = clientSocket.recv(1024).decode()
            if userName in userLoginInfo:
                if userLoginInfo[userName] == userPass:
                    clientSocket.send('login'.encode())
                else:
                    clientSocket.send('incorrect'.encode())
            else:
                clientSocket.send('incorrect'.encode())
        
        if IncomingCommand == 'signup':
            clientSocket.send('username'.encode())
            userName = clientSocket.recv(1024).decode()
            clientSocket.send('password'.encode())
            userPass = clientSocket.recv(1024).decode()
            if userName in userLoginInfo:
                clientSocket.send('reject'.encode())
            else:
                userLoginInfo[userName] = userPass
                clientSocket.send('signup'.encode())


        if IncomingCommand == 'put':
            clientSocket.send('filename'.encode())
            fileName = clientSocket.recv(1024).decode()
            clientSocket.send('file'.encode())
            video = clientSocket.recv(481366*2)
            file = open(filePath + fileName,'wb')
            file.write(video)
            file.close()
            fileStorage[fileName] = userName
            print(fileStorage)
def main():
    #Initiliazation
    global filePath
    filePath = 'E:\\'
    Host = '0.0.0.0'
    Port = 12345
    
    serverSocket.bind((Host, Port))
    serverSocket.listen(5)

    print('Listening for clients to connect...')
    serverMessage = 'Welcome! Type "help" to see a list of commands.'


    #Main Loop
    while True:
        connection, address = serverSocket.accept()
        print('Got connection: ' + str(address))
        ClientThread = Thread(target=NewClient(connection,address))
    


#Start

    #Create Socket
serverSocket = socket(AF_INET, SOCK_STREAM)

if __name__ == '__main__':
    main()