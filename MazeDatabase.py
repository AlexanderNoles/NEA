import sqlite3
from sqlite3 import Error

#DATABASES
#Users table stores name and user_id + any additional information needed
#CompletedLevels table stores the completed levels linked to the foreign key user_id and a primary key completed_id. There will be two columns, one for normal mazes, one for diamond mazes
#the completed levels will be serialized as such (1#3#4#12...) and when the string is imported it will be split into a list.

def main_database():
    user_table = """ CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY,
username text NOT NULL
); """
    completed_levels_table = """ CREATE TABLE IF NOT EXISTS completedLevels (
id integer PRIMARY KEY,
normal_maze text,
diamond_maze text,
user_id integer NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id)
); """    
    connection = create_connection(r"Maze.db")
    if connection is not None:
        create_table(connection,user_table)
        create_table(connection,completed_levels_table)
    else:
        print("Database Connection Error")
    return connection

def create_new_user(connection, username):
    #Create the new user
    new_user_sql = "INSERT INTO users(username) VALUES(?)"
    cursor = connection.cursor()
    cursor.execute(new_user_sql, (username,))
    user_id = cursor.lastrowid
    connection.commit()
    #Then create the sibling entry in the CompletedLevels table based of the generated user_id
    new_completed_levels_sql = "INSERT INTO completedLevels(normal_maze, diamond_maze, user_id) VALUES(?,?,?)"
    cursor = connection.cursor()
    cursor.execute(new_completed_levels_sql, ("","",user_id))
    connection.commit()

def delete_user(connection, user_id):
    pass

def get_list_of_users(connection):
    user_list = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    for row in result:
        user_list.append((str(row)[1:-1]).split(','))
    return user_list

def add_completed_level(connection,level_number,maze_type, user_id):    #Uses the user id to alter the user's completed levels
    pass

def get_list_of_completed_levels(connection, user_id):
    pass

            
def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connection

def create_table(connection, create_table):
    try:
        cursor = connection.cursor()
        cursor.execute(create_table)
    except Error as e:
        print(e)
        
#main_database()
