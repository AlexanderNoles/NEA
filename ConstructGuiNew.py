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

#CREATE
def change_state(state):
    des()
    if state == "start":
        title = tk.Label(window, text = "\n Maze Game \n Version 1.0 \n", bg = "white", borderwidth=1, relief="groove").pack(fill = "x",pady=(250,20))
        start_button = tk.Button(window, text = "Start", bg = "white", command =  lambda: change_state("maze select")).pack()
    elif state == "maze select":
        title = tk.Label(window, text = "\n Maze Select \n", bg = "white",  borderwidth=1, relief="groove").pack(fill = "x",pady=(20,20))
        lines = load_completed_levels()
        normal_maze_button = tk.Button(window, text = "\n  Normal Maze  \n",bg = "white",relief = 'groove', command = lambda: create_levels(1,90,"Normal Maze","normal",lines)).pack(pady=(50,10),fill='y')
        circular_maze_button = tk.Button(window, text = "\n Circular Maze \n",bg = "white",relief = 'groove',command = lambda: create_levels(1,90,"Circular Maze","circular",lines)).pack(pady=10,fill='y')
        back_button = tk.Button(window, text = "Back", command = lambda: change_state("start")).pack(side="bottom",pady=10)

def create_levels(lower,upper,title,maze_type,lines): #create a number of ordered buttons
    des()
    first = tk.Frame(window)
    first.pack(side='top')
    side = first
    title_ = tk.Label(window, text = ("\n" + title + "\nSelect a level\n"), bg = "white", borderwidth = 1, relief = "groove").pack(in_ = first,fill = "x",pady=20)
    top_seperator = tk.Canvas(window, height=50,width=0).pack(in_ = side)
    for i in range((lower),(upper+1)):
        text = str(i)
        try:
            dict_one = {
                "normal":0,
                "circular":1
                }
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
        if (i%10) == 0:
            middle = tk.Frame(window)
            middle.pack(side = "top")
            side = middle
    back_button = tk.Button(window, text = "Back", command = lambda: change_state("maze select")).pack(side="bottom",pady=10)
    
def load_maze(lower,upper,title,maze_type,index,btn):
    maze_size = int((btn['text']).replace("\n(Complete)","")) + 9
    maze_data = main(maze_size,maze_size,100,maze_type)
    won = play_maze(1500,1000,(str(maze_size) + " x " + str(maze_size)),maze_data)
    if won:
        #Edit the CompletedLevels text file to add the newely completed level (it should still be added even if the level has already been completed as it allows the program to record statistics about how many times the level has been completed)
        temp_lines = load_completed_levels()
        temp_lines[index].append(maze_size - 9)
        text_file = open("CompletedLevels.txt","w")
        print(temp_lines)
        text_file.writelines( (((str(temp_lines).replace("'","")).replace("]","\n")).replace("[","")).replace(" ","") )
        text_file.close()
    lines = load_completed_levels()
    create_levels(lower,upper,title,maze_type,lines)
        
#OTHER
def load_completed_levels():
    text_file = open("CompletedLevels.txt",'r')
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
