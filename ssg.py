import tkinter
from tkinter import ttk

# to override the basic Tk widgets, use the following imports:
# from tkinter import *
# from tkinter.ttk import *
# which will override:
# Button, Checkbutton, Entry, Frame, Label, LabelFrame,
# Menubutton, PanedWindow, Radiobutton, Scale and Scrollbar,
# and maybe Spinbox??
# The new entries unique to ttk are:
# Combobox, Notebook, Progressbar, Separator, Sizegrip and Treeview


GridVarSelect = "Row"
CurrentRow = 0
CurrentColumn = 0
delta = 1

# TODO: swap the 'axis' logic
def NextCoord():
    global CurrentRow
    global CurrentColumn
    if GridVarSelect == "Row":
        CurrentRow += delta
    else:
        CurrentColumn += delta
    return CurrentRow, CurrentColumn
    # note; the state of delta and GridVarSelect persist
    # after being modified by CustomNextCoord, and are not reset here
    # that is the desired behavior.


# standard skeleton of object-oriented tk-app
class BaseApp(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.master.title("Epic Title")


def AddDropdown(master, label, choices):
    nrow, ncol = NextCoord()
    choices.append("last choice")
    newdropdown = ttk.Combobox(master, textvariable=tkinter.StringVar(), values=choices)
    newdropdown.set(''.join((label,'(', str(nrow),',', str(ncol),')')))
    newdropdown.grid(row=nrow, column=ncol, padx=10, pady=10)
    return newdropdown

def VariadicCallback(targetfunction, *args):
    print(targetfunction)
    print(args)
    #return lambda: targetfunction(*args)  # causes duplicates in CreateDropdown, for some reason
    return targetfunction(*args)


def FetchStats():
    print("pretending to fetch something")


def CreateButton(parent, text="default", command=FetchStats, nextcoord=None):
    if nextcoord:
        row, column = nextcoord
    else:
        row, column = NextCoord()
    newbutton = tkinter.Button(parent, text=text, command=command)
    newbutton.grid(row=row, column=column, padx=10, pady=10)
    return newbutton


if __name__ == "__main__":
    # root = tkinter.Tk(sync=True)  # 'sync' option causes X-server commands to be executed synchronously
    root = tkinter.Tk()
    window = BaseApp(root)

    AddDropdown(root, label="Select Stats Type", choices=["Rebounding", "Passing"])

    newsvar = tkinter.StringVar()
    newsvar.set("static string")
    ttk.Combobox(root, textvariable=newsvar, values=["qwerty", "asdf"]).grid(row=1, column=1, padx=10, pady=10)
    # you must create a seperate variable to hold the initial string; otherwise it shows up blank
    # or you could call '.set' on the combobox itself, but then it must be named

    # the call to VariadicCallback must be marked lambda, especially since it's not returning lambda anymore
    newCB = lambda: VariadicCallback(AddDropdown, root, "new dropdown", ["choice 1", "Choice 2"])
    # if it returns lambda instead, then the dropdown menus get 'Last Choice' duplicated
    # it doesn't make a difference whether you '.copy()' the choices anywhere/everywhere
    CreateButton(root, "create dropdown", command=newCB)
    # this one-liner also works:
    #CreateButton(root, "create dropdown", command=lambda: VariadicCallback(AddDropdown, root, "new dropdown", ["choice 1", "Choice 2"]))


    # TODO: turn global variables into parameters
    def CustomNextCoord(negative, axis):
        global delta
        global GridVarSelect
        # don't allow negative coords
        match (negative, axis, CurrentRow, CurrentColumn):
            case (True, "Row", 0, _): return (CurrentRow, CurrentColumn)
            case (True, "Column", _, 0): return (CurrentRow, CurrentColumn)
        if negative:
            delta = -1
        else:
            delta = 1
        GridVarSelect = axis
        return NextCoord()


    def ArrowKeyCallback(event):
        #print(event)
        # isNegative, axis
        keysymtable = {
            'Right': (False, "Column"),
            'Left':  (True, "Column"),
            'Up':    (True, "Row"),
            'Down':  (False, "Row"),
        }
        newcoord = CustomNextCoord(*keysymtable[event.keysym])
        CreateButton(root, event.keysym, command=FetchStats, nextcoord=newcoord)

    # assigning callbacks to each arrow key
    keycodes = [str('<' + ''.join(pair) + '>') for pair in zip(['Key-',]*4, ['Left','Right','Up','Down'])]
    for keycode in keycodes:
        root.bind(keycode, ArrowKeyCallback)

    root.mainloop()

# Holy shit I'm epic

