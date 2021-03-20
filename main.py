import tkinter as tk
#import sys
#print('\n'.join(sys.path))

from MazeGenerationNew import main
import MazeDatabase as Db
try:
    from MazeRendererNew import play_maze
    installed = True
except ImportError: #PIL is not installed
    installed = False

#Base tkinter window setup
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

#Get monitor dimensions
import ctypes
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

#User and database variables
user_id = 0
connection = Db.main_database()

number_of_mazes = 2 #CONSTANT

#CREATE
def change_state(state):      #Switches the state of the GUI to the one specified. A state is a pre-defined set of GUI, i.e. a main menu
    des()
    if state == "start":    #Start Screen
        title = tk.Label(window, text = "\n Maze Game \n Version 2.0 \n", bg = "white", borderwidth=1, relief="groove").pack(fill = "x",pady=(250,20))
        enter_button = tk.Button(window, text = "Enter",bg = "white",width=30, command = lambda: change_state("username")).pack()
        exit_button = tk.Button(window, text = "Exit",width=30, bg = "white", fg = "red", command = lambda: exit()).pack(pady=3)
        if not installed:
            error_message = tk.Label(window,text="[PIL not installed, PIL is required for current version]",fg="red").pack(side="bottom",pady = 20)
    if state == "username": #Users select screen
        title = tk.Label(window, text = "\n Accounts \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        top_seperator = tk.Canvas(window, height=50,width=0).pack()
        user_list = Db.get_list_of_users(connection)
        for i in range(0,len(user_list)): #Loads all the current users
            username_button = tk.Button(window,text=((user_list[i][1])[2:-1] + "\n" + "(#" + ("0" * (3-len(user_list[i][0]))) + user_list[i][0] + ")"),bg = "white",width=30,height=2)
            username_button.config(command = lambda u = user_list[i][0]: set_user_id(u,False))
            username_button.pack(pady=3)
        guest_button = tk.Button(window, text = "Play as Guest",bg = "white",width=30,height=2, command = lambda u = "guest": set_user_id(u,True)).pack(pady=3)
        create_new_button = tk.Button(window,text="+",bg = "white",width=10, command = lambda: change_state("new user")).pack(pady=3)
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("start")).pack(side="bottom",pady=10)  
    elif state == "new user":   #New user screen
        title = tk.Label(window, text = "\n New User \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        username_text = tk.Label(window, text = "Username").pack(pady=(10,1))
        username_entry = tk.Entry(window,width=20)
        username_entry.pack()
        enter_button = tk.Button(window, text = "Enter",bg = "white",width=10, command = lambda u = username_entry: new_user(u)).pack(pady = 10)
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("username")).pack(side="bottom",pady=10)  
    elif state == "maze select":    #Maze type select screen. Options are, Normal, Diamond and Custom
        if user_id != 0:
            completed = Db.get_list_of_completed_levels(connection,user_id)
        else:
            completed = [[],[]]
        title = tk.Label(window, text = "\n Maze Select \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,100))
        normal_maze_button = tk.Button(window, text = "\n  Normal-Style Maze  \n",bg = "white",relief = 'groove',width=30, command = lambda: create_levels(1,32,4,"Normal Maze","normal",completed)).pack(pady=(50,10))
        circular_maze_button = tk.Button(window, text = "\n Diamond Maze \n",bg = "white",relief = 'groove',width=30,command = lambda: create_levels(1,32,4,"Diamond Maze","diamond",completed)).pack(pady=10)
        custom_maze_button = tk.Button(window, text = "\n Custom Maze \n",bg = "white",relief = 'groove',width=30,command = lambda: change_state("custom maze")).pack(pady=10)
        reset_button = tk.Button(window, text = "Reset Progress",width=30, bg = "white",relief="groove",fg="red", command =  lambda: reset_progress()).pack(pady=50)        
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("username")).pack(side="bottom",pady=10)      
    elif state == "custom maze":    #Custom maze creation screen
        first = tk.Frame(window)
        title_ = tk.Label(window, text = ("\n Custom Maze \n"), bg = "white", borderwidth = 1, relief = "groove").pack(fill = "x",pady=20)
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
        width_scale = tk.Scale(window, tickinterval=2, length=600, orient="horizontal",from_ = 2,to=50)
        width_scale.pack()
        #Height
        height_text = tk.Label(window, text = "Height").pack(padx=4)
        height_scale = tk.Scale(window, tickinterval=2, length=600, orient="horizontal",from_ = 2,to=50)
        height_scale.pack()
        #RENDERING
        title_ = tk.Label(window, text = ("\n Rendering \n"), bg = "white", borderwidth = 1,width = 100, relief = "groove").pack(pady=(20,5))
        #Cube Size
        cs_text = tk.Label(window, text = "Cell Size").pack(padx=4,pady=(10,0))
        cs_entry = tk.Entry(window, width=20)
        cs_entry.pack()
              
        generate_maze = tk.Button(window, text = "Generate",relief = 'groove', bg="white", command = lambda mt = variable, w = width_scale, h = height_scale, c = cs_entry: custom_maze(mt,h,w,c,"CUSTOM MAZE"))
        generate_maze.pack(pady=30)
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("maze select")).pack(side="bottom",pady=10)

def create_levels(lower,upper,number_of_columns,title,maze_type,completed): #create a number of ordered buttons to represnt different levels, the level number is then passed to the load_maze function
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
    for i in range((lower),(upper+1)):
            text = str(i)                          
            try:
                if completed[dict_one[maze_type]].count(text) > 0:
                    fg = "green"
                    text += "\n(Complete)"
                else:
                    fg = "black"
            except:
                fg = "black"
            button = tk.Button(window, text=text, width = 10, relief = 'groove', bg = "white",fg = fg)
            button.config(command = lambda mt = maze_type, btn = button : load_maze(lower,upper,title,mt,btn))
            button.pack(in_ = side, side = "left", padx=10,pady=10)
            if (i%number_of_columns) == 0:
                middle = tk.Frame(window)
                middle.pack(side = "top")
                side = middle
    back_button = tk.Button(window, text = "Back", command = lambda: change_state("maze select")).pack(side="bottom",pady=10)

#BUTTONS   
def load_maze(lower,upper,title,maze_type,btn):   #Generates the maze and then passes the data along with other parameters to the MazeRenderer script
    maze_size = int((btn['text']).replace("\n(Complete)","")) + 3
    if installed:        
        maze_data = main(maze_size,maze_size,1000,maze_type)
        dict_two = {
            "normal":[[len(maze_data[0])-1],[0],[0,len(maze_data)-1]],
            "diamond":[[len(maze_data[0])-1],[0],[0,len(maze_data)-1]]
            }
        win_pos_x = (dict_two[maze_type])[0]
        win_pos_y = (dict_two[maze_type])[1]
        start_pos = (dict_two[maze_type])[2]
        dimensions = alter_screen()
        won = play_maze(dimensions[0],dimensions[1],(str(maze_size) + " x " + str(maze_size)),10,win_pos_x,win_pos_y,start_pos,maze_data)
    else:
        won = True  #Maze auto-completes if PIL is not installed
    if won:
        if user_id != 0:
            Db.add_completed_level(connection,maze_size-3, maze_type,user_id)
    completed = Db.get_list_of_completed_levels(connection,user_id)
    create_levels(lower,upper,4,title,maze_type,completed)

def custom_maze(maze_type,width,height,cube_size,title):    #Same as the function above but for custom mazes
        width = int(width.get())
        height = int(height.get())
        cube_size = int(cube_size.get())
        maze_data = main(width,height,1000,maze_type.get())
        dimensions = alter_screen()
        play_maze(dimensions[0],dimensions[1],(str(width) + " x " + str(height)),cube_size,[len(maze_data[0])-1],[0],[0,len(maze_data)-1],maze_data)
        change_state('custom maze',True)

def set_user_id(username,guest):    #Sets the user ID
    global user_id
    if guest:
        user_id = 0
    else:
        user_id = username
    change_state("maze select")

def reset_progress():           #Resets the current users progress
    username = Db.delete_user(connection, user_id)
    Db.create_new_user(connection, username)
    change_state("maze select")

def new_user(user_entry_widget):    #Creates a new user named using the entered user name
    name = user_entry_widget.get()
    Db.create_new_user(connection,name)
    change_state("username")

#OTHER  
def des(): #Deletes all current widgets in "window"
    widget_list = all_children(window)
    for item in widget_list:
        item.pack_forget()

def all_children(window): # This makes a list of all the current widgets
    list_one = window.winfo_children()
    for item in list_one:
        if item.winfo_children() :
            list_one.extend(item.winfo_children())
    return list_one

def alter_screen():     #Changes screen dimenions to make the rendering of the maze faster
    const = 2
    dimensions = [0,0]
    dimensions[0] = int(screen_width/const)
    dimensions[1] = int(screen_height/const)
    return dimensions

if __name__ == "__main__":
    change_state(default_state)
    
window.mainloop()
