import tkinter as tk
import numpy as np
from PIL import ImageTk, Image

class Window():
    pixel_scale = 1
    last_key_pressed = None
    
    def __init__(self, height, width, default_colour, title):   #Creates the intial image and sets intial values
        self.height = int(height)
        self.width = int(width)
        self.title = title
        self.default_colour = default_colour
        self.window = create_tkinter_window(self.height, self.width, self.title)
        self.screen = create_canvas(self.window)
        self.layers = []
        self.layers.append(self.Layer(self,self.height,self.width,self.default_colour)) #Create the background layer
        
    class Layer():  #Layer Objects

        def __init__(self,window,height,width,default_colour):
            self.height = height
            self.width = width
            self.default_colour = default_colour
            self.layer_num = len(window.layers)
            self.array = create_image_array(height,width,default_colour)
            self.generated_image = ImageTk.PhotoImage(master = window.screen,image=Image.fromarray(self.array))
            self.image = window.screen.create_image(width,height,image=self.generated_image)

    def move_layer(self,new_coords,layer_num = 0):  #Moves a layer to a given position
        #Get Current Top Left of layer Coords
        old_coords = self.screen.coords(self.layers[layer_num].image)
        old_coords[0] = old_coords[0] - (self.layers[layer_num].height/2)
        old_coords[1] = old_coords[1] - (self.layers[layer_num].width/2)
        #Move to new position
        self.screen.move(self.layers[layer_num].image,new_coords[0] - old_coords[0],new_coords[1] - old_coords[1])

    def delete_layer(self,layer):
        self.screen.delete(self.layers[layer].image)
        self.layers.pop(layer)       

    def init_input(self):
        def on_key_press(event):
            self.last_key_pressed = event.char
            if self.last_key_pressed == '':
                self.last_key_pressed = 'esc'
        def on_key_up(event):
            self.last_key_pressed = None
        self.window.bind('<KeyPress>', on_key_press)
        self.window.bind('<KeyRelease>', on_key_up)

    def reset(self, layer_num = 0):    #Resets the entered layer, used so the line below doesn't need to be typed everytime
        self.layers[layer_num].array = create_image_array(self.layers[layer_num].height,self.layers[layer_num].width,self.layers[layer_num].default_colour)

    def update(self, layer_num = 0):   #Updates an entered layer
        try:
            self.layers[layer_num].generated_image = ImageTk.PhotoImage(master = self.screen,image=Image.fromarray(self.layers[layer_num].array)) #Generate a updated image from the image array
            self.screen.itemconfig(self.layers[layer_num].image, image = self.layers[layer_num].generated_image)
        except IndexError:
            print("Invalid Layer")
        self.window.update()

    def set_pixel(self, coords, colour, layer_num=0): #Change a pixel in the image array and then update the image accordingly
        coords[0] = (coords[0] * self.pixel_scale) - (self.pixel_scale - 1)
        coords[1] = (coords[1] * self.pixel_scale) - (self.pixel_scale - 1)
        for x in range(coords[0],coords[0]+self.pixel_scale):
            for y in range(coords[1],coords[1]+self.pixel_scale):
                try:
                    self.layers[layer_num].array[y,x] = colour
                except IndexError:
                    pass   

    def set_fullscreen(self, boolean):  #Turns fullscreen on and off based on boolean
        self.window.overrideredirect(True)
        self.window.overrideredirect(False)
        self.window.attributes('-fullscreen',boolean)
        self.screen.pack(fill="both", expand=True)
        #for i in range(1,len(self.layers)):
            #self.screen.move(self.layers[i].image,self.width,self.height)
            #self.move_layer([self.width,self.height],i)

    def set_pixel_scale(self, num): #Used to change the pixel scale
        self.pixel_scale = num

    def quit(self):
        for i in range(0,len(self.layers)):
            self.reset(i)
        self.window.destroy()
        del self

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


#import ctypes
#user32 = ctypes.windll.user32
#screen_width = user32.GetSystemMetrics(0)
#screen_height = user32.GetSystemMetrics(1)
#window = Window(screen_height/2,screen_width/2,95,"Cringe")
#window.set_fullscreen(True)
#window.update()
#window.layers.append(window.Layer(window,100,100,255))
#window.update(layer_num = 1)
#while True:
    #window.move_layer([10,10],layer_num = 1)
    #window.update(layer_num=1)


