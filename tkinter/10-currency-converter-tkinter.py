
import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def convert():
    try:
        amount = float(amount_entry.get())
        from_currency = from_combo.get()
        to_currency = to_combo.get()

        response = requests.get(API_URL)
        data = response.json()
        rates = data["rates"]

        if from_currency != "USD":
            amount = amount / rates[from_currency]

        converted = amount * rates[to_currency]
        result_label.config(text=f"{converted:.2f} {to_currency}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {e}")

root = tk.Tk()
root.title("Currency Converter")
root.geometry("300x200")

tk.Label(root, text="Amount:").pack(pady=5)
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="From:").pack()
from_combo = ttk.Combobox(root, values=["USD", "EUR", "GBP", "JPY", "CHF"], state="readonly")
from_combo.set("USD")
from_combo.pack()

tk.Label(root, text="To:").pack()
to_combo = ttk.Combobox(root, values=["USD", "EUR", "GBP", "JPY", "CHF"], state="readonly")
to_combo.set("EUR")
to_combo.pack()

tk.Button(root, text="Convert", command=convert).pack(pady=10)
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
