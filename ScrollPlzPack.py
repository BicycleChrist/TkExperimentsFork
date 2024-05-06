import tkinter as tk
from tkinter import ttk

def scroll_event(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=1200, height=700)

root = tk.Tk()
root.title("Scrollable Tkinter Window")

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", scroll_event)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

for i in range(30):
    button = tk.Button(frame, text=f"Button {i+1}")
    button.pack(side=tk.TOP, fill=tk.X)

root.mainloop()

