import tkinter as tk
import numpy as np
from PIL import ImageTk, Image

class Window():
    pixel_scale = 1

    def __init__(self, height, width, default_colour, title):   #Creates the intial image and sets intial values
        self.height = height
        self.width = width
        self.title = title
        self.default_colour = default_colour
        self.window = create_tkinter_window(self.height, self.width, self.title)
        self.screen = create_canvas(self.window)
        self.image_array = create_image_array(self.height,self.width,self.default_colour)   #Create the image array
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.image_array))
        self.screen_image = self.screen.create_image(self.width/2,self.height/2,anchor="center",image=self.image) #Apply the image_array to the image

    def reset(self):    #Resets the canvas, used so the line below doesn't need to be typed everytime
        self.image_array = create_image_array(self.height,self.width,self.default_colour)

    def update(self):   #Updates the image
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.image_array))
        self.screen_image = self.screen.create_image(self.width/2,self.height/2,anchor="center",image=self.image) #Apply the image_array to the image
        self.window.update()

    def set_pixel(self, coords, colour): #Change a pixel in the image array and then update the image accordingly
        coords[0] = (coords[0] * self.pixel_scale) - (self.pixel_scale - 1)
        coords[1] = (coords[1] * self.pixel_scale) - (self.pixel_scale - 1)
        for x in range(coords[0],coords[0]+self.pixel_scale):
            for y in range(coords[1],coords[1]+self.pixel_scale):
                try:
                    self.image_array[x,y] = colour
                except IndexError:
                    pass

    def set_fullscreen(self, boolean):  #Turns fullscreen on and off based on boolean
        self.window.overrideredirect(True)
        self.window.overrideredirect(False)
        self.window.attributes('-fullscreen',boolean)
        self.screen.pack(fill="both", expand=True)

    def set_pixel_scale(self, num): #Used to change the pixel scale
        self.pixel_scale = num

def create_tkinter_window(height, width, title):    #Creates a tkinter window
    window = tk.Tk()
    window.title(title)
    window.geometry(str(width) + "x" + str(height))
    #window.overrideredirect(1) #Removes the Titlebar
    return window

def create_canvas(tkinter_window):  #Creates a tkinter canvas
    canvas = tk.Canvas(tkinter_window, bg="black")
    canvas.pack(fill="both",expand=True)
    return canvas

def create_image_array(height,width,colour): #Creates the intial image array
    image_array = np.zeros([height+1,width+1,3],dtype=np.uint8)
    image_array.fill(colour)
    return image_array
    
import ctypes
user32 = ctypes.windll.user32
window = Window(user32.GetSystemMetrics(1),user32.GetSystemMetrics(0),0,"Test Window")
window.set_fullscreen(True)
window.set_pixel([50,50],(255,0,0))
#window.reset()
window.update()




