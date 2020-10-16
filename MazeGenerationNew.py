#Each cell in the array/maze stores its x, y, and four ints that indicate the state of the walls
import random

#How the data is encoded
empty = 0
wall = 1

def generate_random_walls(width,height):
    #Intialize the array
    maze_array = []
    for x in range(0,width):
        maze_array.append([])
        for y in range(0,height):
            maze_array[x].append([random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)])
    return maze_array

def generate_walled_maze(width,height):
    #Intialize the array
    maze_array = []
    for x in range(0,width):
        maze_array.append([])
        for y in range(0,height):
            maze_array[x].append([1,1,1,1]) #Add a blank cell with all four walls
    #Alter the array to make a maze
    #The algorithim used should move through the cells at random removing walls untill every cell has been visited
    #To decide whether a wall is removed check whether a cell has already been connected to one/two other cells
    return maze_array



