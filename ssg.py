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

def NextCoord():
    global CurrentRow
    global CurrentColumn
    if GridVarSelect == "Row":
        CurrentRow += delta
    else:
        CurrentColumn += delta
    return CurrentRow, CurrentColumn


# standard skeleton of object-oriented tk-app
class BaseApp(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.master.title("app title")

# the Dropdown's label is the key, maps to callback returning it's value
DropdownGetSelection = {

}

def AddDropdown(master, label, choices):
    nrow, ncol = NextCoord()
    label = label + str(nrow) + str(ncol)
    print(label)
    newsvar = tkinter.StringVar()
    newsvar.set("static string")
    choices.append(label)
    newdropdown = ttk.Combobox(master, textvariable=newsvar, values=choices)
    newdropdown.grid(row=nrow, column=ncol, padx=10, pady=10)
    #DropdownCallbackMap.update({label: newcallback})
    #return newdropdown, newsvar


def VariadicCallback(targetfunction, **kwargs):
    print(targetfunction)
    print(kwargs)
    return lambda: targetfunction(**kwargs)

# If you want to "AddDropdown" through a button, it can't take any parameters
#def CreateCallback(targetfunction, master, label, choices):
#    button["command"] lambda : AddDropdown(master, label, choices)


def FetchStats():
    print("pretending to fetch something")


def CreateButton(parent, text="default", command=FetchStats, nextcoordmethod=NextCoord):
    newbutton = tkinter.Button(parent, text=text, command=command)
    row, column = nextcoordmethod()
    newbutton.grid(row=row, column=column, padx=10, pady=10)
    return newbutton


if __name__ == "__main__":
    root = tkinter.Tk(sync=True)
    # the 'sync' option causes X-server commands to be executed synchronously;
    # so that errors are reported immediately
    # can be important for debugging
    window = BaseApp(root)
    newsvar = tkinter.StringVar()
    newsvar.set("static string")
    newdropdown = ttk.Combobox(root, textvariable=newsvar, values=["Rebounding", "Passing"])
    newdropdown.grid(row=1, column=1, padx=10, pady=10)
    AddDropdown(root, label="Select Stats Type", choices=["Rebounding", "Passing"])
    newcallback = VariadicCallback(AddDropdown, master=root, label="new dropdown", choices=["choice 1", "Choice 2"])
    CreateButton(root, "create dropdown", newcallback)

    newb = CreateButton(root, "newbutton1", FetchStats)
    def callb(Event):
        CreateButton(root, "newbutton69", FetchStats)
    def CustomNextCoord(negative, axis):
        print(f"customnextcoord: {negative}, {axis}")
        global delta
        global GridVarSelect
        oldstate = (delta, GridVarSelect)
        if negative:
            delta = -1
        else:
            delta = 1
        GridVarSelect = axis
        returnvalue = NextCoord()
        delta, GridVarSelect = oldstate
        return returnvalue

    callbackstorage = []

    def specialnewbutton(customfunction, **kwargs):
        print(f"specialnewbutton with: {kwargs}")
        newbuttoncallback = lambda: customfunction(**kwargs)
        callbackstorage.append(newbuttoncallback)
        otherlambda = lambda event: CreateButton(root, "arrowbuttons", FetchStats, newbuttoncallback)
        callbackstorage.append(otherlambda)
        return lambda event: CreateButton(root, "arrowbuttons", FetchStats, newbuttoncallback)
        #newcallback = lambda: CreateButton(root, "arrowbuttons", FetchStats, customfunction)

    def rightcallback(event):
        customnextcoord = lambda: CustomNextCoord(False, "Column")
        return CreateButton(root, "rightkey", command=FetchStats, nextcoordmethod=customnextcoord)

    root.bind("<Key-Return>", callb)
    #root.bind("<Key-Right>", specialnewbutton(CustomNextCoord, negative=False, axis="Row"))
    #root.bind("<Key-Right>", lambda: CustomNextCoord(True, "Row"))
    root.bind("<Key-Right>", rightcallback)
    root.bind("<Shift-A>", callb)
    root.mainloop()

# Holy shit I'm epic

