import tkinter as tk

class Window():
    pixel_scale = 1

    def __init__(self, height, width, title):
        self.height = height
        self.width = width
        self.title = title
        self.window = create_tkinter_window(self.height, self.width, self.title)
        self.screen = create_canvas(self.window)

    def set_pixel(self, coords, colour):
        coords[0] = (coords[0] * self.pixel_scale) - (self.pixel_scale - 1)
        coords[1] = (coords[1] * self.pixel_scale) - (self.pixel_scale - 1)
        self.screen.create_rectangle(coords[1],coords[0], coords[1]+self.pixel_scale, coords[0]+self.pixel_scale, fill = colour, outline="")

    def set_fullscreen(self, boolean):
        self.window.overrideredirect(True)
        self.window.overrideredirect(False)
        self.window.attributes('-fullscreen',boolean)
        self.screen.pack(fill="both", expand=True)

    def set_pixel_scale(self, num):
        self.pixel_scale = num


def create_tkinter_window(height, width, title):
    window = tk.Tk()
    window.title(title)
    window.geometry(str(width) + "x" + str(height))
    #window.overrideredirect(1) #Removes the Titlebar
    return window

def create_canvas(tkinter_window):
    canvas = tk.Canvas(tkinter_window, bg="black")
    canvas.pack(fill="both",expand=True)
    return canvas

window = Window(1,1,"Window Test")
window.set_fullscreen(True)
for i in range(0,100):                   #For comparisions of pixel scales
    window.set_pixel([10,10],"white")
    window.set_pixel_scale(i)

