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


path = './images/companions/buffalo_large.gif'
# path = './images/companions/penguin.png'
#path = 'useless.gif'

class InfoPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid(sticky=SE)

        self.score = Label(self, text='0')
        self.score.grid(row=0, column=0, sticky=NW)
        self.score.config(font=("Arial", 30, "bold"), justify=LEFT, width=3)

        self.moves = Label(self, text='')
        self.moves.grid(row=1, column=0, sticky=NW)
        self.moves.config(font=("Arial", 30, "bold"),fg = 'blue', justify=LEFT, width=3)

        img = Image.open(path)
        resize = img.resize((200, 200), Image.ANTIALIAS)
        self.companion_img = ImageTk.PhotoImage(resize)

        self.label = Label(self, image=self.companion_img)
        self.label.grid(row=0, rowspan=2, column=1, columnspan=1)

        self.objectives = ObjectivesView(self, image_manager = ImageManager('images/dots/', loader=load_image))
        self.objectives.grid(row=0, column=2, sticky=NE)



    def change_text(self, event):
        self.score.config(text='change the value')
        self.event_generate("<<Foo>>", when="tail")
        print('hello')


    def set_score(self, value):
        value_str = str(value)
        self.score.config(text=value_str)

    def set_moves(self, value):
        value_str = str(value)
        self.moves.config(text=value_str)

    def reset_score(self):
        self.score.config(text="0")


#app = InfoPanel('InfoPanel')
#app.mainloop()

