import tkinter
#from tkinter import ttk


class BaseWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()


def Main():
    toplevel = BaseWindow()
    toplevel.mainloop()


if __name__ == "__main__":
    Main()



