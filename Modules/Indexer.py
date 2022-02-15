import os
import sqlite3
import time

from Modules import Database as DBM
from Modules import Drive_Partition_Scanner as DPS
from Modules import Size_Converter as SC
from Modules import Print_Stats as PS

# Initialize the database details
DB_NAME = 'List.db'                     # Database name
FILE_TABLE_NAME = 'FileList'            # Name of the table that stores filenames
FOLDER_TABLE_NAME = 'FolderList'        # Name of the table that stores folder names

# Note the starting time
Start_Time = time.time()

# Initiliaze the counters and other varibales
No_Of_Files = 0
No_Of_Folders = 0
Temp_File_Details = []
Temp_Folder_Details = []
Temp_Chunk_Size = 750

# Create and connect to a database
conn = sqlite3.connect(DB_NAME)             # Create & connect database if not present, or else connect to pre-existing database
cur = conn.cursor()                         # Assign a cursor

# Drop pre-existing tables
DBM.DropTable(cur, FILE_TABLE_NAME)         
DBM.DropTable(cur, FOLDER_TABLE_NAME)


# Create Tables
DBM.CreateTable(cur, FILE_TABLE_NAME)
DBM.CreateTable(cur, FOLDER_TABLE_NAME)

# After all the scrapping and database fill up is done, the data remaining ( < 'Temp_Chunk_Size') in 'Temp_File_Details' is then wrote to database
def flush_all():
    DBM.FillDatabase(Temp_File_Details, cur, FILE_TABLE_NAME)
    DBM.FillDatabase(Temp_Folder_Details, cur, FOLDER_TABLE_NAME)

# Main
def NameScrapper(ScrapePath):

    global No_Of_Folders
    global No_Of_Files

    global Temp_File_Details                                                            # For appending till there are few entries, then dump the whole list into database and empty it.
    global Temp_Folder_Details
                                                                                        # If the directory has permission to scan then execute this 
    for File_OR_Folder_Name in os.listdir(ScrapePath):                                  # Itterate over file/folder names present in the current directory
        Absolute_File_Or_Folder_Name = ScrapePath + '\\' + File_OR_Folder_Name
        
        if os.path.isdir(Absolute_File_Or_Folder_Name) == True:                         # If FOLDER
            No_Of_Folders = No_Of_Folders + 1                                           # Increment FOLDER counter

            Folder_Details = [File_OR_Folder_Name, 'NULL', Absolute_File_Or_Folder_Name]        # [foldername, size, absolute path]
            Temp_Folder_Details.append(Folder_Details)
            try:                                                                        # Some folders aren't scrapable due to system permission (like $RECYCLE.BIN)
                NameScrapper(ScrapePath + '\\' + File_OR_Folder_Name)                   # Scan the folder content using recursion
            except:
                pass                                                                    # Passing those cases as theie details are already noted in database 

        else:                                                                           # If FILE
            No_Of_Files = No_Of_Files + 1                                               # Increment FILE counter
            try:                                                                        # Sometimes the size throws error due to system permission
                File_Size = os.path.getsize(Absolute_File_Or_Folder_Name)               # Get file size
            except:
                File_Size = -1                                                          # Setting dummy size
            File_Abs_Path = Absolute_File_Or_Folder_Name                                # Get file Absolute Path
            File_Name = File_OR_Folder_Name                                             # Get file name

            File_Details = [File_Name, SC.Converter(File_Size), File_Abs_Path]          # SC.Converter() - To convert bytes to readable size notations

            # print(File_Details)
            Temp_File_Details.append(File_Details)

    if ( (len(Temp_File_Details) % Temp_Chunk_Size) == 0):                              # Write the data to database if length of 'Temp_File_Details' == 'Temp_Chunk_Size'                         
        DBM.FillDatabase(Temp_File_Details, cur, FILE_TABLE_NAME)
        Temp_File_Details = []                                                          # Empty the 'Temp_File_Details' list
        DBM.FillDatabase(Temp_Folder_Details, cur, FOLDER_TABLE_NAME)
        Temp_Folder_Details = []                                                        # Empty the 'Temp_Folder_Details' list

        # NOTE: THE DATA REMAINING IN THE VARIABLE 'Temp_File_Details' IN LAST ITTERATION, IS WRITTEN TO DATABASE USING 'flush_all' FUNCTION  


# Path to scrape
ScrapePath = 'Y:\\'
NameScrapper(ScrapePath)
flush_all()                                                 # Write the data remaining from 'Temp_File_Details' which is < 'Temp_Chunk_Size' to database

AvaliableDrives = DPS.Get_Avaliable_Drives()
#     ScrapePath11 = DPS.Get_Avaliable_Drives()
#     for i in ScrapePath11:
#         NameScrapper(i)
#         flush_all()

conn.commit()                   # Commit the changes to database
conn.close()                    # Close the connection

# Display the overall stats
PS.PrintStats([No_Of_Folders, No_Of_Files, time.time(), Start_Time])

print(AvaliableDrives)