import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
import time
import random

class Window():
    pixel_scale = 1

    def __init__(self, height, width, title):
        self.height = height
        self.width = width
        self.title = title
        self.window = create_tkinter_window(self.height, self.width, self.title)
        self.screen = create_canvas(self.window)
        self.image_array = create_image_array(self.height,self.width,70)   #Create the image array
        #print(self.image_array)
        temp_image = ImageTk.PhotoImage(image=Image.fromarray(self.image_array))
        img = Image.fromarray(self.image_array)
        img.show()
        self.screen.create_image(0,0,image=temp_image)

    def reset(self):
        self.screen.delete("all")

    def update(self):
        #self.reset()
        print(self.image_array)
        temp_image = ImageTk.PhotoImage(image=Image.fromarray(self.image_array))
        self.screen.itemconfig(self.screen_image, image=temp_image)
        self.window.update() #tkinter update (not a recursive function)
        print("update run")

    def set_pixel(self, coords, colour): #Change a pixel in the image array and then update the image accordingly
        coords[0] = (coords[0] * self.pixel_scale) - (self.pixel_scale - 1)
        coords[1] = (coords[1] * self.pixel_scale) - (self.pixel_scale - 1)
        for x in range(coords[0],coords[0]+self.pixel_scale):
            for y in range(coords[1],coords[1]+self.pixel_scale):
                self.image_array[x,y] = colour
        print(self.image_array[coords[0],coords[1]])
        #self.update()

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

def create_image_array(height,width,colour):
    image_array = np.zeros([height*2,width*2,3],dtype=np.uint8)
    image_array.fill(colour)
    return image_array
    
window = Window(500,500,"bruh")

for i in range(0,100):    
    #window.set_pixel([random.randint(0,500),random.randint(0,500)],(70,70,70))
    pass
#window.update()


