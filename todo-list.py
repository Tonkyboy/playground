
# Cod1ngTogether
import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.title("To-Do")
root.geometry("400x300")

tasks = []

def add_task():
    root.update()  # Force update before dialog
    text = simpledialog.askstring("Add", "Task:", parent=root)
    root.focus_force()  # Return focus to main window
    if text and text.strip():
        frame = tk.Frame(root)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        var = tk.BooleanVar()
        tk.Checkbutton(frame, variable=var).pack(side=tk.LEFT)
        tk.Label(frame, text=text.strip()).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="−", command=lambda: 
                  [frame.destroy(), tasks.remove((frame, var))], 
                 fg="red").pack(side=tk.RIGHT)
        
        tasks.append((frame, var))

def remove_selected():
    for frame, var in tasks[:]:
        if var.get():
            frame.destroy()
            tasks.remove((frame, var))

tk.Button(root, text="+", command=add_task, 
          font=("Arial", 14), fg="green").pack(pady=5)
tk.Button(root, text="Remove Selected", 
          command=remove_selected, fg="red").pack(pady=5)

root.mainloop()
