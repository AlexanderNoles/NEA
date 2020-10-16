import time
import pygame               #Used to draw pixels on the screen in a window

#colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
default = black             #Equivalent to background colour

#other
scale = 2 #Has to be an int
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
                draw_maze(width,height,screen)
        pygame.display.flip()
        delta_time = time.time() - start_time #delta_time is the time the program took to execute the last frame
    pygame.quit()

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
    for x in range(startpos[0],startpos[0]+width):
        for y in range(startpos[1],startpos[1]+height):
            screen.set_at((x,y),colour)
    if not fill:
        for x in range(startpos[0]+args[0],startpos[0]+width-args[0]):
            for y in range(startpos[1]+args[0],startpos[1]+height-args[0]):
                screen.set_at((x,y),default)

def alter_to_fit_scale(value):
    #Alters any variable to fit game scale
    return (value*scale)

def alter_coords_to_fit_scale(value,full):
    #Makes coords relative to the center and fits them to game scale
    return (full + (value*scale))

def draw_maze(width,height,screen):
    #This function will draw the maze based on maze data generated in the maze generation scripts (currently no data can be passed as the maze generation scripts need to be rewritten)
    draw_rectangle([int(0-20/2),int(0-20/2)],20,20,False,white,screen,[width,height],1)
    pass

play_maze(1000,1000,"Test Maze","")
