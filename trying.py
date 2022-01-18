from itertools import chain
import tkinter as tk
from turtle import position
from typing import Final
from Modules import exit as EXIT
import re

# Debugging
def donothing(*args):
    print("Bmsdk kuch bhi mat type kar")
    return

# Creating root window
root = tk.Tk()

# Getting screen size
ScreenWidth = root.winfo_screenwidth()
ScreenHeight = root.winfo_screenheight()

# Adjusting the App window to screen size
AppWindowWidth = str( int( ScreenWidth / 2 ))
AppWindowHeight = str( int( ScreenHeight / 2 ))
AppWindowX = str( int( ScreenWidth / 4 ))           # Distance from left
AppWindowY = str( int( ScreenHeight / 4 ))          # Distance from top
root.geometry(f'{ AppWindowWidth }x{ AppWindowHeight }+{AppWindowX}+{AppWindowY}')

# Renaming the Window
root.title('Searcher')

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

# Query.insert(0, '  ')
# position = Query.index(tk.INSERT)


def QueryMaker(event):
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


Query.bind('<KeyPress>', QueryMaker)


root.config(menu=menubar)
root.mainloop()