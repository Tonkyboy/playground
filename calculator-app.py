# Simple Calculator in Python
# @CodingTogether
import tkinter as tk

root = tk.Tk()
root.title("✨ Calculator")
root.geometry("280x350")
root.configure(bg="#000")

display = tk.StringVar(value="0")
tk.Label(root, textvariable=display, bg="#111", fg="#0ff", font=("Arial", 20, "bold"), 
         height=2).pack(fill="x", padx=10, pady=10)

def click(btn):
    current = display.get()
    if btn == "C": display.set("0")
    elif btn == "=": 
        try: display.set(str(eval(current)))
        except: display.set("Error")
    else: display.set(current + btn if current != "0" else btn)

buttons = [
    ["C", "", "", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", "", ".", "="]
]

for i, row in enumerate(buttons):
    frame = tk.Frame(root, bg="#000")
    frame.pack(fill="x", padx=10, pady=2)
    for j, btn in enumerate(row):
        color = "#f39c12" if btn in "+-*/=" else "#3498db" if btn == "C" else "#34495e"
        btn_widget = tk.Label(frame, text=btn, font=("Arial", 14, "bold"), bg=color, fg="white",
                              width=5, height=2, relief="flat")
        btn_widget.bind("<Button-1>", lambda e, b=btn: click(b))
        btn_widget.pack(side="left", padx=2)

root.mainloop()
