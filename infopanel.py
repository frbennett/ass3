from tkinter import *
import os
from PIL import ImageTk, Image
from view import *
from util import create_animation, ImageManager


try:
    from PIL import ImageTk, Image

    HAS_PIL = True

except ImportError:
    HAS_PIL = False
def load_image_pil(image_id, size, prefix, suffix='.gif'):
    """Returns a tkinter photo image

    Parameters:
        image_id (str): The filename identifier of the image
        size (tuple<int, int>): The size of the image to load
        prefix (str): The prefix to prepend to the filepath (i.e. root directory
        suffix (str): The suffix to append to the filepath (i.e. file extension)
    """
    width, height = size
    file_path = os.path.join(prefix, f"{width}x{height}", image_id + suffix)
    return ImageTk.PhotoImage(Image.open(file_path))


def load_image_tk(image_id, size, prefix, suffix='.gif'):
    """Returns a tkinter photo image

    Parameters:
        image_id (str): The filename identifier of the image
        size (tuple<int, int>): The size of the image to load
        prefix (str): The prefix to prepend to the filepath (i.e. root directory
        suffix (str): The suffix to append to the filepath (i.e. file extension)
    """
    width, height = size
    file_path = os.path.join(prefix, f"{width}x{height}", image_id + suffix)
    return tk.PhotoImage(file=file_path)


# This allows you to simply load png images with PIL if you have it,
# otherwise will default to gifs through tkinter directly
load_image = load_image_pil if HAS_PIL else load_image_tk  # pylint: disable=invalid-name


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

        self.objectives = ObjectivesView(self, image_manager = ImageManager('images/dots/', loader=load_image))
        self.objectives.grid(row=2, column=10)


    def depositCallBack(self, event):
        # self.depositLabel.config(text='the test has changed')
        print('hello')

    def change_text(self, event):
        self.label1.config(text='change the value')
        self.event_generate("<<Foo>>", when="tail")
        print('hello')


    def set_score(self, value):
        value_str = str(value)
        self.label1.config(text=value_str)



