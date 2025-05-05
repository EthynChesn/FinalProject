from tkinter import filedialog; import tkinter as tk
from socket import *; from threading import *
from videoplayer import *

Server = '10.200.4.67' #Replace with Server IP
Port = 12345

#Create socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#Connect client to server
clientSocket.connect((Server, Port))

def MainScreen(userName):
    for widget in mainFrame.winfo_children():
        widget.pack_forget()

    welcomeLabel.pack()
    welcomeLabel.config(text='Welcome! Browse Videos or Upload a Video.')

    browseButton = tk.Button(text='Browse Videos')
    browseButton.pack(pady=5)
    uploadButton = tk.Button(text='Upload Video',command=UploadVideo)
    uploadButton.pack(pady=5)



def SendLoginInfo(userName,userPass):
    clientSocket.send('login'.encode())
    while True:
        request = clientSocket.recv(1024).decode()
        if request == 'username':
            clientSocket.send(userName.encode())
        elif request == 'password':
            clientSocket.send(userPass.encode())
        elif request == 'incorrect':
            welcomeLabel.pack()
            welcomeLabel.config(text='Username or Password is Incorrect')
            break
        elif request == 'login':
            MainScreen(userName)
            break

def SendSignupInfo(userName,userPass):
    clientSocket.send('signup'.encode())
    while True:
        request = clientSocket.recv(1024).decode()
        if request == 'username':
            clientSocket.send(userName.encode())
        elif request == 'password':
            clientSocket.send(userPass.encode())
        elif request == 'reject':
            welcomeLabel.pack()
            welcomeLabel.config(text='Username is Already Taken')
            break
        elif request == 'signup':
            LoginScreen()
            break


def LoginScreen():
    for widget in mainFrame.winfo_children():
        widget.pack_forget()
    userName = tk.StringVar()
    userLabel = tk.Label(mainFrame, text='Enter Username:')
    userLabel.pack(pady=2)
    userEntry = tk.Entry(mainFrame,textvariable=userName)
    userEntry.pack(pady=5)
    userEntry.focus()
    
    userPass = tk.StringVar()
    passLabel = tk.Label(mainFrame,text='Enter Password:')
    passLabel.pack(pady=2)
    passEntry = tk.Entry(mainFrame,textvariable=userPass)
    passEntry.pack(pady=5)

    sendLoginButton = tk.Button(text='Log In',command= lambda: SendLoginInfo(userName.get(),userPass.get()))
    sendLoginButton.pack(pady=5)


def SignupScreen():
    for widget in mainFrame.winfo_children():
        widget.pack_forget()
    userName = tk.StringVar()
    userLabel = tk.Label(mainFrame, text='Choose Username:')
    userLabel.pack(pady=2)
    userEntry = tk.Entry(mainFrame,textvariable=userName)
    userEntry.pack(pady=5)
    userEntry.focus()

    userPass = tk.StringVar()
    passLabel = tk.Label(mainFrame,text='Choose Password:')
    passLabel.pack(pady=2)
    passEntry = tk.Entry(mainFrame,textvariable=userPass)
    passEntry.pack(pady=5)

    SignupButton.pack(pady=5)
    SignupButton.config(command= lambda: SendSignupInfo(userName.get(),userPass.get()))


def UploadVideo():
    clientSocket.send('put'.encode())
    fileName = filedialog.askopenfilename(title='Select a Video File',filetypes=[('Video Files',"*.mp4;*.avi;*.mkv;*.mov"),('All Files','*.*')])
    file = open(fileName,'rb')
    while True:
        request = clientSocket.recv(1024).decode()
        if request == 'filename':
            fileShort = fileName.split('/')[-1]
            clientSocket.send(fileShort.encode())
        elif request == 'file':
            clientSocket.sendfile(file)
            uploadLabel = tk.Label(mainFrame,text='Video Succesfully Uploaded')
            uploadLabel.pack(pady=5)
        file.close()
        return
    

root = tk.Tk()
root.title('Login')
root.state('zoomed')

mainFrame = tk.Frame(root)
mainFrame.pack()

welcomeLabel = tk.Label(mainFrame,text='Welcome! Please Log in if you already have an account, or sign up to create one.')
welcomeLabel.pack()

loginButton = tk.Button(mainFrame,text='Log In',command=LoginScreen)
loginButton.pack(pady=5)

SignupButton = tk.Button(mainFrame,text='Sign Up',command=SignupScreen)
SignupButton.pack(pady=5)



root.mainloop()