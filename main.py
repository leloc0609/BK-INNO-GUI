import time
from tkinter import *
from PIL import Image, ImageTk
WELCOME = 'PRESS LOGO TO CONTINUE'
class Fullscreen_Window:
    def __init__(self):
        self.tk = Tk()
        self.tk.config(background="white")
        self.state = True
        self.tk.attributes("-fullscreen", self.state)
        self.tk.bind("<F11>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

class Init_Screen:
    def __init__(self, master):
        self.master= master
        self.index = 0
        self.interval = 200
        self.labelText = ''

        #Put every attributes define before this
        self.createWidgets()

    def createWidgets(self):
        self.logoInitFrame = Frame(self.master, background="white")
        self.logoInitFrame.place(in_=self.master, anchor="c", relx=.5, rely=.5)
        self.logo = ImageTk.PhotoImage(Image.open("D:\BK INNP\code\BKINNO_logo.png"))
        self.logoInitButton = Button(self.logoInitFrame, image=self.logo, border=0, borderwidth=0, command=self.initButtonAction)
        self.logoInitButton.grid(column=0, row=0, pady=10)
        self.label = Label(self.logoInitFrame, text=self.labelText, background="white", font= ('Helvatica', 30, 'bold'))
        self.label.grid(column=0, row=1, pady=10)
        self.label.after(self.interval, self.updateInitialLabel)

    def updateInitialLabel(self):
        self.labelText= self.labelText + WELCOME[self.index]
        self.label.config(text=self.labelText)
        self.index += 1
        if self.index==len(WELCOME):
            self.index=0
            self.labelText=''

        self.label.after(self.interval, self.updateInitialLabel)

    def initButtonAction(self):
        self.logoInitFrame.destroy()
        self.logoInitFrame = Frame(self.master, background="white")
        self.logoInitFrame.place(in_=self.master, anchor="c", relx=.5, rely=.5)
        self.logo = ImageTk.PhotoImage(Image.open("D:\BK INNP\code\BKINNO_logo.png"))
        self.logoInitButton = Button(self.logoInitFrame, image=self.logo, border=0, borderwidth=0)

if __name__ == '__main__':
    w = Fullscreen_Window()
    initScreen = Init_Screen(w.tk)
    w.tk.mainloop()