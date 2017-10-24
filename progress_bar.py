from tkinter import *



class interval_bar(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent, width=1000)
        self.num_rect = 6
        self.score = 0
        self.rectangle = []
        for i in range(self.num_rect):
            self.rectangle.append(self.create_rectangle(50 * i, 50, 50 + 50 * i, 30 + 50, fill="steel blue", tag='BOX'))

    def update_score(self):
        if self.score == self.num_rect:
            for i in range(self.num_rect):
                self.itemconfig(self.rectangle[i], fill="steel blue")
                self.score = 0
        else:
            self.itemconfig(self.rectangle[self.score], fill="red")
            self.score += 1




