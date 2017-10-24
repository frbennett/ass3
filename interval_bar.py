from tkinter import *
root = Tk()

canvas = Canvas(root, width =620, height = 70)
canvas.pack()
rectangle1 = canvas.create_rectangle(50,50, 100,20)
rectangle2 = canvas.create_rectangle(150,50, 100,20)
rectangle3 = canvas.create_rectangle(250,50, 100,20)
rectangle4 = canvas.create_rectangle(350,50, 100,20)
rectangle5 = canvas.create_rectangle(450,50, 100,20)
rectangle6 = canvas.create_rectangle(550,50, 100,20)
canvas.itemconfig(rectangle1, fill='steel blue')
canvas.itemconfig(rectangle2, fill='steel blue')
canvas.itemconfig(rectangle3, fill='steel blue')
canvas.itemconfig(rectangle4, fill='steel blue')
canvas.itemconfig(rectangle5, fill='steel blue')
canvas.itemconfig(rectangle6, fill='steel blue')

root.mainloop()