
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

root = tk.Tk()
# root.title('Indexing...')
# root.iconbitmap('angle-circle-up.ico')
lbl = ImageLabel(root)
lbl.pack(padx=30, pady=30)
root.config(background='#0E111F')
root.overrideredirect(True)

w = tk.Label(root, text='L o a d i n g . . .', background='#0E111F', foreground='white', font=('Roboto', 13, 'bold'))
w.pack()

q = tk.Label(root, text='', foreground='#0E111F', background='#0E111F')
q.pack()

lbl.load("GIFF.gif")

root.call('wm', 'attributes', '.', '-topmost', '1')

root.mainloop()



