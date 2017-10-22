from tkinter import *
import os
from PIL import ImageTk, Image

path = './images/companions/penguin.gif'
# path = './images/companions/penguin.png'
#path = 'useless.gif'

class InfoPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid()
        #self.master.title(title)

        self.label1 = Label(self, text='Hello')
        self.label1.grid(row=0, column=0)
        self.label1.bind('<Button-1>', self.change_text)

        img = Image.open(path)
        resize = img.resize((200, 200), Image.ANTIALIAS)
        self.companion_img = ImageTk.PhotoImage(resize)

        self.label = Label(self, image=self.companion_img)
        self.label.grid(row=2, rowspan=6, column=4, columnspan=3)
        self.label.bind('<Button-1>', self.depositCallBack)

    def depositCallBack(self, event):
        # self.depositLabel.config(text='the test has changed')
        print('hello')

    def change_text(self, event):
        self.label1.config(text='change the value')
        self.event_generate("<<Foo>>", when="tail")
        print('hello')

    


#app = InfoPanel('InfoPanel')
#app.mainloop()

