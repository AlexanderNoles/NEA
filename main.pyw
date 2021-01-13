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
        title = tk.Label(window, text = "\n Maze Game \n Version 1.2 \n", bg = "white", borderwidth=1, relief="groove").pack(fill = "x",pady=(250,20))
        enter_button = tk.Button(window, text = "Enter",bg = "white",width=30, command = lambda: change_state("username")).pack()
        exit_button = tk.Button(window, text = "Exit",width=30, bg = "white", fg = "red", command = lambda: exit()).pack(pady=3)
        if not installed:
            error_message = tk.Label(window,text="[Pygame not installed, Pygame is required for current version]",fg="red").pack(side="bottom",pady = 20)
    if state == "username":
        title = tk.Label(window, text = "\n Accounts \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        top_seperator = tk.Canvas(window, height=50,width=0).pack()       
        for i in range(0,1): #will eventually base the amount of buttons off the amount of users
            username_button = tk.Button(window,text=("stand-in \n(#00" + str(i) + ")"),bg = "white",width=30,height=2)
            username_button.config(command = lambda u = username_button: set_user_id(u,False))
            username_button.pack(pady=3)
        guest_button = tk.Button(window, text = "Play as Guest",bg = "white",width=30,height=2, command = lambda u = "guest": set_user_id(u,True)).pack(pady=3)
        create_new_button = tk.Button(window,text="+",bg = "white",width=10, command = lambda: change_state("new user")).pack(pady=3)
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("start")).pack(side="bottom",pady=10)  
    elif state == "new user":
        title = tk.Label(window, text = "\n New User \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        username_text = tk.Label(window, text = "Username").pack(pady=(10,1))
        username_entry = tk.Entry(window,width=20)
        username_entry.pack()
        enter_button = tk.Button(window, text = "Enter",bg = "white",width=30, command = lambda: change_state("username")).pack(pady = 10)
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("username")).pack(side="bottom",pady=10)  
    elif state == "maze select":
        title = tk.Label(window, text = "\n Maze Select \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        lines = load_completed_levels()
        normal_maze_button = tk.Button(window, text = "\n  Normal-Style Maze  \n",bg = "white",relief = 'groove',width=30, command = lambda: create_levels(1,30,4,"Normal Maze","normal",lines)).pack(pady=(50,10))
        circular_maze_button = tk.Button(window, text = "\n Diamond Maze \n",bg = "white",relief = 'groove',width=30,command = lambda: create_levels(1,30,4,"Diamond Maze","diamond",lines)).pack(pady=10)
        custom_maze_button = tk.Button(window, text = "\n Custom Maze \n",bg = "white",relief = 'groove',width=30,command = lambda: change_state("custom maze",False)).pack(pady=10)
        reset_button = tk.Button(window, text = "Reset Progress",width=30, bg = "white",relief="groove",fg="red", command =  lambda: reset_progress()).pack(pady=50)        
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("username")).pack(side="bottom",pady=10)      
    elif state == "custom maze":
        first = tk.Frame(window)
        title_ = tk.Label(window, text = ("\n Custom Maze \n\n"), bg = "white", borderwidth = 1, relief = "groove").pack(fill = "x",pady=20)
        top_seperator = tk.Canvas(window, height=50,width=0).pack()
        #GENERATION
        title_ = tk.Label(window, text = ("\n Generation \n"), bg = "white", borderwidth = 1,width = 100, relief = "groove").pack(pady=20)
        #Maze Type 
        maze_type_text = tk.Label(window, text = "Type").pack(padx=4,pady=(10,0))
        variable = tk.StringVar(window)
        variable.set("normal")
        maze_type_menu = tk.OptionMenu(window, variable, "normal","diamond")
        maze_type_menu.pack(pady=(0,10))
        #Width
        width_text = tk.Label(window, text = "Width").pack(padx=4)
        width_scale = tk.Scale(window, tickinterval=10, length=600, orient="horizontal")
        width_scale.pack()
        #Height
        height_text = tk.Label(window, text = "Height").pack(padx=4)
        height_scale = tk.Scale(window, tickinterval=10, length=600, orient="horizontal")
        height_scale.pack()
        #RENDERING
        title_ = tk.Label(window, text = ("\n Rendering \n"), bg = "white", borderwidth = 1,width = 100, relief = "groove").pack(pady=(20,5))
        #Cube Size
        cs_text = tk.Label(window, text = "Cell Size").pack(padx=4,pady=(10,0))
        cs_entry = tk.Entry(window, width=20)
        cs_entry.pack()
              
        generate_maze = tk.Button(window, text = "Generate",relief = 'groove', bg="white", command = lambda mt = variable, w = width_scale, h = height_scale, c = cs_entry: custom_maze(mt,h,w,c,"CUSTOM MAZE"))
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
                "diamond":1
                }
    for i in range((lower),(upper+2)):
        text = str(i) 
        if i != upper+1:                  
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
        else:
            button = tk.Button(window, text=text, width = 10, relief = 'groove', bg = "white",fg = "red")
            button.config(command = lambda mt = maze_type, btn = button : load_maze(lower,upper,title,mt,dict_one[maze_type],btn))
            button.pack(padx=10,pady=10)
    back_button = tk.Button(window, text = "Back", command = lambda: change_state("maze select")).pack(side="bottom",pady=10)

#BUTTONS   
def load_maze(lower,upper,title,maze_type,index,btn):
    maze_size = int((btn['text']).replace("\n(Complete)","")) + 9
    if installed:        
        maze_data = main(maze_size,maze_size,1000,maze_type)
        dict_two = {
            "normal":[[len(maze_data[0])-1],[0],[0,len(maze_data)-1]],
            "diamond":[[len(maze_data[0])-1],[0],[0,len(maze_data)-1]]
            }
        win_pos_x = (dict_two[maze_type])[0]
        win_pos_y = (dict_two[maze_type])[1]
        start_pos = (dict_two[maze_type])[2]
        won = play_maze(screen_width,screen_height,(str(maze_size) + " x " + str(maze_size)),10,win_pos_x,win_pos_y,start_pos,maze_data)
    else:
        won = True
    if won:
        if user_id != 0:
            add_completed_level(maze_size-9, maze_type)
    lines = load_completed_levels()
    create_levels(lower,upper,4,title,maze_type,lines)

def custom_maze(maze_type,width,height,cube_size,title):
    try:
        width = int(width.get())
        height = int(height.get())
        cube_size = int(cube_size.get())
        maze_data = main(width,height,1000,maze_type.get())
        play_maze(screen_width,screen_height,(str(width) + " x " + str(height)),cube_size,[len(maze_data[0])-1],[0],[0,len(maze_data)-1],maze_data)
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
    pass

#DATABASES
#Users table stores name and user_id + any additional information needed
#CompletedLevels table stores the completed levels linked to the foreign key user_id and a primary key completed_id. There will be two columns, one for normal mazes, one for diamond mazes
#the completed levels will be serialized as such (1#3#4#12...) and when the string is imported it will be split into a list.

def main_database():
    user_table = """ CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY,
username text NOT NULL
); """
    completed_levels_table = """ CREATE TABLE IF NOT EXISTS completedLevels (
id integer PRIMARY KEY,
normal_maze text,
diamond_maze text,
user_id integer NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
); """    
    connection = create_connection(r"Maze.db")
    if connection is not None:
        create_table(connection,user_table)
        create_table(connection,completed_levels_table)
    else:
        print("Database Connection Error")

def create_new_user(connection, username):
    new_user_sql = ''' INSERT INTO user(username) VALUES(?)'''
    cursor = connection.cursor()
    cursor.execute(new_user_sql,username)
    connection.commit()

def add_completed_level(connection,level_number,maze_type):    #Uses the user id to alter the user's completed levels
    pass
            
def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connection

def create_table(connection, create_table):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table)
    except Error as e:
        print(e)
        
main_database()

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

if __name__ == "__main__":
    change_state(default_state)
    
#window.mainloop()
