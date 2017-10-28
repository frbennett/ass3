from tkinter import *



class interval_bar(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent, height =30)
        self.num_rect = 6
        self.score = 0
        self.rectangle = []
        height = 10
        width = 50
        for i in range(self.num_rect):
            self.rectangle.append(self.create_rectangle(width * i, 10, width + width * i, height + 10, fill="steel blue", outline="steel blue", tag='BOX'))

    def update_score(self):
        if self.score == self.num_rect:
            for i in range(self.num_rect):
                self.itemconfig(self.rectangle[i], fill="steel blue")
                self.score = 0
        else:
            self.itemconfig(self.rectangle[self.score], fill="red")
            self.score += 1

    def reset(self):
        for i in range(self.num_rect):
            self.itemconfig(self.rectangle[i], fill="steel blue")
            self.score = 0






