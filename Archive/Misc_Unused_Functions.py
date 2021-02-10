def draw_maze(window_dimensions,cube_size,win_pos_x,win_pos_y,screen,maze_data): #This function is no longer used but should be kept so I can write about it in the writing section the NEA
    #Content of maze#
    maze_width = (len(maze_data) * (cube_size-1))+1 #Calculates the dimensions of the maze, taking into account the fact the squares overlap
    maze_height = (len(maze_data[0]) * (cube_size-1))+1    
    offsety = 0
    offsetx = 0
    for y in range(0,len(maze_data)):
        for x in range(0, len(maze_data[y])):
            draw_rectangle([(0-(maze_height/2)+offsetx),((0-maze_width/2)+offsety)],cube_size,cube_size,False,white,screen,window_dimensions,maze_data[y][x])
            if won([x,y],win_pos_x,win_pos_y):
                draw_rectangle([(0-(maze_height/2)+offsetx+2),((0-maze_width/2)+offsety+2)],cube_size-4,cube_size-4,True,green,screen,window_dimensions)
            offsetx += cube_size-1    
        offsety += cube_size-1
        offsetx = 0
    return [maze_width,maze_height]
