from socket import * 
from threading import *
import pickle; from datetime import *
import tkinter as tk; from tkinter import filedialog
import os

fileStorage = {}
userLoginInfo = {}
connections = []



def NewClient(clientSocket,address):
    global fileStorage
    global userLoginInfo
    global connections
    connections += [clientSocket]
    while True:
        try:
            IncomingCommand = clientSocket.recv(1024).decode()
        except:
            pass
        else:
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
                if fileName in fileStorage:
                    clientSocket.send('reject'.encode())
                else:
                    clientSocket.send('file'.encode())
                    with clientSocket:
                        with open(filePath + fileName,'wb') as file:
                            while chunk:= clientSocket.recv(1 << 20):
                                file.write(chunk)
                                fileStorage[fileName] = userName
                    file.close()

            if IncomingCommand == 'list':
                data = pickle.dumps(fileStorage,-1)
                clientSocket.sendall(data)
            
            if IncomingCommand == 'get':
                clientSocket.send('filename'.encode())
                fileName = clientSocket.recv(1024).decode()
                if fileName in fileStorage:
                    clientSocket.send('download'.encode())
                    videofile = open(filePath + fileName,'rb')
                    while chunk:=videofile.read(1 << 20):
                        clientSocket.sendall(chunk)



def SaveFiles():
    global fileStorage
    saveFile = open(filePath + 'backup' + datetime.now().strftime('%Y-%m-%d-%H%M%S') +'.txt','wb')
    pickle.dump(fileStorage, saveFile)
    saveFile.close()


def LoadFiles():
    global fileStorage
    fileName = filedialog.askopenfilename(title='Select Backup File to Load',filetypes=[('All Files','*.*')])
    loadFile = open(fileName,'rb')
    fileStorage = pickle.load(loadFile)


def SaveCredentials():
    global userLoginInfo
    saveFile = open(filePath + 'usercredentials.txt','wb')
    pickle.dump(userLoginInfo,saveFile)
    saveFile.close

def LoadCredentials():
    global userLoginInfo
    try:
        loadFile = open(filePath + 'usercredentials.txt','rb')
    except:
        return
    else:
        userLoginInfo = pickle.load(loadFile)

def InputListener():
    global fileStorage
    while True:
        serverInput = input()
        if serverInput == 'save':
            SaveFiles()
        if serverInput == 'load':
            LoadFiles()
        if serverInput == 'list':
            if len(fileStorage) > 0:
                print('List of Files on Server:')
                for file in fileStorage:
                    print(file + ', Uploaded By - ' + fileStorage[file])
            else:
                print('Problem: No Files stored on Server')
        if serverInput.startswith('delete '):
            fileDelete = serverInput.removeprefix('delete ')
            if fileDelete in fileStorage:
                os.remove(filePath + fileDelete)
                del fileStorage[fileDelete]
            else:
                print('Problem: File Not Found')
        if serverInput == 'close':
            for connection in connections:
                connection.close()
            SaveCredentials()
            serverSocket.close()


def tkMainloop():
    root = tk.Tk()
    root.withdraw()
    root.mainloop()


def main():
    #Initiliazation
    global filePath
    filePath = 'E:\\'
    Host = '0.0.0.0'
    Port = 12345
    LoadCredentials()
    serverSocket.bind((Host, Port))
    serverSocket.listen(5)

    print('Listening for clients to connect...')
    serverMessage = 'Welcome! Type "help" to see a list of commands.'

    InputThread = Thread(target=InputListener)
    InputThread.start()
    
    tkThread= Thread(target=tkMainloop)
    tkThread.start()

    #Main Loop
    while True:
        connection, address = serverSocket.accept()
        print('Got connection: ' + str(address))
        ClientThread = Thread(target=NewClient(connection,address))
        ClientThread.start()


#Start

    #Create Socket
serverSocket = socket(AF_INET, SOCK_STREAM)

if __name__ == '__main__':
    main()
