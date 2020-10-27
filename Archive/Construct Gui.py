import tkinter as tk
import math

window = tk.Tk()
window.state("zoomed")
window.title("Maze Game One")
root_menu = tk.Menu(window)
window.geometry("500x500")
window.config(menu = root_menu)
state = "start"

#Load Completed Levels
text_file = open("CompletedLevels.txt",'r')
temp_lines=text_file.readlines()
lines = []
for i in range(0,len(temp_lines)):
    lines.append(temp_lines[i].split(','))
    for j in range(0,len(lines[i])):
        lines[i][j] = (lines[i][j])[0]

def des(): # This calls the below function in the correct way so all the widgets can be deleted
    widget_list = all_children(window)
    for item in widget_list:
        item.pack_forget()

def all_children (window): # This makes a list of all the widgets
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

def levels(lower, higher, title,maze_type,page):
    des()
    print(lower)
    print(higher)
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side="right", fill='y')
    top = tk.Frame(window)
    top.pack(side='top')
    side = top
    bg = "white"
    label = tk.Label(window, text = ("\n" + title + "\nSelect a level\n"), bg = "white", borderwidth=1, relief="groove").pack(in_ = top, fill = "x", pady=10)
    top_seperator = tk.Canvas(window, height=50,width=0).pack(in_ = side)
    if higher > 160 + (160*page):
        higher = 160
    for i in range((lower+1), (higher+1)):
        try:
            if lines[maze_type].count(str(i-10)) > 0:
                bg = "gray"
            else:
                bg = "white"
        except:
            bg = "white"
        btn = tk.Button(window, text=str(i-10), width = 10, relief = 'groove', bg = bg, command = lambda: getText(str(i-10),maze_type,btn))
        btn.pack(in_ = side, side = 'left', padx=10, pady=10)
        if ((i-10)%10) == 0:
            middle = tk.Frame(window)
            middle.pack(side = 'top')
            side = middle
    #back_btn = tk.Button(window,text='Back', width=10)
    #back_btn.config(command = lambda t=-1,r=maze_type, btn = btn:getText(t,r,btn))
    #back_btn.pack(pady=10)
    increaseButton = tk.Button(window, text='>>',command = lambda: change_levels(title,maze_type,1,page))
    increaseButton.pack(side = 'right')
    if (True):
        decreaseButton = tk.Button(window, text='<<',command = lambda: change_levels(title,maze_type,-1,page))
        decreaseButton.pack(side = 'left')

def getText(text,maze_type, btn):
    if (int(text)) == -1:
        changestate('maze_type')
    else:
        if maze_type == 0:
            circular_maze(int(text)+10,1)
        else:
            normal_maze(int(text)+10,1)

def change_levels(title, maze_type,increase,page):
    page = page + increase
    print(page)
    levels(1 + (160 * page),160  + (160 * page),title,maze_type,page)
    

def circular_maze(*args):
    try:
        if args[1] == 1:
            make_maze("circular",args[0])
    except:
        levels(10,700,"Circular Mazes",0,0)


def normal_maze(*args):
    try:
        if args[1] == 1:
            make_maze("normal",args[0])
    except:
        levels(10,700,"Normal Mazes",1,0)

def custom_maze():
    pass

def menu_button():
    changestate('maze_type')

def changestate(state):
    if state == 'start':
        des()
        label = tk.Label(window, text = "\n Maze Game \n Version 0.1 \n", bg = "white", borderwidth=1, relief="groove").pack(fill = "x",pady=(250,20))
        btn1 = tk.Button(window, text = "Play", bg = "grey", command = menu_button).pack()

    elif state == 'maze_type':
        des()
        circular_button = tk.Button(window,width =32, text = "Circular Maze\n(Easy)",command = circular_maze).pack(pady=(100,0))
        normal_button = tk.Button(window,width = 32, text = "Normal Maze\n(Hard)",command = normal_maze).pack(pady=10)
        custom_button = tk.Button(window,width = 32, text = "Custom Maze\n(Alter width and height of normal maze)", command =custom_maze).pack()

def make_maze(maze_type,maze_size):  #If it is a custom maze enter maze_size as a list
    des()
    try:
        if maze_type == 'circular':
            from CircularMazeGeneration import generate_circular_maze
            full_maze_data = generate_circular_maze(maze_size)
            pos = [int(math.ceil(maze_size/2)),int(math.ceil(maze_size/2))]
        elif maze_type == 'normal':
            from MazeGeneration import generate_maze
            full_maze_data = generate_maze(maze_size,maze_size)
            pos = [0,0]
        elif maze_type == 'custom':
            from MazeGeneration import generate_maze
            full_maze_data = generate_maze(maze_size[0],maze_size[1])
            pos = [0,0]
        else:
            print("Invalid Maze Type")
            input("")
            exit()
        maze_data = full_maze_data[0]
        tunnel_data = full_maze_data[1]
        display_maze(maze_data,tunnel_data,pos,maze_size)
    except:
        print("Failed to generate maze")

def display_maze(maze_data,tunnel_data,player_pos,maze_size):
    #Construct the area the maze will be displayed in and set the intial maze data
    maze = tk.StringVar()
    temp_str = ''
    for i in range(0,len(maze_data)):
        for j in range(0,len(maze_data[i])):
            temp_str = temp_str + maze_data[i][j] + ' '
        temp_str = temp_str + ('\n')

    #At some point we should turn the map_data in to better looking stuff
    maze.set(temp_str)
    maze_text = tk.Text(window)
    maze_text.tag_configure("center",justify='center')
    maze_text.insert("1.0",maze.get())
    maze_text.tag_add("center","1.0","end")
    maze_text.pack(expand=True,fill='both')
    maze_text.config(state='disabled')
    #This is only temporary for DEBUG purposes, at a later date we could instead use something such as pygame after a level is selected

changestate(state)
window.mainloop()
