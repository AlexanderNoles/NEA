#This is a test to try and remove the dependency on pygame
import tkinter as tk

window = tk.Tk()
window.overrideredirect(True)
window.overrideredirect(False)
window.attributes('-fullscreen',True)

w = tk.Canvas(window)
w.place(x=0,y=0)
w.create_rectangle(1,1, 1, 1, fill="red",outline="red")

window.mainloop()
