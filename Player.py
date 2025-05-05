import tkinter as tk
from tkinter import filedialog
import vlc
import sys

class VideoPlayer:
    def __init__(self,root):
        self.root = root
        self.root.title('Video Player')

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.video_panel = tk.Frame(root,bg='black')
        self.video_panel.pack(fill=tk.BOTH,expand=1)

        self.controls = tk.Frame(root)
        self.controls.pack(fill=tk.X,padx = 10, pady = 5)
        self.isPlaying = False

        #self.play_button = tk.Button(self.controls,text='Play',command=self.play_video)
        #self.play_button.pack(side=tk.LEFT,padx=5)
        self.pause_button = tk.Button(self.controls,text='Pause',command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT,padx=5)
    
    def set_video_panel(self):
        self.player.set_hwnd(self.video_panel.winfo_id())

    def play_video(self):
        self.isPlaying = True
        self.player.play()
    
    def pause_video(self):
        self.player.pause()
        if self.isPlaying:
            self.pause_button.config(text = 'Play')
        else:
            self.pause_button.config(text = 'Pause')

    def open_file(self):
        self.filename = filedialog.askopenfilename(title='Select a Video File',filetypes=[('Video Files',"*.mp4;*.avi;*.mkv;*.mov"),('All Files','*.*')])
        if self.filename:
            media = self.instance.media_new(self.filename)
            self.player.set_media(media)
            self.set_video_panel()

if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    player = VideoPlayer(root)
    player.open_file()
    player.play_video()
    root.mainloop()

