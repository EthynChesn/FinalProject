import tkinter as tk; from tkinter import filedialog;import tkinter.font
import vlc
import sys

class VideoPlayer:
    def __init__(self,root):
        self.root = root
        self.root.title('Video Player')

        self.stop = False

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.video_panel = tk.Frame(root,bg='black')
        self.video_panel.pack(fill=tk.BOTH,expand=1)

        self.controls = tk.Frame(root)
        self.controls.pack(fill=tk.X,padx = 10, pady = 5)
        
        self.pause_button = tk.Button(self.controls,text='   | |   ',command=self.pause_video)
        self.pause_button.config(font=('Helvetica',10,'bold'))
        self.pause_button.pack(side=tk.LEFT,padx=5)

        self.replay_button = tk.Button(self.controls,text=' \u21BA ',command=self.replay_video)
        self.replay_button.config(font=('Helvetica',20))
        self.replay_button.pack(side=tk.LEFT,padx=5)

        self.volume_slider = tk.Scale(self.controls, from_=0, to=100,orient=tk.HORIZONTAL, label="Volume",command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=5)


    def set_video_panel(self):
        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.video_panel.winfo_id())
        elif sys.platform == "win32":
            self.player.set_hwnd(self.video_panel.winfo_id())
        elif sys.platform == "darwin":
            self.player.set_nsobject(self.video_panel.winfo_id())

    def play_video(self):
        self.player.play()
    
    def replay_video(self):
        self.player.stop()
        self.player.play()

    def pause_video(self):
        if self.player.is_playing():
            self.pause_button.config(text='   \u25B6   ')
        else:
            self.pause_button.config(text='   | |   ')
        self.player.pause()
        

    def open_file(self,fileName=None):
        if fileName is None:
            self.filename = filedialog.askopenfilename(title='Select a Video File',filetypes=[('Video Files',"*.mp4;*.avi;*.mkv;*.mov"),('All Files','*.*')])
        else:
            self.filename = fileName
        if self.filename:
            media = self.instance.media_new(self.filename)
            self.player.set_media(media)
            self.set_video_panel()

    def set_volume(self, value):
        self.player.audio_set_volume(int(value))

        
if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    player = VideoPlayer(root)
    player.open_file()
    player.play_video()
    root.mainloop()

