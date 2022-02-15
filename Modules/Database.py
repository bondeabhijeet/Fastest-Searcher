import time
import sqlite3
# To create database 
def CreateTable(cur, TABLE_NAME):
    try:                                                # Try to create a table if not present
        cur.execute(f'''CREATE TABLE {TABLE_NAME}(
            filename text,
            filesize text,
            path text
        ) 
        ''')
    except:                                             # If table already present 
        print('[*] : Table already exists')


# To fill data in database (list of list)
def FillDatabase(To_Fill, cur, TABLE_NAME):             # FillDatabase([['0bd2c1d8ecd9daba0e2471ba75ad6adefc7051', '154 Bytes', 'E:\\PROGRAMS\\YoutubeData\\.git\\objects\\fe\\0bd2c1d8ecd9daba0e2471ba75ad6adefc7051']])

    for element in To_Fill:                                                                 # Itterating over INNER list to get elements different attributes
        cur.execute(f'INSERT INTO {TABLE_NAME} VALUES (:filename, :filesize, :path)',       # Seperating the attributes and adding them to database
        {
            'filename': element[0],
            'filesize': element[1],
            'path': element[2]
        }
        )


# To search the database
def SearchDatabase(curr, To_Search):#, cur, TABLE_NAME):
    start = time.time()
    conn = sqlite3.connect('List.db')
    cur = conn.cursor()
    

    # output1 = cur.execute(f'SELECT * FROM FileList WHERE filename=?', (To_Search,))     # Searching the database
    output1 = cur.execute(f'SELECT * FROM FileList WHERE filename like "%{To_Search}%"')     # Searching the database
    # print(output1.fetchall())                                                               # Get all the entries that match the query
    output1 = output1.fetchall()                                                               # Get all the entries that match the query
    
    conn.commit()
    conn.close()
    print(time.time()-start)
    return output1

# To drop a certain table
def DropTable(cur, TABLE_NAME):
    try:
        cur.execute(f'DROP TABLE {TABLE_NAME}')         # Dropping the table
        print('Table dropped')
    except:
        print('Table is not present')

def ShowAllDB(curr):
    output1 = curr.exectue(f'SELECT * FROM FileList WHERE filename like "%%"')
    output1 = output1.fetchall()
    return output1

# [ DEBUGGING ]

# CreateDatabase()

# FillDatabase([['0bd2c1d8ecd9daba0e2471ba75ad6adefc7051', '154 Bytes', 'E:\\PROGRAMS\\YoutubeData\\.git\\objects\\fe\\0bd2c1d8ecd9daba0e2471ba75ad6adefc7051']])

# Searching('ok')

# To view the datatypes: PRAGMA table_info(table-name);