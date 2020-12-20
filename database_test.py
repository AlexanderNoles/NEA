import sqlite3

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)       
    except Error as e:
        print(e)
    return connection

conn = create_connection('Test.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()

#Create Test_Table_One
c.execute('''CREATE TABLE TEST_ONE
(generated_id INTEGER PRIMARY KEY,
Client_Name TEXT)''')

#Create Test_Table_Two
c.execute('''CREATE TABLE TEST_TWO
(test_id INTEGER PRIMARY KEY,
Completed_Levels_Normal TEXT,
Completed_Levels_Labyrinth TEXT,
generated_id INT,
FOREIGN KEY (generated_id) REFERENCES TEST_ONE(generated_id))''')

conn.commit()
