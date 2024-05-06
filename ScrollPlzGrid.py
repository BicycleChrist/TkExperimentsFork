import tkinter as tk
from tkinter import ttk

def scroll_event(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=200)

root = tk.Tk()
root.title("Scrollable Tkinter Window")

canvas = tk.Canvas(root)
canvas.grid(row=0, column=0, sticky="nsew")

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", scroll_event)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

for i in range(30):
    button = tk.Button(frame, text=f"Button {i+1}")
    button.grid(row=i, column=0, sticky="ew")

root.mainloop()
