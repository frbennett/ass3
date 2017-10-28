"""
CSSE1001 Assignment 3
Semester 2, 2017
"""

# There are a number of jesting comments in the support code
# They should not be taken seriously. Keep it fun folks :D
# Students are welcome to add their own source code humour, provided it remains civil

import tkinter as tk
from tkinter.messagebox import showinfo
import os
import random
import infopanel
import progress_bar
import game_parameters

try:
    from PIL import ImageTk, Image

    HAS_PIL = True

except ImportError:
    HAS_PIL = False

from view import GridView, ObjectivesView
from game import DotGame, ObjectiveManager
from dot import BasicDot
from dot import WildcardDot
from util import create_animation, ImageManager

# Fill these in with your details
__author__ = "Justine Bennett (s4482360)"
__email__ = "justine.e.bennett@gmail.com"
__date__ = ""

__version__ = "1.1.1"


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

DEFAULT_ANIMATION_DELAY = 0  # (ms)
ANIMATION_DELAYS = {
    # step_name => delay (ms)
    'ACTIVATE_ALL': 50,
    'ACTIVATE': 100,
    'ANIMATION_BEGIN': 300,
    'ANIMATION_DONE': 0,
    'ANIMATION_STEP': 200
}


# Define your classes here
# You may edit as much of DotsApp as you wish
class DotsApp:
    """Top level GUI class for simple Dots & Co game"""

    def __init__(self, master):
        """Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget
        """
        self._master = master

        self._playing = True

        self._image_manager = ImageManager('images/dots/', loader=load_image)

        # Game
        self.level = game_parameters.set_game_paramters()
        self.current_level = 0
        self.num_levels = len(self.level.levels)
        counts = self.level.levels[self.current_level]['counts']
        random.shuffle(counts)
        # randomly pair counts with each kind of dot
        objectives = zip([BasicDot(1), BasicDot(2), BasicDot(4), BasicDot(3)], counts)

        self.initial_objectives = [(BasicDot(1), counts[0]), (BasicDot(2), counts[1]), (BasicDot(4), counts[2]), (BasicDot(3), counts[3])]

        self._objectives = ObjectiveManager(objectives)


        # Game
        dead_cells = self.level.levels[self.current_level]['dead_cells']
        basic_dots = self.level.levels[self.current_level]['basic_dots']
        wild_dots = self.level.levels[self.current_level]['wild_dots']

        self._game = DotGame({BasicDot: basic_dots, WildcardDot: wild_dots}, objectives=self._objectives, kinds=(1, 2, 3, 4),
                             size=self.level.levels[self.current_level]['size'],
                             dead_cells=dead_cells)
        self.moves = self.level.levels[self.current_level]['moves']
        self._game.set_moves(self.moves)


        # The following code may be useful when you are implementing task 2:
         #for i in range(0, 4):
             #for j in range(0, 2):
                 #position = i, j
                 #self._game.grid[position].set_dot(BasicDot(3))
         #self._game.grid[(7, 3)].set_dot(BasicDot(1))

        # Grid View
        self._grid_view = GridView(master, size=self._game.grid.size(), image_manager=self._image_manager)
        self._grid_view.pack()
        self._grid_view.draw(self._game.grid)
        self.draw_grid_borders()

        # Events
        self.bind_events()

        # Set initial score again to trigger view update automatically
        self._refresh_status()

    def draw_grid_borders(self):
        """Draws borders around the game grid"""

        borders = list(self._game.grid.get_borders())

        # this is a hack that won't work well for multiple separate clusters
        outside = max(borders, key=lambda border: len(set(border)))

        for border in borders:
            self._grid_view.draw_border(border, fill=border != outside)

    def bind_events(self):
        """Binds relevant events"""
        self._grid_view.on('start_connection', self._drag)
        self._grid_view.on('move_connection', self._drag)
        self._grid_view.on('end_connection', self._drop)

        self._game.on('reset', self._refresh_status)
        self._game.on('complete', self._drop_complete)

        self._game.on('connect', self._connect)
        self._game.on('undo', self._undo)

    def _animation_step(self, step_name):
        """Runs for each step of an animation
        
        Parameters:
            step_name (str): The name (type) of the step    
        """
        print(step_name)
        self._refresh_status()
        self.draw_grid()


    def animate(self, steps, callback=lambda: None):
        """Animates some steps (i.e. from selecting some dots, activating companion, etc.
        
        Parameters:
            steps (generator): Generator which yields step_name (str) for each step in the animation
        """

        if steps is None:
            steps = (None for _ in range(1))

        animation = create_animation(self._master, steps,
                                     delays=ANIMATION_DELAYS, delay=DEFAULT_ANIMATION_DELAY,
                                     step=self._animation_step, callback=callback)
        animation()

    def _drop(self, position):  # pylint: disable=unused-argument
        """Handles the dropping of the dragged connection

        Parameters:
            position (tuple<int, int>): The position where the connection was
                                        dropped
        """
        if not self._playing:
            return

        if self._game.is_resolving():
            return

        self._grid_view.clear_dragged_connections()
        self._grid_view.clear_connections()

        self.animate(self._game.drop())

    def _connect(self, start, end):
        """Draws a connection from the start point to the end point

        Parameters:
            start (tuple<int, int>): The position of the starting dot
            end (tuple<int, int>): The position of the ending dot
        """

        if self._game.is_resolving():
            return
        if not self._playing:
            return
        self._grid_view.draw_connection(start, end,
                                        self._game.grid[start].get_dot().get_kind())

    def _undo(self, positions):
        """Removes all the given dot connections from the grid view

        Parameters:
            positions (list<tuple<int, int>>): The dot connects to remove
        """
        for _ in positions:
            self._grid_view.undo_connection()

    def _drag(self, position):
        """Attempts to connect to the given position, otherwise draws a dragged
        line from the start

        Parameters:
            position (tuple<int, int>): The position to drag to
        """

        if self._game.is_resolving():
            return
        if not self._playing:
            return

        tile_position = self._grid_view.xy_to_rc(position)

        if tile_position is not None:
            cell = self._game.grid[tile_position]
            dot = cell.get_dot()

            if dot and self._game.connect(tile_position):
                self._grid_view.clear_dragged_connections()
                return

        kind = self._game.get_connection_kind()

        if not len(self._game.get_connection_path()):
            return

        start = self._game.get_connection_path()[-1]

        if start:
            self._grid_view.draw_dragged_connection(start, position, kind)

    @staticmethod
    def remove(*_):
        """Deprecated in 1.1.0"""
        raise DeprecationWarning("Deprecated in 1.1.0")

    def draw_grid(self):
        """Draws the grid"""
        self._grid_view.draw(self._game.grid)

    def set_level(self):
        """ Set up a new level of the game"""

    def reset(self,info, pbar, step):
        score = 0
        """Resets the game"""
        print("resetting " + step)
        if step == 'new_game' :
            info.reset_score()
            self.current_level = 0
            score = 0
        if step == 'new_level':
            score = self._game.get_score()

        counts = self.level.levels[self.current_level]['counts']
        random.shuffle(counts)
        # randomly pair counts with each kind of dot
        objectives = zip([BasicDot(1), BasicDot(2), BasicDot(4), BasicDot(3)], counts)

        self.initial_objectives = [(BasicDot(1), counts[0]), (BasicDot(2), counts[1]), (BasicDot(4), counts[2]),
                                   (BasicDot(3), counts[3])]

        self._objectives = ObjectiveManager(objectives)
        random.shuffle(counts)
        # randomly pair counts with each kind of dot
        objectives = zip([BasicDot(1), BasicDot(2), BasicDot(4), BasicDot(3)], counts)

        self.initial_objectives = [(BasicDot(1), counts[0]), (BasicDot(2), counts[1]), (BasicDot(4), counts[2]),
                                   (BasicDot(3), counts[3])]

        self._objectives = ObjectiveManager(objectives)
        dead_cells = self.level.levels[self.current_level]['dead_cells']
        basic_dots = self.level.levels[self.current_level]['basic_dots']
        wild_dots = self.level.levels[self.current_level]['wild_dots']
        self._game = DotGame({BasicDot: basic_dots, WildcardDot: wild_dots}, objectives=self._objectives, kinds=(1, 2, 3, 4),
                             size=self.level.levels[self.current_level]['size'],
                             dead_cells=dead_cells)
        moves = self.level.levels[self.current_level]['moves']
        self._game.set_moves(moves)
        self._grid_view.destroy()
        self._grid_view = GridView(self._master, size=self._game.grid.size(), image_manager=self._image_manager)
        self._grid_view.pack()
        self._grid_view.draw(self._game.grid)
        self.draw_grid_borders()
        self._game._score = score
        info.set_moves(moves)
        info.objectives.draw(self.initial_objectives)
        pbar.reset()


        # Events
        self.bind_events()

        # Set initial score again to trigger view update automatically
        self._refresh_status()

    def check_game_over(self):
        """Checks whether the game is over and shows an appropriate message box if so"""
        state = self._game.get_game_state()
        if state == self._game.GameState.WON:
            self.current_level += 1
            if self.current_level == self.num_levels :
                showinfo("Game Over!", "You won!!!")
                self._playing = False
            else :
                showinfo("Level Completed!", "Get Ready for New Level")
                self._master.event_generate("<<new_level>>", when='tail')
        elif state == self._game.GameState.LOST:
            showinfo("Game Over!",
                     f"You didn't reach the objective(s) in time. You connected {self._game.get_score()} points")
            self._playing = False

    def _drop_complete(self):
        """Handles the end of a drop animation"""

        # Useful for when implementing a companion
        # if self._game.companion.is_fully_charged():
        #     self._game.companion.reset()
        #     steps = self._game.companion.activate(self._game)
        #     self._refresh_status()
        #
        #     return self.animate(steps)

        # Need to check whether the game is over
        #raise NotImplementedError()  # no mercy for stooges
        print('drop is compler')
        print(str(self._objectives.status))
        self.updated_objectives = self._objectives.status
        self.moves = self._game.get_moves()
        print("moves ", self.moves)
        self.doit()


    def _refresh_status(self):
        """Handles change in score"""

        # Normally, this should raise the following error:
        # raise NotImplementedError()
        # But so that the game can work prior to this method being implemented,
        # we'll just print some information
        # Sometimes I believe Python ignores all my comments :(
        score = self._game.get_score()
        print("Score is now {}.".format(score))
        self.reported_score = score

    def doit(self):
        self._master.event_generate("<<update_score>>", when='tail')

        print('hello')



def doFoo(*args):
    print('hello world')

def update_score(event, current_game, info, pbar):
    #score = frame.reported_score
    print('reported score is : ')
    print("im here")
    print(current_game.reported_score)
    score = current_game.reported_score
    info.set_score(score)
    moves = current_game.moves
    info.set_moves(moves)
    pbar.update_score()
    current_game.check_game_over()
    info.objectives.draw(current_game.updated_objectives)


def hello():
    print('hello')


def setup_menu(x, current_game, info, pbar):
    menubar = tk.Menu(x)
    # create a pulldown menu, and add it to the menu bar
    filemenu = tk.Menu(menubar, tearoff=False)
    filemenu.add_command(label="Start New Game", command= lambda info=info, pbar=pbar, step='new_game' : current_game.reset(info, pbar, step))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=x.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=hello)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    x.config(menu=menubar)


def main():
    """Sets-up the GUI for Dots & Co"""
    # Write your GUI instantiation code here
    root = tk.Tk()
    root.grid()
    root.title('Dots & Co.')
    frame1 = tk.Frame(root)
    frame1.grid(row=0, column=0)
    pbar = progress_bar.interval_bar(root)
    pbar.grid(row=1, column=0)
    frame2 = tk.Frame(root)
    frame2.grid(row=2, column=0)
    info = infopanel.InfoPanel(frame1)

    current_game = DotsApp(frame2)
    objectives = current_game.initial_objectives
    info.objectives.draw(objectives)
    frame2.bind("<<update_score>>", lambda event, current_game=current_game, info=info, pbar=pbar: update_score(event, current_game, info, pbar))
    frame2.bind("<<new_level>>", lambda event, info=info, pbar=pbar, step='new_level' : current_game.reset(info, pbar, step))
    setup_menu(root,current_game, info, pbar)
    moves = current_game.moves
    info.set_moves(moves)
    root.mainloop()



if __name__ == "__main__":
    main()


