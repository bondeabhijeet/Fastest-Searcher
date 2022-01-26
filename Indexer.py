import os
from sqlite3 import connect
import time
from Modules import Database as DBM
from Modules import Drive_Partition_Scanner as DPS
from Modules import Size_Converter as SC

# Initialize the database details
DB_NAME = 'List.db'
FILE_TABLE_NAME = 'FileList'
FOLDER_TABLE_NAME = 'FolderList'

# Note the starting time
Start_Time = time.time()

# Initiliaze the counters
No_Of_Files = 0
No_Of_Folders = 0
Temp_File_Details = []
Temp_Folder_Details = []
Temp_Chunk_Size = 750


# Drop pre-existing tables
DBM.DropTable(DB_NAME, FILE_TABLE_NAME)
DBM.DropTable(DB_NAME, FOLDER_TABLE_NAME)

# Create a Database and Tables
DBM.CreateDatabase(DB_NAME, FILE_TABLE_NAME)
DBM.CreateDatabase(DB_NAME, FOLDER_TABLE_NAME)

# After all the scrapping and database fill up is done, the data remaining ( < 'Temp_Chunk_Size') in 'Temp_File_Details' is then wrote to database
def flush_all():
    DBM.FillDatabase(Temp_File_Details, DB_NAME, FILE_TABLE_NAME)
    DBM.FillDatabase(Temp_Folder_Details, DB_NAME, FOLDER_TABLE_NAME)

# Main
def NameScrapper(ScrapePath):

    global No_Of_Folders
    global No_Of_Files

    global Temp_File_Details                                                            # For appending till there are few entries, then dump the whole list into database and empty it.
    global Temp_Folder_Details

    try:                                                                                    # If the directory has permission to scan then execute this 
        for File_OR_Folder_Name in os.listdir(ScrapePath):                                  # Itterate over file/folder names present in the current directory
            Absolute_File_Or_Folder_Name = ScrapePath + '\\' + File_OR_Folder_Name
            
            if os.path.isdir(Absolute_File_Or_Folder_Name) == True:                         # If FOLDER
                No_Of_Folders = No_Of_Folders + 1                                           # Increment FOLDER counter

                Folder_Details = [File_OR_Folder_Name, 'NULL', Absolute_File_Or_Folder_Name]
                Temp_Folder_Details.append(Folder_Details)

                NameScrapper(ScrapePath + '\\' + File_OR_Folder_Name)                       # Scan the folder content using recursion

            elif os.path.isfile(Absolute_File_Or_Folder_Name) == True:                      # If FILE
                No_Of_Files = No_Of_Files + 1                                               # Increment FILE counter
                File_Size = os.path.getsize(Absolute_File_Or_Folder_Name)                   # Get file size
                File_Abs_Path = Absolute_File_Or_Folder_Name                                # Get file Absolute Path
                File_Name = File_OR_Folder_Name                                             # Get file name

                File_Details = [File_Name, SC.Converter(File_Size), File_Abs_Path]          # SC.Converter() - To convert bytes to readable size notations

                print(File_Details)
                Temp_File_Details.append(File_Details)
        
                # print(File_Abs_Path, end='   ')
                # print(Converter(File_Size), end='    ')
                # print(File_Name)

        if ( (len(Temp_File_Details) % Temp_Chunk_Size) == 0):                              # Write the data to database if length of 'Temp_File_Details' == 'Temp_Chunk_Size'                         
            DBM.FillDatabase(Temp_File_Details, DB_NAME, FILE_TABLE_NAME)
            Temp_File_Details = []                                                          # Empty the 'Temp_File_Details' list
            DBM.FillDatabase(Temp_Folder_Details, DB_NAME, FOLDER_TABLE_NAME)
            Temp_Folder_Details = []                                                        # Empty the 'Temp_Folder_Details' list


        # NOTE: THE DATA REMAINING IN THE VARIABLE 'Temp_File_Details' IN LAST ITTERATION, IS WRITTEN TO DATABASE USING 'flush_all' FUNCTION  
                    
        # writetofile(Temp_File_Details)
    except:                                                                                 # If there are not enough permission
        File_Folder_Name = os.path.basename(ScrapePath)                                     # Get directory name from its path

        No_Of_Folders = No_Of_Folders + 1                                                   # Incrememt counter

        Folder_Details = [File_Folder_Name, 'NULL', ScrapePath]

        Temp_Folder_Details.append(Folder_Details)


# Path to scrape
ScrapePath = 'E:\\PROGRAMS'
NameScrapper(ScrapePath)
flush_all()                                                 # Write the data remaining from 'Temp_File_Details' which is < 'Temp_Chunk_Size' to database

AvaliableDrives = DPS.Get_Avaliable_Drives()
#     ScrapePath11 = DPS.Get_Avaliable_Drives()
#     for i in ScrapePath11:
#         NameScrapper(i)
#         flush_all()

# Display the overall stats
print('Total folders: ', No_Of_Folders)
print('Total files: ', No_Of_Files)
print('Total files and folders: ', No_Of_Files + No_Of_Folders)
time_taken = time.time() -Start_Time
print(f'Time taken to execute: {time.time() - Start_Time} Seconds')
print(f'Average speed: {(No_Of_Files) / (time.time() - Start_Time)} Entries / Second')
print(AvaliableDrives)
