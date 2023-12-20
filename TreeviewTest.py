#from tkinter import *
#from tkinter.ttk import *
# which will override:
# Button, Checkbutton, Entry, Frame, Label, LabelFrame,
# Menubutton, PanedWindow, Radiobutton, Scale and Scrollbar,
# and maybe Spinbox??
# The new entries unique to ttk are:
# Combobox, Notebook, Progressbar, Separator, Sizegrip and Treeview

import tkinter
from tkinter import ttk

import random

## main-stuff
root = tkinter.Tk()
frm = ttk.Frame(root)
frm.pack()

TREE = ttk.Treeview(root)
for i in range(10):
    newid = TREE.insert("", index="end", text=f"something_{i}", values=list(random.randint(1, 10) for _ in range(3)))
    for x in range(random.randint(1, 4)):
        TREE.insert(newid, index="end", text=f"child_{newid}_{x}", values=[random.randint(1, 10) for _ in range(3)])
TREE.pack()

for i in range(10):
    ttk.Menubutton(text=f"button#{i}").pack()

root.mainloop()
