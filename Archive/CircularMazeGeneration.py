from random import randint
import random
import math
#from numpy.random import randint
wall = '⬛'
empty = '⬜'
tunnel = '❏'
#This algorthim generates a braid maze (where one point in the maze can be reached from any other but the maze can contain loops)

def generate_lists(x):
    #Generates a 2-D array to serve as the maze
    #Maze coords start at the top left
    list_one = []
    for i in range(0,x):
        temp_list = []
        for j in range(0,x):
            temp_list.append(empty)
        list_one.append(temp_list)
    return list_one

def create_walls(i1,i2,maze):
    for i in range(i1,i2+1):
        maze[i1][i] = wall
        maze[i2][i] = wall
        maze[i][i1] = wall
        maze[i][i2] = wall
    return maze

def non_corner_check(y,x,maze):
    try:
        if (maze[y-1][x] == wall) and (maze[y+1][x] == wall):
            return True
        elif (maze[y][x-1] == wall) and (maze[y][x+1] == wall):
            return True
        else:
            return False
    except:
        return False

def destroy_random_walls(maze,num_to_destroy,diameter):
    for i in range(0,num_to_destroy):
        while True:
            random_y = (randint(0,diameter))#[0]
            random_x = (randint(0,diameter))#[0]
            vaild = non_corner_check(random_y,random_x,maze)
            if vaild == False:
                pass
            else:
                maze[random_y][random_x] = empty
                break
    return maze

def generate_circular_maze(diameter): #The maze isn not actually circular but rather a circular style maze where you start at the center and move outwards
    diameter = (diameter//3)*3
    maze = generate_lists(diameter)
    center = math.ceil(diameter/2) -1
    maze[center-1][center] = empty
    radius = 1
    while (radius*2) < diameter: #Create the walls
        maze = create_walls(center-radius,center+radius,maze)
        radius = radius + 2
    maze = destroy_random_walls(maze,diameter*15,diameter)
    # TUNNELS #
    num_of_tunnels = int(diameter/10)
    tunnels = []
    if num_of_tunnels%2 != 0:
        num_of_tunnels + 1
    for  i in range(0,num_of_tunnels):
        while True:
            random_y = (randint(0,diameter-1))#[0]
            random_x = (randint(0,diameter-1))#[0]
            if (maze[random_y][random_x]) == empty:
                tunnels.append([random_y,random_x])
                maze[random_y][random_x] = tunnel
                break
    return maze, tunnels

maze = generate_circular_maze(45) #45 is the max the console can display without breaking the text into multiple lines
#for i in range(0,len(maze[0])):
    #for j in range(0,len(maze[0][i])):
        #print(maze[0][i][j],end=' ')
    #print('')
#print(maze[1])
#input()
