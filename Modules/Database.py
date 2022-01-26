import sqlite3


# To create database 
def CreateDatabase(DB_NAME, TABLE_NAME):
    conn = sqlite3.connect(DB_NAME)                     # Create & connect database if not present, or else connect to pre-existing database
    cur = conn.cursor()                                 # Assign a cursor

    try:                                                # Try to create a table if not present
        cur.execute(f'''CREATE TABLE {TABLE_NAME}(
            filename text,
            filesize text,
            path text
        ) 
        ''')
    except:                                             # If table already present 
        print('[*] : Table already exists')

    conn.commit()                                       # Commit the changes to database
    conn.close()                                        # Close the connection


# To fill data in database (list of list)
def FillDatabase(To_Fill, DB_NAME, TABLE_NAME):                              # FillDatabase([['0bd2c1d8ecd9daba0e2471ba75ad6adefc7051', '154 Bytes', 'E:\\PROGRAMS\\YoutubeData\\.git\\objects\\fe\\0bd2c1d8ecd9daba0e2471ba75ad6adefc7051']])
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for element in To_Fill:                                                                 # Itterating over INNER list to get elements different attributes
        cur.execute(f'INSERT INTO {TABLE_NAME} VALUES (:filename, :filesize, :path)',   # Seperating the attributes and adding them to database
        {
            'filename': element[0],
            'filesize': element[1],
            'path': element[2]
        }
        )

    conn.commit()
    conn.close()


# To search the database
def Searching(To_Search, DB_NAME, TABLE_NAME):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    output1 = cur.execute(f'SELECT * FROM {TABLE_NAME} WHERE filesize=?', (To_Search,))
    print(output1.fetchall())                           # Get all the entries that match the query

    conn.commit()
    conn.close()


# To drop a certain table
def DropTable(DB_NAME, TABLE_NAME):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute(f'DROP TABLE {TABLE_NAME}')         # Dropping the table
        print('Table dropped')
    except:
        print('Table is not present')

    conn.commit()
    conn.close()

# [ DEBUGGING ]

# CreateDatabase()

# FillDatabase([['0bd2c1d8ecd9daba0e2471ba75ad6adefc7051', '154 Bytes', 'E:\\PROGRAMS\\YoutubeData\\.git\\objects\\fe\\0bd2c1d8ecd9daba0e2471ba75ad6adefc7051']])

# Searching('20 Bytes')

# To view the datatypes: PRAGMA table_info(table-name);