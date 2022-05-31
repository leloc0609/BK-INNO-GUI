try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

from PIL import Image, ImageTk
import CH340_relay
from serial import Serial

WELCOME = 'PRESS LOGO TO CONTINUE'

serialCommunication = Serial(CH340_relay.getPort(), baudrate=9600)
class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        tk.Tk.config(self,background="white")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.state = True
        tk.Tk.attributes(self,"-fullscreen", self.state)
        tk.Tk.bind(self,"<F11>", self.toggle_fullscreen)
        self.frames = {}
        for F in (StartPage, LockerChoosePage, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        tk.Tk.attributes(self,"-fullscreen", self.state)
        return "break"

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background="white")
        self.labelText=''
        self.createWidgets()
        self.index = 0


    def createWidgets(self):
        self.logoInitFrame = tk.Frame(self, background="white")
        self.logoInitFrame.place(in_=self, anchor="c", relx=.5, rely=.5)
        self.logo = ImageTk.PhotoImage(Image.open("D:\BK INNP\code\BKINNO_logo.png"))
        self.logoInitButton = tk.Button(self.logoInitFrame, image=self.logo, border=0, borderwidth=0,
                                        command=lambda: self.controller.show_frame("LockerChoosePage"))
        self.logoInitButton.grid(column=0, row=0, pady=10)
        self.label = tk.Label(self.logoInitFrame, text=self.labelText, background="white", font=('Helvatica', 30, 'bold'))
        self.label.grid(column=0, row=1, pady=10)
        self.label.after(200, self.updateInitialLabel)

    def updateInitialLabel(self):
        self.labelText = self.labelText + WELCOME[self.index]
        self.label.config(text=self.labelText)
        self.index += 1
        if self.index == len(WELCOME):
            self.index = 0
            self.labelText = ''

        self.label.after(200, self.updateInitialLabel)


class LockerChoosePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background="white")
        self.createWidgets()
    def createWidgets(self):
        label = tk.Label(self, text="This is page 1",)
        label.pack(side="top", fill="x", pady=10)
        button0 = tk.Button(self, text="Press to turn on relay 0",
                            command= lambda: CH340_relay.control_relay(serialCommunication,0))
        button0.pack()
        button1 = tk.Button(self, text="Press to turn on relay 1",
                            command=lambda: CH340_relay.control_relay(serialCommunication, 1))
        button1.pack()
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()