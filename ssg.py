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

# Extensions: "LabeledScale", "OptionMenu",

GridAxisSelect = "Row"
CurrentColumn = 0
CurrentRow = 0
delta = 1

# TODO: turn global variables into parameters, or create a class
# tkinter already has a class 'Grid' that seems to track everything
def GetNextCoord(axis=None, ndelta=None):
    global CurrentColumn
    global CurrentRow
    global delta
    global GridAxisSelect
    if axis is not None: GridAxisSelect = axis
    if ndelta is not None: delta = ndelta
    # the row/column logic might seem 'backwards', but it's not.
    # the selected axis is the one we want to STAY on, so we operate on the other
    match (delta, GridAxisSelect, CurrentColumn, CurrentRow):
        # checking to prevent negative coords negative coords
        case(-1, _, 0, 0): delta = 1
        # in these cases we modify the delta/axis so that the next autoplace will work
        case (-1, "Column", _, 0): GridAxisSelect = "Row"; delta = 1;
        case (-1, "Row", 0, _): GridAxisSelect = "Column"; delta = 1;
        case (_, "Column", _, _): CurrentRow += delta
        case (_, "Row", _, _): CurrentColumn += delta
    #print(CurrentColumn, CurrentRow, GridAxisSelect, delta)
    return CurrentColumn, CurrentRow
# note; the state of delta and GridAxis persist after being modified by GetNextCoord
# that is the desired behavior
# TODO: prevent overlapping elements

# standard skeleton of object-oriented tk-app
class BaseApp(tkinter.Frame):
    def __init__(self, master=None, title=None):
        super().__init__(master)
        self.grid()  # does nothing?
        if title and master:
            self.master.title(title)

    # unfortunately combobox and listbox steal keyboard focus forever
    # the only way to deselect is to hit tab
    def AddDropdown(self, label, choices):
        ncol, nrow = GetNextCoord()
        choices.append("last choice")
        newdropdown = ttk.Combobox(self, values=choices, takefocus=0)
        newdropdown.set(''.join((label,'(', str(ncol),',', str(nrow),')')))
        newdropdown.grid(column=ncol, row=nrow, padx=10, pady=10)

    def AddListbox(self, choices):
        ncol, nrow = GetNextCoord()
        choices.append("last choice")
        newvar = tkinter.StringVar()  # Listbox requires a stringvar
        newvar.set(choices)  # why can't we do this in constructor
        newlistbox = tkinter.Listbox(self, listvariable=newvar, selectmode="extended", exportselection=False)
        newlistbox.grid(column=ncol, row=nrow, padx=10, pady=10)
        # for some reason you can't update the list?

    def CreateButton(self, text="default", command=None, nextcoord=None):
        if not nextcoord:
            nextcoord = GetNextCoord()
        newbutton = tkinter.Button(self, text=text, command=command)
        newbutton.grid(column=nextcoord[0], row=nextcoord[1], padx=10, pady=10)
        newbutton.focus_set()

def VariadicCallback(targetfunction, *args):
    #return lambda: targetfunction(*args)  # causes duplicates in CreateDropdown, for some reason
    return targetfunction(*args)


def Placeholder():
    print("pretending to do something")


if __name__ == "__main__":
    root = tkinter.Tk(sync=False)  # 'sync' option causes X-server commands to be executed synchronously
    window = BaseApp(root, "Epic Title")

    # the call to VariadicCallback must be marked lambda, especially since it's not returning lambda anymore
    newCB = lambda: VariadicCallback(window.AddDropdown, "new dropdown", ["choice 1", "Choice 2"])
    # if it returns lambda instead, then the dropdown menus get 'Last Choice' duplicated
    # it doesn't make a difference whether you '.copy()' the choices anywhere/everywhere
    window.CreateButton("more dropdown", command=newCB, nextcoord=(0,0))
    # this one-liner also works:
    #CreateButton(root, "create dropdown", command=lambda: VariadicCallback(AddDropdown, root, "new dropdown", ["choice 1", "Choice 2"]))
    window.CreateButton("more button", command=lambda: window.CreateButton("new"))
    window.AddDropdown(label="otherbox", choices=["createdby", "AddDropdown()"])

    def ArrowKeyCallback(event):
        keysymtable = { # axis, delta
            'Left':  ("Row", -1),
            'Right': ("Row", 1),
            'Up':    ("Column", -1),
            'Down':  ("Column", 1),
        }
        newcoord = GetNextCoord(*keysymtable[event.keysym])
        window.CreateButton(event.keysym, command=Placeholder, nextcoord=newcoord)
        event.widget.focus_set()  # try to break focus for ComboBox. Still doesn't work for down-arrow
        #window.focus_set()  # also 'almost' works

    # assigning callbacks to each arrow key
    keycodes = [str('<' + ''.join(pair) + '>') for pair in zip(['Key-',]*4, ['Left','Right','Up','Down'])]
    for keycode in keycodes:
        root.bind(keycode, ArrowKeyCallback)

    # cause mouseclicks to set focus
    #root.bind_all("<Button-1>", lambda event: event.widget.focus_set())
    # errors on ComboBox: 'str' object doesn't have attribute 'focus_set'
    root.bind_all("<Button-1>", lambda event: window.focus_set())

    root.mainloop()
