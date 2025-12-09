
import tkinter as tk
from tkinter import filedialog
import os, shutil

root = tk.Tk()
root.title("📂 File Organizer")
root.geometry("400x250")
root.configure(bg="#000")

status_var = tk.StringVar(value="Ready to Organize")
tk.Label(root, textvariable=status_var, bg="#111", fg="#0ff", font=("Arial", 16, "bold"),
         height=2).pack(fill="x", padx=10, pady=20)

TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Docs": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Audio": [".mp3", ".wav"]
}

def organize_files(event):
    folder = filedialog.askdirectory()
    if not folder: return
    
    count = 0
    for file in os.listdir(folder):
        if "." not in file: continue
        ext = os.path.splitext(file)[1].lower()
        
        for category, extensions in TYPES.items():
            if ext in extensions:
                target_dir = os.path.join(folder, category)
                if not os.path.exists(target_dir): os.makedirs(target_dir)
                shutil.move(os.path.join(folder, file), os.path.join(target_dir, file))
                count += 1
                break
    status_var.set(f"Moved {count} Files! ✨")

frame = tk.Frame(root, bg="#000")
frame.pack(pady=20)

btn_text = "SELECT FOLDER"
btn_widget = tk.Label(frame, text=btn_text, font=("Arial", 14, "bold"), bg="#f39c12", fg="white",
                      width=20, height=2, relief="flat")
btn_widget.bind("<Button-1>", organize_files)
btn_widget.pack()

tk.Label(root, text="Sorts: Images, Docs, Video, Audio", bg="#000", fg="#555", 
         font=("Arial", 10)).pack(side="bottom", pady=10)

root.mainloop()