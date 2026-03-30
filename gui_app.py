import tkinter as tk
from tkinter import messagebox
import csv
import random
import os

CSV_FILE = 'data.csv'

def get_next_no_and_barcodes():
    max_no = 0
    barcodes = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    no = int(row['no'])
                    if no > max_no:
                        max_no = no
                except ValueError:
                    pass
                if 'barcode' in row:
                    barcodes.add(row['barcode'])
    return max_no + 1, barcodes

def generate_unique_barcode(existing_barcodes):
    while True:
        # Generate a 10-digit barcode with leading zeros if needed
        barcode = f"{random.randint(0, 9999999999):010d}"
        if barcode not in existing_barcodes:
            return barcode

def submit_data():
    name = entry_name.get()
    description = entry_desc.get()
    weight = entry_weight.get()
    width = entry_width.get()
    lenght = entry_lenght.get()
    height = entry_height.get()
    price = entry_price.get()
    quantity = entry_quantity.get()

    if not all([name, description, weight, width, lenght, height, price, quantity]):
        messagebox.showerror("Error", "All fields are required")
        return

    next_no, existing_barcodes = get_next_no_and_barcodes()
    barcode = generate_unique_barcode(existing_barcodes)

    new_row = [next_no, barcode, name, description, weight, width, lenght, height, price, quantity]

    # Append to CSV
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['no', 'barcode', 'name', 'description', 'weight', 'width', 'lenght', 'height', 'price', 'quantity'])
        writer.writerow(new_row)

    messagebox.showinfo("Success", f"Data appended successfully!\nNo: {next_no}\nBarcode: {barcode}")

    # Clear entries
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    entry_width.delete(0, tk.END)
    entry_lenght.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)

root = tk.Tk()
root.title("Add Storage Item")

# Labels and Entries
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Description").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Weight").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Width").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Lenght").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Height").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Price").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="Quantity").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

entry_name = tk.Entry(root, width=50)
entry_name.grid(row=0, column=1, padx=10, pady=5)
entry_desc = tk.Entry(root, width=50)
entry_desc.grid(row=1, column=1, padx=10, pady=5)
entry_weight = tk.Entry(root, width=50)
entry_weight.grid(row=2, column=1, padx=10, pady=5)
entry_width = tk.Entry(root, width=50)
entry_width.grid(row=3, column=1, padx=10, pady=5)
entry_lenght = tk.Entry(root, width=50)
entry_lenght.grid(row=4, column=1, padx=10, pady=5)
entry_height = tk.Entry(root, width=50)
entry_height.grid(row=5, column=1, padx=10, pady=5)
entry_price = tk.Entry(root, width=50)
entry_price.grid(row=6, column=1, padx=10, pady=5)
entry_quantity = tk.Entry(root, width=50)
entry_quantity.grid(row=7, column=1, padx=10, pady=5)

submit_btn = tk.Button(root, text="Submit", command=submit_data)
submit_btn.grid(row=8, column=0, columnspan=2, pady=10)

if __name__ == '__main__':
    root.mainloop()
