from tkinter import *
from random import *

window = Tk()
window.title('Maze Renderer')

def create_grid(window):
    width = 1900
    height = 1000
    canvas = Canvas(window, background='white', width=width, height=height)


    for line in range(0, width, 10):
        canvas.create_line([(line, 0), (line, height)], fill='white', tags='grid_line_w')

    for line in range(0, height, 10):
        canvas.create_line([(0, line), (width, line)], fill='white', tags='grid_line_h')

    canvas.pack()

create_grid(window)
window.mainloop()
