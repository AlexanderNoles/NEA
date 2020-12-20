import tkinter as tk
import sqlite3
from sqlite3 import Error

from MazeGenerationNew import main
try:
    from MazeRendererNew import play_maze
    installed = True
except ImportError: #Pygame is not installed
    installed = False
    
window = tk.Tk()
try:
    window.state("zoomed")
except:
    window.state("normal")
window.title("Maze Game")
window.geometry("500x500")
root_menu = tk.Menu(window)
window.config(menu = root_menu)
default_state = "start"

import ctypes
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

user_id = 0

number_of_mazes = 2

#CREATE
def change_state(state,*args):
    des()
    if state == "start":
        title = tk.Label(window, text = "\n Maze Game \n Version 1.1 \n", bg = "white", borderwidth=1, relief="groove").pack(fill = "x",pady=(250,20))
        enter_button = tk.Button(window, text = "Enter",bg = "white",width=30, command = lambda: change_state("username")).pack()
        exit_button = tk.Button(window, text = "Exit",width=30, bg = "white", fg = "red", command = lambda: exit()).pack(pady=3)
        if not installed:
            error_message = tk.Label(window,text="[Pygame not installed, Pygame is required for current version]",fg="red").pack(side="bottom",pady = 20)
    if state == "username":
        title = tk.Label(window, text = "\n Accounts \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        top_seperator = tk.Canvas(window, height=50,width=0).pack()
        guest_button = tk.Button(window, text = "Play as Guest",bg = "white",width=30,height=2, command = lambda u = "guest": set_user_id(u,True)).pack(pady=3)
        for i in range(0,0): #will eventually base the amount of buttons off the amount of users
            username_button = tk.Button(window,text="stand-in",bg = "white",width=30,height=2)
            username_button.config(command = lambda u = username_button: set_user_id(u,False))
            username_button.pack(pady=3)
        create_new_button = tk.Button(window,text="+",bg = "white",width=10, command = lambda: change_state("new user")).pack(pady=3)
    elif state == "new user":
        pass
    elif state == "maze select":
        title = tk.Label(window, text = "\n Maze Select \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        lines = load_completed_levels()
        normal_maze_button = tk.Button(window, text = "\n  Normal-Style Maze  \n",bg = "white",relief = 'groove',width=30, command = lambda: create_levels(1,30,4,"Normal Maze","normal",lines)).pack(pady=(50,10))
        circular_maze_button = tk.Button(window, text = "\n Labyrinth Maze \n",bg = "white",relief = 'groove',width=30,command = lambda: create_levels(1,30,4,"Labyrinth Maze","circular",lines)).pack(pady=10)
        custom_maze_button = tk.Button(window, text = "\n Custom Maze \n",bg = "white",relief = 'groove',width=30,command = lambda: change_state("custom maze",False)).pack(pady=10)
        reset_button = tk.Button(window, text = "Reset Progress",width=30, bg = "white",relief="groove",fg="red", command =  lambda: reset_progress()).pack(pady=50)        
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("username")).pack(side="bottom",pady=10)      
    elif state == "custom maze":
        first = tk.Frame(window)
        title_ = tk.Label(window, text = ("\n Custom Maze \nType in dimensions\n"), bg = "white", borderwidth = 1, relief = "groove").pack(fill = "x",pady=20)
        top_seperator = tk.Canvas(window, height=50,width=0).pack()
        #Maze Type 
        #maze_type_text = tk.Label(window, text = "Type").pack(padx=4)
        variable = tk.StringVar(window)
        variable.set("normal")
        #maze_type_menu = tk.OptionMenu(window, variable, "normal","circular")
        #maze_type_menu.pack()
        #Width
        width_text = tk.Label(window, text = "Width").pack(padx=4)
        width_entry = tk.Entry(window, width=20)
        width_entry.pack()
        #Height
        height_text = tk.Label(window, text = "Height").pack(padx=2,pady=4)
        height_entry = tk.Entry(window, width=20)
        height_entry.pack()
        #Cube Size
        cs_text = tk.Label(window, text = "Cell Size").pack(padx=1,pady=4)
        cs_entry = tk.Entry(window, width=20)
        cs_entry.pack()       
        generate_maze = tk.Button(window, text = "Generate",relief = 'groove', bg="white", command = lambda mt = variable, w = width_entry, h = height_entry, c = cs_entry: custom_maze(mt,h,w,c,"CUSTOM MAZE"))
        generate_maze.pack(pady=30)
        if(args[0]):
            error_label = tk.Label(window, text = "Invalid Entry", fg = "red").pack()
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("maze select")).pack(side="bottom",pady=10)

def create_levels(lower,upper,number_of_columns,title,maze_type,lines): #create a number of ordered buttons
    des()
    first = tk.Frame(window)
    first.pack(side='top')
    side = first
    title_ = tk.Label(window, text = ("\n" + title + "\nSelect a level\n"), bg = "white", borderwidth = 1, relief = "groove").pack(in_ = first,fill = "x",pady=20)
    top_seperator = tk.Canvas(window, height=50,width=0).pack(in_ = side)
    dict_one = {
                "normal":0,
                "circular":1
                }
    for i in range((lower),(upper+1)):
        text = str(i)        
        try:
            if lines[dict_one[maze_type]].count(text) > 0:
                fg = "green"
                text += "\n(Complete)"
            else:
                fg = "black"
        except:
            fg = "black"
        button = tk.Button(window, text=text, width = 10, relief = 'groove', bg = "white",fg = fg)
        button.config(command = lambda mt = maze_type, btn = button : load_maze(lower,upper,title,mt,dict_one[maze_type],btn))
        button.pack(in_ = side, side = "left", padx=10,pady=10)
        if (i%number_of_columns) == 0:
            middle = tk.Frame(window)
            middle.pack(side = "top")
            side = middle
    back_button = tk.Button(window, text = "Back", command = lambda: change_state("maze select")).pack(side="bottom",pady=10)

#BUTTONS   
def load_maze(lower,upper,title,maze_type,index,btn):
    maze_size = int((btn['text']).replace("\n(Complete)","")) + 9
    if installed:        
        maze_data = main(maze_size,maze_size,5,maze_type)
        dict_two = {
            "normal":[[len(maze_data[0])-1],[0],[0,len(maze_data)-1]],
            "circular":[[len(maze_data[0])-1],[0],[int(maze_size/2),int(maze_size/2)]]
            }
        win_pos_x = (dict_two[maze_type])[0]
        win_pos_y = (dict_two[maze_type])[1]
        start_pos = (dict_two[maze_type])[2]
        won = play_maze(screen_width,screen_height,(str(maze_size) + " x " + str(maze_size)),10,win_pos_x,win_pos_y,start_pos,maze_data)
    else:
        won = True
    if won:
        if user_id != 0:
            #Edit the CompletedLevels text file to add the newely completed level (it should still be added even if the level has already been completed as it allows the program to record statistics about how many times the level has been completed)
            temp_lines = load_completed_levels()
            print(temp_lines)
            temp_lines[index].append(maze_size - 9)
            #text_file.writelines(temp_lines)
            with open('CompletedLevels.txt', 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow(temp_lines)
    lines = load_completed_levels()
    create_levels(lower,upper,4,title,maze_type,lines)

def custom_maze(maze_type,width,height,cube_size,title):
    try:
        width = int(width.get())
        height = int(height.get())
        cube_size = int(cube_size.get())
        maze_data = main(width,height,5,maze_type.get())
        play_maze(1500,1000,(str(width) + " x " + str(height)),cube_size,[len(maze_data[0])-1],[0],[0,len(maze_data)-1],maze_data)
    except:
        change_state('custom maze',True)

def set_user_id(username,guest):    
    global user_id
    if guest:
        user_id = 0
        change_state("maze select")
    else:
        username = (username['text'])
        print(username)
        #Get user_id from database based on username
        pass

def reset_progress():
    text_file = open("CompletedLevels.txt",'w+')
    text_file.write(("0\n"*number_of_mazes))
    text_file.close()

#DATABASES
#User table stores name and user_id + any additional information needed
#CompletedLevels table stores the completed levels linked to the foreign key user_id and a primary key completed_id. There will be two columns, one for normal mazes, one for labyrinth mazes
#the completed levels will be serialized as such (1#3#4#12...) and when the string is imported it will be split into a list.
            
def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connection

#OTHER
def load_completed_levels():
    #Loads the completed levels based on the file (the location of which is stored in the stats database) linked to the user id
    return []
  
def des(): #Deletes all current widgets in "window"
    widget_list = all_children(window)
    for item in widget_list:
        item.pack_forget()

def all_children(window): # This makes a list of all the widgets
    list_one = window.winfo_children()
    for item in list_one:
        if item.winfo_children() :
            list_one.extend(item.winfo_children())
    return list_one

change_state(default_state)
window.mainloop()
