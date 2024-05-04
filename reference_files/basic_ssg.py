import tkinter as tk
from tkinter import ttk

GridVarSelect = "Row"
CurrentRow = 0
CurrentColumn = 0

def NextCoord():
    if GridVarSelect == "Row":
        global CurrentRow
        CurrentRow += 1
    else:
        global CurrentColumn
        CurrentColumn += 1
    return CurrentRow, CurrentColumn


# standard skeleton of object-oriented tk-app
class BaseApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.master.title("app title")

    def AddDropdown(self, master=None):
        self.stats_var = tk.StringVar()
        self.stats_var.set("Select Stats Type")
        self.stats_dropdown = ttk.Combobox(master, textvariable=self.stats_var,
                                           values=["Rebounding", "Passing"])
        self.stats_dropdown.grid(row=0, column=0, padx=10, pady=10)


def FetchStats():
    print("pretending to fetch something")


def CreateButton(parent, text="default", command=FetchStats):
    newbutton = tk.Button(parent, text=text, command=command)
    row, column = NextCoord()
    newbutton.grid(row=row, column=column, padx=10, pady=10)
    return newbutton


if __name__ == "__main__":
    root = tk.Tk()
    window = BaseApp(root)
    window.AddDropdown(root)
    newb = CreateButton(root, "newbutton1", FetchStats)
    def callb(Event):
        CreateButton(root, "newbutton69", FetchStats)
    root.bind("<Key-Return>", callb)


# Holy shit I'm epic

