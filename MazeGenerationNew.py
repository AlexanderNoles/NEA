#Each cell in the array/maze stores its x, y, and four ints that indicate the state of the walls
import random
import time

#How the data is encoded
empty = 0
wall = 1

def intialize_array(width,height):
    #Intialize the array
    maze_array = []
    for x in range(0,width):
        maze_array.append([])
        for y in range(0,height):
            maze_array[x].append([1,1,1,1]) #Add a blank cell with all four walls to create an array that will be altered to generate a maze, this array is the data we return
    return maze_array

def generate_random_walls(height,width):
    #Intialize the array
    maze_array = []
    temp_list = [0,0,0,0,0,0,1]
    for x in range(0,width):
        maze_array.append([])
        for y in range(0,height):
            maze_array[x].append([random.choice(temp_list),random.choice(temp_list),random.choice(temp_list),random.choice(temp_list)])
    return maze_array

def generate_walled_maze(width,height,max_weight):
    weight_group_array = []                 
    for x in range(0,width):
        weight_group_array.append([])
        for y in range(0,height):
            weight_group_array[x].append([random.randint(1,max_weight),random.randint(1,max_weight),random.randint(1,max_weight),random.randint(1,max_weight),0])   #Create a "sister" array that stores the weight values and group of each cell
    maze_array = kruskals_algorithim(weight_group_array,width,height,max_weight)
    return maze_array

def generate_circular_maze(width,height,max_weight):
    start_time = time.time()
    weight_group_array = []
    for x in range(0,width):
        weight_group_array.append([])
        for y in range(0,height):
            weight_group_array[x].append([random.randint(1,max_weight),random.randint(1,max_weight),random.randint(1,max_weight),random.randint(1,max_weight),0])
    #Manipulate the weight group array to make the algorithim generate a circular maze with random gaps in the walls
    random_center_coords = [random.randint(int(width/4),int(width*(3/4))),random.randint(int(height/4),int(height*(3/4)))]
    random_center_coords = [int(width/2),int(height/2)]
    weight_group_array[random_center_coords[0]][random_center_coords[1]] = [1,1,1,1,0]
    weight_to_change_to = 2
    dir_list = [[-1,0],[0,1],[1,0],[0,-1]]
    move_dir_dict = {
        0:[0,1],
        1:[1,0],
        2:[0,-1],
        3:[-1,0]
        }
    start_side_list = [1,3,0,2]
    for i in range(0,4):
        new_pos = (random_center_coords[0] + dir_list[i][0], random_center_coords[1]+dir_list[i][1])
        circiling = True
        move_amount = 2
        index = 0 + i 
        current_pos = new_pos
        while circiling:
            try:
                start_pos = current_pos
                side_to_remove = start_side_list[index]
                move_dir = move_dir_dict[index]               
                for j in range(0,move_amount+1):
                    current_pos = [start_pos[0]+(move_dir[0]*j),start_pos[1]+(move_dir[1]*j)]
                    if current_pos[0] < 0 or current_pos[1] < 0:
                        current_pos[len(current_pos)+2] = "error" #Intentionally cause an index error
                    weight_group_array[current_pos[0]][current_pos[1]][side_to_remove] = weight_to_change_to                    
                    if weight_to_change_to != max_weight:
                        weight_to_change_to += 1               
                move_amount += 2
                index += 1
                if index > (len(start_side_list)-1):
                    index = 0                
            except IndexError:
                circiling = False
    print(time.time() - start_time)    
    maze_array = kruskals_algorithim(weight_group_array,width,height,max_weight)
    print(time.time() - start_time) 
    return maze_array
    

def kruskals_algorithim(weight_group_array,width,height,max_weight): #Based on the algorithim as described in "Mazes for Programmers"
    maze_array = intialize_array(width,height)
    group_designation = 1                                                                                                                                           
    temp_list_empty = False
    while not all_in_one_group(weight_group_array,height,width) or not temp_list_empty: #Only ends loop when no new corridors can be checked and all the corriders are in the same group
        temp_list = lowest_values_pos(weight_group_array,width,height,max_weight+1)
        if temp_list == []:
            temp_list_empty = True
        else:
            dict_one = {
                0:[0,-1,1],
                1:[0,1,0],
                2:[-1,0,3],
                3:[1,0,2]
                }
            for pos in temp_list:
                can_connect = True
                difference = dict_one[pos[2]]
                current_pos_group = (weight_group_array[pos[0]][pos[1]])[4]                
                try:
                    if pos[0]+difference[0] == -1 or pos[1]+difference[1] == -1:
                        error = pos[100]
                    connected_pos_group = (weight_group_array[pos[0]+difference[0]][pos[1]+difference[1]])[4]
                    if current_pos_group == 0:
                        if connected_pos_group == 0:
                            (weight_group_array[pos[0]][pos[1]])[4] = group_designation
                            (weight_group_array[pos[0]+difference[0]][pos[1]+difference[1]])[4] = group_designation
                            group_designation += 1
                        else:
                            (weight_group_array[pos[0]][pos[1]])[4] = (weight_group_array[pos[0]+difference[0]][pos[1]+difference[1]])[4]
                    else:
                        if current_pos_group == connected_pos_group:
                            can_connect = False
                        elif connected_pos_group == 0:
                            (weight_group_array[pos[0]+difference[0]][pos[1]+difference[1]])[4] = current_pos_group
                        elif connected_pos_group != 0:
                            group_pos = get_all_in_group(weight_group_array,width,height,connected_pos_group)
                            for pos2 in group_pos:
                                (weight_group_array[pos2[0]][pos2[1]])[4] = current_pos_group
                    if(can_connect):
                        (maze_array[pos[0]][pos[1]])[pos[2]] = 0
                        (maze_array[pos[0]+difference[0]][pos[1]+difference[1]])[difference[2]] = 0
                    (weight_group_array[pos[0]][pos[1]])[pos[2]] = max_weight+2
                    (weight_group_array[pos[0]+difference[0]][pos[1]+difference[1]])[difference[2]] = max_weight+2
                except IndexError:
                    (weight_group_array[pos[0]][pos[1]])[pos[2]] = max_weight+2
                    if (weight_group_array[pos[0]][pos[1]])[4] == 0:
                        (weight_group_array[pos[0]][pos[1]])[4] = group_designation
                        group_designation += 1
    return maze_array

def get_all_in_group(wg_array,width,height,group):  #Gets the positions of all the cells that have the group specified
    temp_array = []
    for x in range(0,width):
        for y in range(0,height):
            if (wg_array[x][y])[4] == group:
                temp_array.append([x,y])
    return temp_array
                
    
def all_in_one_group(wg_array,height,width):    #Checks to see if every cell is in a singular group (a.k.a every cell can be reached from any other cell)
    returned = True
    first_group = "null"
    for x in range(0,width):
        for y in range(0,height):
            temp = (wg_array[x][y])[4]
            if first_group == "null":
                first_group = temp
            if temp != first_group or temp == 0:
                returned = False
    return returned

def lowest_values_pos(wg_array,width,height,compared_to):   #Finds all the connections in the maze with the lowest weight value
    temp_list = []
    for x in range(0,width):
        for y in range(0,height):
            for i in range(0,4):
                if wg_array[x][y][i] < compared_to:
                    compared_to = wg_array[x][y][i]
                    temp_list = []
                    temp_list.append([x,y,i])
                elif wg_array[x][y][i] == compared_to:
                    temp_list.append([x,y,i])
    return temp_list

def main(width,height,max_weight,maze_type):
    if maze_type == "normal":
        maze_data = generate_walled_maze(width,height,max_weight)
    elif maze_type == "circular":
        maze_data = generate_circular_maze(width,height,max_weight)
    return maze_data
