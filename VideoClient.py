from tkinter import filedialog; import tkinter as tk
from socket import *; from threading import *
from videoplayer import *
import pickle

Server = '10.200.4.67' #Replace with Server IP
Port = 12345
filePath = 'E:\\Downloads\\'

#Create socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#Connect client to server
clientSocket.connect((Server, Port))

def PlayVideo(fileName):
    mainFrame.pack_forget()
    player = VideoPlayer(root)
    player.open_file(fileName)
    player.play_video()


def GetVideo(fileName,uploader):
    clientSocket.send('get'.encode())
    while True:
        request = clientSocket.recv(1024).decode()
        if request == 'filename':
            clientSocket.send(fileName.encode())
        request = clientSocket.recv(1024).decode()
        if request == 'download':
            with clientSocket:
                with open(filePath + 'temp-' + fileName,'wb') as file:
                    while chunk:= clientSocket.recv(1 << 20):
                        file.write(chunk)
                        break
                    PlayVideo(filePath + 'temp-' + fileName)

def ListVideos():
    for widget in mainFrame.winfo_children():
        widget.pack_forget()
    clientSocket.send('list'.encode())
    listdata = clientSocket.recv(1024)
    videolist = pickle.loads(listdata)
    for video in videolist:
        vButton = tk.Button(mainFrame,text=video + ' By ' + videolist[video],command=lambda:GetVideo(video,videolist[video]))
        vButton.pack(pady=5)
    backButton = tk.Button(mainFrame,text='Back',command=MainScreen)
    backButton.pack(pady=10)

def MainScreen():
    root.title('Home')
    for widget in mainFrame.winfo_children():
        widget.pack_forget()

    welcomeLabel.pack()
    welcomeLabel.config(text='Welcome! Browse Videos or Upload a Video.')

    browseButton = tk.Button(mainFrame,text='Browse Videos',command=ListVideos)
    browseButton.pack(pady=5)
    uploadButton = tk.Button(mainFrame,text='Upload Video',command=UploadVideo)
    uploadButton.pack(pady=5)
    deleteButton = tk.Button(mainFrame,text='Delete Video')
    deleteButton.pack(pady=5)

    signoutButton = tk.Button(mainFrame,text='Log Out',command=LoginScreen)
    signoutButton.pack(pady=10)



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
            MainScreen()
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
            welcomeLabel.pack(side=tk.TOP)
            welcomeLabel.config(text='Username is Already Taken')
            break
        elif request == 'signup':
            LoginScreen()
            break


def LoginScreen():
    root.title('Log in')
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

    sendLoginButton = tk.Button(mainFrame,text='Log In',command= lambda: SendLoginInfo(userName.get(),userPass.get()))
    sendLoginButton.pack(pady=5)

    signupLabel = tk.Label(mainFrame,text="Don't have an Account?")
    signupLabel.pack(pady=10)
    SignupButton.config(command=SignupScreen)
    SignupButton.pack()

def SignupScreen():
    root.title('Sign up')
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

    loginLabel = tk.Label(mainFrame,text='Already have an Account?')
    loginLabel.pack(pady=10)
    loginButton.config(command=LoginScreen)
    loginButton.pack()


def UploadVideo():
    clientSocket.send('put'.encode())
    fileName = filedialog.askopenfilename(title='Select a Video File',filetypes=[('Video Files',"*.mp4;*.avi;*.mkv;*.mov"),('All Files','*.*')])
    file = open(fileName,'rb')
    while True:
        request = clientSocket.recv(1024).decode()
        if request == 'filename':
            fileShort = fileName.split('/')[-1]
            clientSocket.send(fileShort.encode())
        if request == 'reject':
            rejectLabel=tk.Label(mainFrame,text='A Video With That Name Already Exists.')
            rejectLabel.pack()
        if request == 'file':
            while chunk:=file.read(1 << 20):
                clientSocket.sendall(chunk)
            uploadLabel = tk.Label(mainFrame,text='File Uploaded succesfully')
            uploadLabel.pack()
            break
    file.close()
    
    

root = tk.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

root.title('Log in or Sign Up')
root.state('zoomed')

mainFrame = tk.Frame(root)
mainFrame.pack(pady=screenHeight/3)

welcomeLabel = tk.Label(mainFrame,text='Welcome! Please Log in if you already have an account, or sign up to create one.')
welcomeLabel.pack()

loginButton = tk.Button(mainFrame,text='Log In',command=LoginScreen)
loginButton.pack(pady=5)

SignupButton = tk.Button(mainFrame,text='Sign Up',command=SignupScreen)
SignupButton.pack(pady=5)


root.mainloop()