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

#GAME LOGIC
def play_maze(width,height,title,maze_data):
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption(title)
    temp = 0 #Temporary Variable to manage progress of stand-in progress bar
    delta_time = 0
    add_to_y = 0
    add_to_x = 0
    loading = True
    first_frame = True
    running = True
    position_set_to = [0,0]
    move_dir = ""
    player_pos = [0,0]
    cube_size = 10
    check_walls = True
    while running:
        #Anything in this loop is run every frame (Equivalent to Unity's update() function)
        start_time = time.time() #For measuring execution time it is used for debug, testing program speed and the calculation of delta_time  
        for event in pygame.event.get():            
            #Makes program stop when user closes the window
            if event.type == pygame.QUIT:
                running = False
            #Checks if the player has pressed a move button (and which one it was) this frame
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    add_to_x = -1
                    move_dir = "left"
                elif event.key == pygame.K_RIGHT:
                    add_to_x = 1
                    move_dir = "right"
                elif event.key == pygame.K_UP:
                    add_to_y = -1
                    move_dir = "up"
                elif event.key == pygame.K_DOWN:
                    add_to_y = 1
                    move_dir = "down"
                else:
                    move_dir = ""
                if event.key == pygame.K_e: #This is a reset button and is only for testing, can be removed in final version
                    first_frame = True
                    screen.fill(default)
                    from MazeGenerationNew import generate_random_walls
                    maze_data = generate_random_walls(100,100)
                #Checks to make sure player can't go outside the maze
                if position_set_to[0] + add_to_x < 0 or position_set_to[0] + add_to_x > len(maze_data[0]):
                    add_to_x = 0
                    check_walls = False
                if position_set_to[1] + add_to_y < 0 or position_set_to[1] + add_to_y > len(maze_data):
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
                progress_bar(100,4,temp,screen,[0,0],[width,height]) #This is a stand-in progress bar to test how it would look, the real one's progression would be based on the maze generation progression
                temp += 1 * delta_time                               #currently the maze generates before the progress bar is shown and the maze is rendered after (To make it properly linked to maze generation
        elif not loading:                                            #the progress bar would have to be called from the MazeGenerationNew script)
            if first_frame == True:                
                first_frame = False
                generated_data = draw_maze([width,height],cube_size,screen,maze_data)
                player_pos = draw_player(maze_data,generated_data[0],generated_data[1],cube_size,screen,[width,height],[0,len(maze_data)-1],True)
                position_set_to = player_pos
            else:
                player_pos = draw_player(maze_data,generated_data[0],generated_data[1],cube_size,screen,[width,height],[position_set_to[0] + add_to_x,position_set_to[1] + add_to_y],False,player_pos)
                if won(player_pos,[len(maze_data[0])-1,0]):
                    running = False #Currently this just closes the program but at some point it should display a maze sloved message on screen
        pygame.display.flip()                                                                                                                                                                
        delta_time = time.time() - start_time #delta_time is the time the program took to execute the last frame
    pygame.quit()

#CHECKS
def won(player_pos,win_pos):
    if player_pos == win_pos:
        return True
    else:
        return False

def wall(maze_data,position_to_set_to,player_pos,move_dir): #Checks to see if there is a wall blocking the players way (currently not working)
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
def draw_maze(window_dimensions,cube_size,screen,maze_data):
    #This function will draw the maze based on maze data generated in the maze generation script
    #A cube_size of two and below will cause the squares to be too small to be properly represented properly on any pixelated screen, hence, 3 is the lowest the function allows
    if cube_size < 3: cube_size = 3 
    #Content of maze#
    maze_width = (len(maze_data) * (cube_size-1))+1 #Calculates the dimensions of the maze, taking into account the fact the squares overlap
    maze_height = (len(maze_data[0]) * (cube_size-1))+1    
    offsety = 0
    offsetx = 0
    for y in range(0,len(maze_data)):
        for x in range(0, len(maze_data[y])):
            draw_rectangle([(0-(maze_height/2)+offsetx),((0-maze_width/2)+offsety)],cube_size,cube_size,False,white,screen,window_dimensions,maze_data[y][x])
            offsetx += cube_size-1    
        offsety += cube_size-1
        offsetx = 0
    #Maze Shell#
    draw_rectangle([(0-maze_height/2),(0-maze_width/2)],maze_height,maze_width,False,white,screen,window_dimensions,[1,1,1,1])
    return [maze_width,maze_height,]

def draw_player(maze_data,maze_height,maze_width,cube_size,screen,window_dimensions,new_pos,first_pos,*args):
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
            draw_rectangle(old_player_pos,player_size,player_size,True,black,screen,window_dimensions) #Remove previous player_pos   
            draw_rectangle(player_pos,player_size,player_size,True,green,screen,window_dimensions)                   
    return new_pos

def progress_bar(width,number_of_segements,progress,screen,offset,window_dimensions):
    center = [0+offset[0],0+offset[0]]
    #Draw progress bar shell
    draw_rectangle([int(center[0]-width/2),center[1]],width,15,False,white,screen,window_dimensions,1)
    #Draw actual progress
    draw_rectangle([int(center[0]-width/2)+2,center[1]+2],int((width-4)*progress),11,True,white,screen,window_dimensions)

def draw_rectangle(startpos,width,height,fill,colour,screen,window_dimensions,*args):
    #Draws a rectangle based around 0,0 (screen center), for best use don't redraw things that are already drawn (i.e. stagnant sprites, like the maze)
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
def find_center_of_square(maze_width,maze_height,cube_size,pos): #Converts map coords to pixel measurments so that the player can be properly positioned 
    x = pos[0]                                                   #Currently while the player isn't intersecting walls they don't look like they are in the center 
    y = pos[1]
    pos_in_pixels = [(0-(maze_width/2)+(cube_size-1)*x)+(0.2*cube_size),(0-(maze_height/2)+(cube_size-1)*y)+(0.2*cube_size)]
    #print(pos_in_pixels)   
    return pos_in_pixels

def alter_to_fit_scale(value):
    #Alters any variable to fit game scale
    return int(value*scale)

def alter_coords_to_fit_scale(value,full):
    #Makes coords relative to the center and fits them to game scale
    return int(full + (value*scale))

from MazeGenerationNew import generate_random_walls
maze_data = generate_random_walls(100,100)
play_maze(1500,1000,"Test Maze",maze_data)
