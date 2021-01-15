import time     
import os                   #Used to hide the initial pygame console output
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame               #Used to draw pixels on the screen in a window

#VARIABLES
#colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
default = black             #Equivalent to background colour

#other
default_line_weight = 1
scale = 1 #Has to be an int
debug = False
with open('font.txt') as f:
    font = f.readlines()
    f.close()

#GAME LOGIC
def play_maze(width,height,title,cube_size,win_pos_x,win_pos_y,start_pos,maze_data):
    #A cube_size of two and below will cause the squares to be too small to be properly represented properly on any pixelated screen, hence, 3 is the lowest the function allows
    if cube_size < 3: cube_size = 3 
    #pygame.init()
    screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
    pygame.display.set_caption(title)
    temp = 0 #Temporary Variable to manage progress of stand-in progress bar
    delta_time = 0
    time_to_close = 1.5
    add_to_y = 0
    add_to_x = 0
    loading = True
    first_frame = True
    running = True
    position_set_to = [1,0]
    move_dir = ""
    player_pos = start_pos
    active_last_frame = True
    check_walls = True
    to_return = False
    ending = True
    drawing_per_frame = True
    while running:
        #Anything in this loop is run every frame (Equivalent to Unity's update() function)
        start_time = time.time() #For measuring execution time it is used for debug, testing program speed and the calculation of delta_time  
        for event in pygame.event.get():            
            #Makes program stop when user closes the window or presses "esc"
            if event.type == pygame.QUIT:
                running = False
            #Checks if the player has pressed a move button (and which one it was) this frame or if the player has pressed the escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_LEFT or event.key == pygame.key.key_code("a"):
                    add_to_x = -1
                    move_dir = "left"
                elif event.key == pygame.K_RIGHT or event.key == pygame.key.key_code("d"):
                    add_to_x = 1
                    move_dir = "right"
                elif event.key == pygame.K_UP or event.key == pygame.key.key_code("w"):
                    add_to_y = -1
                    move_dir = "up"
                elif event.key == pygame.K_DOWN or event.key == pygame.key.key_code("s"):
                    add_to_y = 1
                    move_dir = "down"
                else:
                    move_dir = ""
                if event.key == pygame.K_e:
                    print(player_pos)
                #Checks to make sure player can't go outside the maze
                if position_set_to[0] + add_to_x < 0 or position_set_to[0] + add_to_x > len(maze_data[0])-1:
                    add_to_x = 0
                    check_walls = False
                if position_set_to[1] + add_to_y < 0 or position_set_to[1] + add_to_y > len(maze_data)-1:
                    add_to_y = 0
                    check_walls = False
                #Checks to see if there is a wall in the players way
                if(wall(maze_data,[position_set_to[0] + add_to_x,position_set_to[1] + add_to_y],player_pos,move_dir)) and check_walls:
                    add_to_y = 0
                    add_to_x = 0
                check_walls = True
            else:
                position_set_to = player_pos
                add_to_y = 0
                add_to_x = 0
        #Game Code
        if debug:
            print(str(round((time.time() - start_time)*1000,1)) + "ms") #Prints execution time (per frame) to console
            print(temp)
        if loading:
            if temp >= 1:
                loading = False
                screen.fill(default)
            else:
                if temp == 0:
                    #Create Title
                    text("Maze Game",10,[0,-height/4],white,screen,[width,height])
                    time.sleep(0.1)
                progress_bar(width/4,temp,screen,[0,height/4],[width,height])  #This is a stand-in progress bar to test how it would look, the real one's progression would be based on the maze generation progression
                temp += 1 * delta_time                                  #currently the maze generates before the progress bar is shown and the maze is rendered after (To make it properly linked to maze generation
        elif not loading:                                               #the progress bar would have to be called from the MazeGenerationNew script)
            if first_frame == True:                
                first_frame = False
                if drawing_per_frame:
                    maze_width = (len(maze_data) * (cube_size-1))+1
                    maze_height = (len(maze_data[0]) * (cube_size-1))+1
                    x = 0
                    y = 0
                #Create Maze Title
                text(title,3,[0,-((((len(maze_data) * (cube_size-1))+1)/2)+15)],white,screen,[width,height])
                #Instantiate Player
                player_pos = draw_player(maze_data,maze_width,maze_height,cube_size,screen,[width,height],player_pos,True)
                position_set_to = player_pos            
            else:
                if won(player_pos,win_pos_x,win_pos_y):#[len(maze_data[0])-1,0]):
                    if ending:
                        time.sleep(0.4) #Halts the game for a very short amount of time to make the transition to the end screen smoother
                        ending = False
                    screen.fill(default)
                    text("Maze Completed",10,[0,0],white,screen,[width,height])
                    text("#",5,[0,-50],white,screen,[width,height])
                    if time_to_close < 0:
                        to_return = True
                        running = False
                    else:
                        time_to_close -= delta_time
                else:
                    if drawing_per_frame:
                        draw_maze_per_cell([maze_height,maze_width], [x,y], [width,height], cube_size, [win_pos_x,win_pos_y], screen, maze_data)
                        x += 1
                        if x == len(maze_data[y]):
                            x = 0
                            y += 1
                        if y == len(maze_data):
                            drawing_per_frame = False
                    player_pos = draw_player(maze_data,maze_width,maze_height,cube_size,screen,[width,height],[position_set_to[0] + add_to_x,position_set_to[1] + add_to_y],False,player_pos)
        pygame.display.flip()  
        if(pygame.display.get_active() and active_last_frame == False):
            generated_data = draw_maze([width,height],cube_size,win_pos_x,win_pos_y,screen,maze_data)
            text(title,3,[0,-((((len(maze_data) * (cube_size-1))+1)/2)+15)],white,screen,[width,height])                                                                                                                                                                 
        delta_time = time.time() - start_time #delta_time is the time the program took to execute the last frame
        active_last_frame = pygame.display.get_active()
    pygame.quit()
    return to_return
        
#CHECKS
def won(player_pos,win_pos_x,win_pos_y): #Compares player position to entered position
    if player_pos[0] in win_pos_x and player_pos[1] in win_pos_y:
        return True
    else:
        return False

def wall(maze_data,position_to_set_to,player_pos,move_dir): #Checks to see if there is a wall blocking the players way when they attempt to move
    if move_dir == "":
        return True
    dict_one = {
        "left":[0,1],
        "right":[1,0],
        "up":[2,3],
        "down":[3,2]
        }
    if (maze_data[player_pos[1]][player_pos[0]])[(dict_one[move_dir])[0]] == 1 or (maze_data[position_to_set_to[1]][position_to_set_to[0]])[(dict_one[move_dir])[1]] == 1:
        return True
    else:
        return False

#RENDERING
def draw_maze_per_cell(maze_dimensions, coords_to_draw, window_dimensions, cube_size, win_pos, screen, maze_data):
    offsetx = coords_to_draw[0] * (cube_size-1)
    offsety = coords_to_draw[1] * (cube_size-1)
    draw_rectangle([(0-(maze_dimensions[0]/2)+offsetx),((0-maze_dimensions[1]/2)+offsety)],cube_size,cube_size,False,white,screen,window_dimensions,maze_data[coords_to_draw[1]][coords_to_draw[0]])
    if won([coords_to_draw[0],coords_to_draw[1]],win_pos[0],win_pos[1]):
        draw_rectangle([(0-(maze_dimensions[0]/2)+offsetx+2),((0-maze_dimensions[1]/2)+offsety+2)],cube_size-4,cube_size-4,True,green,screen,window_dimensions) 

def draw_player(maze_data,maze_height,maze_width,cube_size,screen,window_dimensions,new_pos,first_pos,*args): #Draws the player in the center of a square, indicated by x and y coordinates
    player_size = cube_size * 0.6
    if first_pos:
        player_pos = find_center_of_square(maze_width,maze_height,cube_size,new_pos)
        draw_rectangle(player_pos,player_size,player_size,True,green,screen,window_dimensions)
    else:
        if args[0] is None:
            print("ERROR: No previous position entered")
        else:
            old_player_pos = find_center_of_square(maze_width,maze_height,cube_size,args[0])
            player_pos = find_center_of_square(maze_width,maze_height,cube_size,new_pos)
            draw_rectangle(old_player_pos,player_size,player_size,True,default,screen,window_dimensions) #Remove previous player_pos   
            draw_rectangle(player_pos,player_size,player_size,True,white,screen,window_dimensions)                   
    return new_pos

def progress_bar(width,progress,screen,offset,window_dimensions): #Generates a progress bar in the center of the screen, however, it's position can be shifted using the offset
    center = [0+offset[0],0+offset[1]]
    #Draw progress bar shell
    draw_rectangle([int(center[0]-width/2),center[1]],width,15,False,white,screen,window_dimensions,1)
    #Draw actual progress
    draw_rectangle([int(center[0]-width/2)+2,center[1]+2],int((width-4)*progress),11,True,white,screen,window_dimensions)

def text(text,text_size,offset,colour,screen,window_dimensions):        #Draws entered text on screen in the font defined in 'font.txt', by default it is drawn in the center, however, this can be altered by entering an offset
    text_dict = {                                                       
        "a":0,"A":0,"b":1,"B":1,"c":2,"C":2,"d":3,"D":3,"e":4,"E":4,
        "f":5,"F":5,"g":6,"G":6,"h":7,"H":7,"i":8,"I":8,"j":9,"J":9,
        "k":10,"K":10,"l":11,"L":11,"m":12,"M":12,"n":13,"N":13,"o":14,"O":14,
        "p":15,"P":15,"q":16,"Q":16,"r":17,"R":17,"s":18,"S":18,"t":19,"T":19,
        "u":20,"U":20,"v":21,"V":21,"w":22,"W":22,"x":23,"X":23,"y":24,"Y":24,
        "z":25,"Z":25," ":26,"1":27,"2":28,"3":29,"4":30,"5":31,"6":32,"7":33,
        "8":34,"9":35,"0":36,"#":37
        }
    text_list = split(text)
    text_width = 0
    text_height = 5 * text_size
    offsetx = 0
    offsety = 0
    offset_character = 0
    for i in text_list:
        character_data = split_int(font[text_dict[i]])
        text_width += (int((len(character_data)*text_size)/5) + (1*text_size))
    for i in text_list:
        character_data = split_int(font[text_dict[i]])
        for y in range(0,5):
            for x in range(0,int(len(character_data)/5)):
                if character_data[(y*int(len(character_data)/5))+x] == 0:
                    pass
                else:
                    draw_rectangle([(-text_width/2)+offsetx+offset_character+(offset[0]),(-text_height/2)+offsety+(offset[1])],text_size,text_size,True,colour,screen,window_dimensions)
                offsetx += text_size
            offsety += text_size
            offsetx = 0
        offset_character += (text_size * (len(character_data)/5))+(1 * text_size)
        offsety = 0
        
def draw_rectangle(startpos,width,height,fill,colour,screen,window_dimensions,*args): #Draws a rectangle based around 0,0 (screen center), for best use don't redraw things that are already drawn (i.e. stagnant sprites, like the maze)
    width = alter_to_fit_scale(width)
    height = alter_to_fit_scale(height)
    for i in range(0,len(startpos)):
        startpos[i] = alter_coords_to_fit_scale(startpos[i],int((window_dimensions[i])/2))
    if fill:
        for x in range(startpos[0],startpos[0]+width):
            for y in range(startpos[1],startpos[1]+height):
                screen.set_at((x,y),colour)
    if not fill:
        list_one = []
        if isinstance(args[0], int):
            for i in range(0,4):
                list_one.append(args[0])
        else:
            list_one = args[0]
        for x in range(startpos[0],startpos[0]+width):
            for y in range(startpos[1],startpos[1]+height):
                if (x in range(startpos[0]+list_one[0],startpos[0]+width-list_one[1])) and (y in range(startpos[1]+list_one[2],startpos[1]+height-list_one[3])):
                    pass
                else:
                    screen.set_at((x,y),colour)

#CONVERTORS
def find_center_of_square(maze_width,maze_height,cube_size,pos): #Converts x and y coords to pixel measurments so that the player can be properly positioned 
    x = pos[0]                                                   
    y = pos[1]
    pos_in_pixels = [(0-(maze_width/2)+(cube_size-1)*x)+(0.2*cube_size),(0-(maze_height/2)+(cube_size-1)*y)+(0.2*cube_size)]
    return pos_in_pixels

def alter_to_fit_scale(value): #Alters any variable to fit game scale    
    return int(value*scale)

def alter_coords_to_fit_scale(value,full): #Makes coords relative to the center and fits them to game scale   
    return int(full + (value*scale))

#OTHER
def split(word):
    return [char for char in word]

def split_int(word):
    word = word.replace(" ","")
    word = word.replace("\n","")
    return [int(char) for char in word]

def pythag(a,b):                #Intended to be used to help create the circle of visibilty around the player
    return ((a*a)+(b*b))**0.5
