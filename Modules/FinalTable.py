import subprocess
from tkinter import ttk
import tkinter as tk


def display(root, records, dimensions):
    style = ttk.Style()
    style.theme_use('classic')

    style.configure('Treeview', background='#1A374D', foreground='#71DFE7', font=('Arial', 8, 'bold'))
    style.configure('Treeview.Heading',background='#072227', foreground='#AEFEFF')

    style.map('Treeview', background=[('selected', '#17D7A0')])

    MyTree = ttk.Treeview(root)

    MyTree['columns'] = ('filename', 'size', 'path')
    
    MyTree.column('#0', width=0, stretch=tk.NO)
    MyTree.column('filename', anchor=tk.W, width= int(2 * dimensions / 7))
    MyTree.column('size', anchor=tk.W, width= int(2 * dimensions / 7))
    MyTree.column('path', anchor=tk.W, width= int(3 * dimensions / 7))
    
    MyTree.heading('#0', text='', anchor=tk.W)
    MyTree.heading('filename', text='File names', anchor=tk.W)
    MyTree.heading('size', text='Size', anchor=tk.W)
    MyTree.heading('path', text='Path', anchor=tk.W)
    counter = 0
    for record in records:
        MyTree.insert(parent='', index='end', iid=counter, text='', values=(record[0], record[1], record[2]))
        counter = counter + 1
    def Selected_Entry(event):
        ItemID = MyTree.selection()[0]
        ItemValue = MyTree.item(ItemID)
        crete = 'explorer /select, ' + ItemValue['values'][2]
        subprocess.Popen(crete)
    
    MyTree.bind('<Double-1>', Selected_Entry)
    MyTree.pack(padx=5, fill=tk.BOTH, expand=1)

    return MyTree

def DisplayEntries(records, MyTree):
    counter = 0
    for record in records:
        MyTree.insert(parent='', index='end', iid=counter, text='', values=(record[0], record[1], record[2]))
        counter = counter + 1
    def Selected_Entry(event):
        ItemID = MyTree.selection()[0]
        ItemValue = MyTree.item(ItemID)
        crete = 'explorer /select, ' + ItemValue['values'][2]
        subprocess.Popen(crete)
    MyTree.bind('<Double-1>', Selected_Entry)
    MyTree.pack(padx=5, fill=tk.BOTH, expand=1)

    return MyTree


# root = tk.Tk()
# records = [['Noice', '20kb', 'E:\TorrentSearcherBot'], ['okay', '200kb', 'E:\PROGRAMS\\bondeabhijeet.github.io'], ['Cool', '210kb', 'F:\sdcard'], ['Argh', '380kb', 'G:\Aeroplane'], ['Sed', '83kb', 'C:\Program Files (x86)\Google'], ['Noice', '20kb', 'E:\TorrentSearcherBot'], ['okay', '200kb', 'E:\PROGRAMS\\bondeabhijeet.github.io'], ['Cool', '210kb', 'F:\sdcard'], ['Argh', '380kb', 'G:\Aeroplane'], ['Sed', '83kb', 'C:\Program Files (x86)\Google'], ['Noice', '20kb', 'E:\TorrentSearcherBot'], ['okay', '200kb', 'E:\PROGRAMS\\bondeabhijeet.github.io'], ['Cool', '210kb', 'F:\sdcard'], ['Argh', '380kb', 'G:\Aeroplane'], ['Sed', '83kb', 'C:\Program Files (x86)\Google']]

# display(root, records, 700)

# root.mainloop()