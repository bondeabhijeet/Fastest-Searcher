import tkinter as tk
from tkinter import ttk
from Modules import exit as EXIT
from Modules import Database as DBM
from Modules import FinalTable as FT
import sqlite3

# Debugging
def donothing(*args):
    print("Bmsdk kuch bhi mat type kar")
    return

DB_NAME = 'List.db'                     # Database name
FILE_TABLE_NAME = 'FileList'            # Name of the table that stores filenames
FOLDER_TABLE_NAME = 'FolderList'        # Name of the table that stores folder names

# Open the database
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Creating root window
root = tk.Tk()

# root.configure(background='#101116')

# Getting screen size
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()

# Adjusting the App window to screen size
AppWindowWidth = str( int( (ScreenWidth / 2) + 200 ))
AppWindowHeight = str( int( (ScreenHeight / 2) + 200 ))
AppWindowX = str( int( ScreenWidth / 6 ))           # Distance from left
AppWindowY = str( int( ScreenHeight / 10 ))          # Distance from top
root.geometry(f'{ AppWindowWidth }x{ AppWindowHeight }+{AppWindowX}+{AppWindowY}')

# Renaming the Window
root.title('Fastest-Searcher')

# Changing the icon of the app
root.iconbitmap('angle-circle-up.ico')

# Turn off the title bar
# root.overrideredirect(True)

# Creating Menubar
menubar = tk.Menu( root)

def exit(*args):
    EXIT.exit()

# Adding File Menu and commands
file = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu = file)
file.add_command(label='Open', command= None)
file.add_command(label='New', command=None)
file.add_command(label='Exit', command=exit, accelerator='Ctrl + W')
root.bind('<Control-w>', exit)

edit = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Search', menu = edit)
edit.add_command(label='Audios', command=None)
edit.add_command(label='Videos', command=None)
edit.add_command(label='Executable', command=None)
edit.add_command(label='Folder', command=None)
edit.add_command(label='Picture', command=None)
edit.add_command(label='Compressed', command=donothing, accelerator='Ctrl + F')
root.bind('<Control-f>', donothing)

# Creating the ENTRY field to type the search term
Query = tk.Entry(root, width=AppWindowWidth, fg='Black', bd='0', insertwidth=1, insertbackground='black', justify=tk.LEFT)
Query.config(highlightbackground='black', highlightthickness=1, fg='black')
Query.focus()                                                                       # Initialize the cursor to entry box on application start
Query.pack(padx=5, pady=5, fill='x')

Strr = [' Hello this is abhijeet.', ' Hello this is veena.', ' Hello this is Knu.', ' Hello this is Kay.', ' Hello this is K.']
records = [['Ready for Searching...', 'Type to search...', 'System is ready...']]
MyTree = None
MyTree = FT.display(root, records, 700)
# for strr in Strr:
#     p = Label(root, text=strr, anchor='w', width=500, background='#101116', foreground='#00a2ff', font=('Helvetica', 9, 'bold'))           # Anchors :- https://www.tutorialspoint.com/python/tk_anchors.htm

#     p.pack(padx= 400)

# pw = ttk.PanedWindow(orient='horizontal')
# sidebar = ttk.PanedWindow(pw, orient="vertical")
# main = tk.Frame(pw, width=400, height=400, background="black")
# sidebar_top = tk.Frame(sidebar, width=200, height=200, background="gray")
# sidebar_bottom = tk.Frame(sidebar, width=200, height=200, background="white")
# pw.pack(fill="both", expand=True)
# pw.add(sidebar)
# pw.add(main)

# Query.insert(0, '  ')
# position = Query.index(tk.INSERT)


def QueryMaker(event):
    global MyTree
    LatestChar= event.char
    FinalQuery = Query.get() + event.char                                           # Lag (old string without latest character)+ Offset (only latest character)

    if LatestChar.isalpha() or LatestChar == '\b' or LatestChar == ' ' or LatestChar.isdigit():             # Check if latest character is ALPHABET or BACKSPACE or SPACE or NUMBER
        if event.char == '\b':                                                      # If BACKSPACE then remove last character
            FinalQuery = FinalQuery[:-2]
        elif event.char == ' ':                                                     # If SPACE then pass (append as usual)
            pass
        else:                                                                       # If ALPHABET then pass (append as usual)
            pass
    else:                                                                           # If any other character then return and do nothing
        return

    print('FINAL STRING:', FinalQuery)              # Final query to search in database
    for i in MyTree.get_children():
        MyTree.delete(i)
    output1 = DBM.SearchDatabase(cur, FinalQuery)   
    # MyTree = FT.display(root, output1, 700)
    MyTree = FT.DisplayEntries(output1, MyTree)

Query.bind('<KeyPress>', QueryMaker)

conn.commit()
conn.close()

root.config(menu=menubar)
root.mainloop()