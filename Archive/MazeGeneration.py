import random
from random import choice
from random import randint
#import numpy
#from PIL import Image

wall = '⬛'
empty = '⬜'
tunnel = '❏'
low_prob = 1
high_prob = 0
#This algorthim always generates a perfect maze (where one point in the maze can be reached from any other but the maze cannot contain loops)

def generate_lists(x,y):
    #Generates a 2-D array to serve as the maze
    #Maze coords start at the top left
    list_one = []
    for i in range(0,y):
        temp_list = []
        for j in range(0,x):
            temp_list.append(wall)
        list_one.append(temp_list)
    return list_one

def indivdual_cell_test(y,x,active,maze):
    #In this case 'True' means it's a valid cell
    try:
        current_pos = maze[y][x]
        if current_pos == empty and ((y == active[0] and x == active[1]) == False):
            return False
        else:
            return True
    except:
        return True
    pass

def tests(new_pos,active,maze):
    #This function checks a cell to see if that cell is filled or empty. All the cells need to return True for the new empty to be placed
    north = indivdual_cell_test((new_pos[0]-1),new_pos[1],active,maze)
    south = indivdual_cell_test((new_pos[0]+1),new_pos[1],active,maze)
    east = indivdual_cell_test(new_pos[0],new_pos[1]+1,active,maze)
    west = indivdual_cell_test(new_pos[0],new_pos[1]-1,active,maze)
    if west and east and north and south:
        return 'valid'
    else:
        return 'invalid'


def generate_maze(x,y): #similar_limit defines how many iterations the generation results in the same maze before it is decided that no more corridors can be made a.k.a the amount of corridors the maze has
    maze = generate_lists(x,y)        #x and y defines the width and height of the maze
    # ALGORTHIM FOR BASIC PATH #
    similar_limit = x*x
    similar_count = 0
    x -= 1
    y -= 1
    start_pos = [y,0]
    maze[start_pos[0]][start_pos[1]] = empty
    active = start_pos
    pre_pos = [0,0]
    non_stopped = True
    directions_dict = {'n':-1,'s':1,'e':1,'w':-1}
    probability = [low_prob,low_prob,low_prob,low_prob]
    previous_maze_iter = [[]]
    while non_stopped == True:
        try:
            #print(probability) #DEBUG
            #Handles the creation of corridors in the maze
            direction = (choice(list(directions_dict)))[0]
            #print(direction) #DEBUG
            probability = [low_prob,low_prob,low_prob,low_prob]
            #print("Confirm One") #DEBUG
            try:
                #Finding a new position
                if direction == 'n' or direction == 's':
                    new_pos = [(active[0] + directions_dict[direction]),active[1]]
                    if direction == 'n':
                        probability[0] = high_prob
                    else:
                        probability[1] = high_prob
                else:
                    new_pos = [active[0],(active[1] + directions_dict[direction])]
                    if direction == 'e':
                        probability[2] = high_prob
                    else:
                        probability[3] = high_prob
                #print(new_pos) #DEBUG
                if new_pos == pre_pos:              #This is to stop the generator going back on it self
                    del directions_dict[direction]
                else:
                    #print("Confirm Two") #DEBUG
                    #Testing current squares
                    #########################################################
                    #This tests to see if the new position is within the maze
                    if (new_pos[1] > x or new_pos[1] < 0) or (new_pos[0] > y or new_pos[0] < 0):
                        intentional_error = broken_list['FAKE']
                    #########################################################
                    #print(maze[new_pos[0]][new_pos[1]]) #DEBUG
                    #print("Confirm Three") #DEBUG
                    result = tests(new_pos,active,maze) #Test squares around the new_pos
                    if result == 'valid': #'valid' means the new_pos is in a valid position
                        #print("Confirm Four") #DEBUG
                        directions_dict = {'n':-1,'s':1,'e':1,'w':-1}
                        maze[new_pos[0]][new_pos[1]] = empty
                        pre_pos = active
                        active = new_pos
                    else:
                        del directions_dict[direction]
            except:
                del directions_dict[direction]
        except:
            #Makes the program create a new corridor braching off the original and then will create another corridor branching of one of those and so on and so on
            #until there are no possible more corridors
            picking = True
            while picking:
                random_y = ((randint(0,y)))#(randint(low=0,high=y,size=1))[0]
                random_x = ((randint(0,x)))#(randint(low=0,high=x,size=1))[0]
                if maze[random_y][random_x] == empty:
                    active = [random_y,random_x]
                    #print("Active:" , active) #DEBUG
                    directions_dict = {'n':-1,'s':1,'e':1,'w':-1} #Resets the direction dict as otherwise it would just have nothing in it resulting in nothing happening
                    probability = [low_prob,low_prob,low_prob,low_prob]
                    picking = False                    
            if previous_maze_iter == maze:
                if similar_count == similar_limit:
                    non_stopped = False
                else:
                    similar_count += 1
                    #print(similar_count) #DEBUG
            previous_maze_iter = maze
    # ALGORTHIM FOR ADDITION OF TUNNELS #
    num_of_tunnels =  int(x/10)
    tunnels = []
    if num_of_tunnels%2 != 0:
        num_of_tunnels + 1
    if num_of_tunnels == 1:
        num_of_tunnels = 0
    for  i in range(0,num_of_tunnels):
        while True:
            random_y = ((randint(0,y)))#(randint(low=0,high=y,size=1))[0]
            random_x = ((randint(0,x)))#(randint(low=0,high=x,size=1))[0]
            if (maze[random_y][random_x]) == empty:
                tunnels.append([random_y,random_x])
                maze[random_y][random_x] = tunnel
                break
    # FOR MAKING SURE THERE IS AN EXIT IN THE TOP RIGHT SO THE MAZE CAN BE SOLVED #
    for i in range(0,y):
        if (maze[i][x] == empty) or ((maze[i][x-1] == empty) and i != 0):
            maze[i][x] = empty
            break
        maze[i][x] = empty
    return maze, tunnels

# FOR TESTING #
#width = 20
#height = width
#maze = generate_maze(width,height)
#str_one = ''
#for i in range(0,len(maze[0])):
    #for j in range(0,len(maze[0][i])):
    #    str_one = str_one + (maze[0][i][j]) + ' '
    #str_one = str_one + ('\n')
#print(str_one)
#print(maze[1]) #Tunnels
#image = False
#if image == True:
    #arr = (numpy.array(maze[0])).astype(numpy.uint8) 
    #img = Image.fromarray(arr)
    #basewidth = 300
    #wpercent = (basewidth/float(img.size[0]))
    #hsize = int((float(img.size[1])*float(wpercent)))
    #img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    #img.save('my.png') 
#input()
