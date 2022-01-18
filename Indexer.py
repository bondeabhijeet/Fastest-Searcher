import os
from sqlite3 import connect
import time
from Modules import Database as DBM

# Note the starting time
Start_Time = time.time()

# Initiliaze the counters
No_Of_Files = 0
No_Of_Folders = 0
Temp_File_Details = []
Temp_Chunk_Size = 500

# Drop pre-existing table
DBM.DropTable()

# Create a Database and Table
DBM.CreateDatabase()

# To convert bytes to readable size notations
def Converter(Size_Bytes):

    File_Sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    Iter_Counter = 0                                        # To keep track of number of times the size is divided by 1024

    while(Size_Bytes > 1024):
        Size_Bytes = Size_Bytes / 1024                      # No. of times size is divided by 1024 is located in File_Sizes
        Iter_Counter = Iter_Counter + 1

    Final_Size = str( round(Size_Bytes, 2) ) + ' ' + File_Sizes[Iter_Counter]       # Rounding off to 2 decimals and creating final string
    return(Final_Size)

# After all the scrapping and database fill up is done, the data remaining ( < 'Temp_Chunk_Size') in 'Temp_File_Details' is then wrote to database
def flush_all():
    DBM.FillDatabase(Temp_File_Details)

# Main
def NameScrapper(ScrapePath):

    global No_Of_Folders
    global No_Of_Files

    global Temp_File_Details                                                            # For appending till there are few entries, then dump the whole list into database and empty it.

    for File_OR_Folder_Name in os.listdir(ScrapePath):                                  # Itterate over file/folder names present in the current directory
        Absolute_File_Or_Folder_Name = ScrapePath + '\\' + File_OR_Folder_Name
        
        if os.path.isdir(Absolute_File_Or_Folder_Name) == True:                         # If FOLDER
            No_Of_Folders = No_Of_Folders + 1                                           # Increment FOLDER counter
            NameScrapper(ScrapePath + '\\' + File_OR_Folder_Name)                       # Scan the folder content using recursion

        else:                                                                           # If FILE
            No_Of_Files = No_Of_Files + 1                                               # Increment FILE counter
            File_Size = os.path.getsize(Absolute_File_Or_Folder_Name)                   # Get file size
            File_Abs_Path = Absolute_File_Or_Folder_Name                                # Get file Absolute Path
            File_Name = File_OR_Folder_Name                                             # Get file name

            File_Details = [File_Name, Converter(File_Size), File_Abs_Path]

            print(File_Details)
            Temp_File_Details.append(File_Details)
    
            # print(File_Abs_Path, end='   ')
            # print(Converter(File_Size), end='    ')
            # print(File_Name)

    if ( (len(Temp_File_Details) % Temp_Chunk_Size) == 0):                              # Write the data to database if length of 'Temp_File_Details' == 'Temp_Chunk_Size'                         
        DBM.FillDatabase(Temp_File_Details)
        Temp_File_Details = []                                                          # Empty the 'Temp_File_Details' list

    # NOTE: THE DATA REMAINING IN THE VARIABLE 'Temp_File_Details' IN LAST ITTERATION, IS WRITTEN TO DATABASE USING 'flush_all' FUNCTION                
    # writetofile(Temp_File_Details)

# [ DEBUGGING ]
def writetofile(content1):
    with open('names1.txt', 'a') as f:
        for i in content1:
            for j in i:
                f.write(j)
            f.write('\n')

# Path to scrape
ScrapePath = 'E:\\PROGRAMS'
NameScrapper(ScrapePath)
flush_all()                                                 # Write the data remaining from 'Temp_File_Details' which is < 'Temp_Chunk_Size' to database

# Display the overall stats
print('Total folders: ', No_Of_Folders)
print('Total files: ', No_Of_Files)
print('Total files and folders: ', No_Of_Files + No_Of_Folders)

print(f'Time taken to execute: {time.time() - Start_Time} Seconds')
print(f'Average speed: {(No_Of_Files) / (time.time() - Start_Time)} Entries / Second')
