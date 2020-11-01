import tkinter as tk

from MazeGenerationNew import main
from MazeRendererNew import play_maze

window = tk.Tk()
window.state("zoomed")
window.title("Maze Game")
window.geometry("500x500")
root_menu = tk.Menu(window)
window.config(menu = root_menu)
default_state = "start"

number_of_mazes = 2

#CREATE
def change_state(state,*args):
    des()
    if state == "start":
        title = tk.Label(window, text = "\n Maze Game \n Version 1.0 \n", bg = "white", borderwidth=1, relief="groove").pack(fill = "x",pady=(250,20))
        start_button = tk.Button(window, text = "Start",width=30, bg = "white", command =  lambda: change_state("maze select")).pack()
        exit_button = tk.Button(window, text = "Exit",width=30, bg = "white", fg = "red", command = lambda: exit()).pack(pady=10)
    elif state == "maze select":
        title = tk.Label(window, text = "\n Maze Select \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,20))
        lines = load_completed_levels()
        normal_maze_button = tk.Button(window, text = "\n  Normal-Style Maze  \n",bg = "white",relief = 'groove', command = lambda: create_levels(1,30,4,"Normal Maze","normal",lines)).pack(pady=(50,10),fill='y')
        circular_maze_button = tk.Button(window, text = "\n Labyrinth Maze \n",bg = "white",relief = 'groove',command = lambda: create_levels(1,30,4,"Labyrinth Maze","circular",lines)).pack(pady=10,fill='y')
        custom_maze_button = tk.Button(window, text = "\n Custom Maze \n",bg = "white",relief = 'groove',command = lambda: change_state("custom maze",False)).pack(pady=10,fill='y')
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("start")).pack(side="bottom",pady=10)
    elif state == "custom maze":
        first = tk.Frame(window)
        title_ = tk.Label(window, text = ("\n Custom Maze \nType in dimensions\n"), bg = "white", borderwidth = 1, relief = "groove").pack(fill = "x",pady=20)
        top_seperator = tk.Canvas(window, height=50,width=0).pack()
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
        generate_maze = tk.Button(window, text = "Generate",relief = 'groove', bg="white", command = lambda w = width_entry, h = height_entry, c = cs_entry: custom_maze(h,w,c,"CUSTOM MAZE"))
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
    maze_data = main(maze_size,maze_size,10000,maze_type)
    dict_two = {
        "normal":[[len(maze_data[0])-1],[0],[0,len(maze_data)-1]],
        "circular":[[len(maze_data[0])-1],[0],[int(maze_size/2),int(maze_size/2)]]
        }
    win_pos_x = (dict_two[maze_type])[0]
    win_pos_y = (dict_two[maze_type])[1]
    start_pos = (dict_two[maze_type])[2]
    won = play_maze(1500,1000,(str(maze_size) + " x " + str(maze_size)),10,win_pos_x,win_pos_y,start_pos,maze_data)
    if won:
        #Edit the CompletedLevels text file to add the newely completed level (it should still be added even if the level has already been completed as it allows the program to record statistics about how many times the level has been completed)
        temp_lines = load_completed_levels()
        temp_lines[index].append(maze_size - 9)
        text_file = open("CompletedLevels.txt","w")
        text_file.writelines( (((str(temp_lines).replace("'","")).replace("]","\n")).replace("[","")).replace(" ","") )
        text_file.close()
    lines = load_completed_levels()
    create_levels(lower,upper,4,title,maze_type,lines)

def custom_maze(width,height,cube_size,title):
    try:
        width = int(width.get())
        height = int(height.get())
        cube_size = int(cube_size.get())
        maze_data = main(width,height,100,"normal")
        play_maze(1500,1000,(str(width) + " x " + str(height)),cube_size,[len(maze_data[0])-1],[0],[0,len(maze_data)-1],maze_data)
    except:
        change_state('custom maze',True)
        
#OTHER
def load_completed_levels():
    while True:
        try:
            text_file = open("CompletedLevels.txt",'r')
            break
        except:
            text_file = open("CompletedLevels.txt",'w+')
            text_file.write(("0\n"*number_of_mazes))
    temp_lines=text_file.readlines()
    text_file.close()
    to_return = []
    for i in range(0,len(temp_lines)):
        to_return.append(temp_lines[i].split(','))
        for j in range(0,len(to_return[i])):
            to_return[i][j] = str(to_return[i][j]).replace('\n','')
    return to_return
    
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
