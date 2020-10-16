import time     
import os                   #Used to hide the initial pygame prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame               #Used to draw pixels on the screen in a window

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

def play_maze(width,height,title,maze_data):
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption(title)
    temp = 0 #Temporary Variable to manage progress of stand-in progress bar
    delta_time = 0
    loading = True
    first_frame = True
    running = True
    while running:
        start_time = time.time() #For measuring execution time, for debug and for testing program speed    
        #Anything in this loop is run every frame while running is True
        for event in pygame.event.get():            
            #Makes program stop when user closes the window
            if event.type == pygame.QUIT:
                running = False
        #Game Code
        if debug:
            print(str(round((time.time() - start_time)*1000,1)) + "ms") #Prints execution time (per frame) to console
            print(temp)
        if loading == True:
            if temp >= 1:
                loading = False
                screen.fill(default)
            else:
                progress_bar(100,4,temp,screen,[0,0],[width,height]) #This is a stand-in progress bar to test how it would look, the real one's progression would be based on the actual loading progression
                temp += 1 * delta_time
        elif loading == False:
            if first_frame == True:
                first_frame = False
                draw_maze([width,height],10,screen,maze_data)
        pygame.display.flip()
        delta_time = time.time() - start_time #delta_time is the time the program took to execute the last frame
    pygame.quit()

def progress_bar(width,number_of_segements,progress,screen,offset,window_dimensions):
    center = [0+offset[0],0+offset[0]]
    #Draw progress bar shell
    draw_rectangle([int(center[0]-width/2),center[1]],width,15,False,white,screen,window_dimensions,1)
    #Draw actual progress
    draw_rectangle([int(center[0]-width/2)+2,center[1]+2],int((width-4)*progress),11,True,white,screen,window_dimensions)

#Both draw_outline and draw_rectangle could be combined down into a just draw_rectangle (however that can be done at a later date)
def draw_outline(startpos,width,height,colour,screen,window_dimensions,list_one):
    width = alter_to_fit_scale(width) 
    height = alter_to_fit_scale(height)
    for i in range(0,len(startpos)):
        startpos[i] = alter_coords_to_fit_scale(startpos[i],int((window_dimensions[i])/2))
    for x in range(startpos[0],startpos[0]+width):
        for y in range(startpos[1],startpos[1]+height):
            if (x in range(startpos[0]+list_one[0],startpos[0]+width-list_one[1])) and (y in range(startpos[1]+list_one[2],startpos[1]+height-list_one[3])):
                pass
            else:
                screen.set_at((x,y),colour)

def draw_rectangle(startpos,width,height,fill,colour,screen,window_dimensions,*args):
    #Draws a rectangle based around 0,0 (screen center), for best use don't redraw things that are already drawn (i.e. stagnant sprites, like the maze)
    width = alter_to_fit_scale(width)
    height = alter_to_fit_scale(height)
    for i in range(0,len(startpos)):
        startpos[i] = alter_coords_to_fit_scale(startpos[i],int((window_dimensions[i])/2))
    for x in range(startpos[0],startpos[0]+width):
        for y in range(startpos[1],startpos[1]+height):
            screen.set_at((x,y),colour)
    if not fill:
        try:  #This allows rectangles to not be filled with the weight of thier lines controlled by args[0] (if it's entered as an int)
            for x in range(startpos[0]+args[0],startpos[0]+width-args[0]):
                for y in range(startpos[1]+args[0],startpos[1]+height-args[0]):
                    screen.set_at((x,y),default)
        except: #Allows different sides of the cube to have different line weights controlled by args[0] (if it's entered as a list of ints)
            for x in range(startpos[0]+args[0][0],startpos[0]+width-args[0][1]):
                for y in range(startpos[1]+args[0][2],startpos[1]+height-args[0][3]):
                    screen.set_at((x,y),default)

def alter_to_fit_scale(value):
    #Alters any variable to fit game scale
    return (value*scale)

def alter_coords_to_fit_scale(value,full):
    #Makes coords relative to the center and fits them to game scale
    return (full + (value*scale))

def draw_maze(window_dimensions,cube_size,screen,maze_data):
    #This function will draw the maze based on maze data generated in the maze generation script
    #Content of maze#
    maze_width = len(maze_data) * (cube_size / 1.1) #Divided by 1.1 to shift maze into proper place when cubes slightly overlap each other (represented by the offsets being cube_size-1)
    maze_height = len(maze_data[0]) * (cube_size / 1.1)    
    offsety = 0
    offsetx = 0
    for x in range(0,len(maze_data)):
        for y in range(0, len(maze_data[x])):
            draw_rectangle([int(0-(maze_height/2)+offsetx),int((-maze_width/2)+offsety)],cube_size,cube_size,False,white,screen,window_dimensions,maze_data[x][y])
            offsetx += cube_size-1         
        offsety += cube_size-1  
        offsetx = 0
    #Maze Shell#
    draw_outline([int(0-maze_height/2),int(0-maze_width/2)],((cube_size-1)*len(maze_data[0])),((cube_size-1)*len(maze_data)),white,screen,window_dimensions,[1,1,1,1])

from MazeGenerationNew import generate_random_walls
maze_data = generate_random_walls(100,100)
play_maze(1000,1000,"Test Maze",maze_data)
