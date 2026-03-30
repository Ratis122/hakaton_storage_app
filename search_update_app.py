import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

CSV_FILE = 'data.csv'

def load_data():
    data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    return data

def save_data(data, fieldnames):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

class SearchUpdateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search and Update Quantity")
        self.root.geometry("600x450")
        self.data = []
        self.fieldnames = ['no', 'barcode', 'name', 'description', 'weight', 'width', 'lenght', 'height', 'price', 'quantity']
        
        # Search Frame
        search_frame = tk.Frame(root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(search_frame, text="Search by:").pack(side=tk.LEFT, padx=5)
        self.search_by_var = tk.StringVar(value="name")
        search_by_combo = ttk.Combobox(search_frame, textvariable=self.search_by_var, values=["name", "barcode", "no"], state="readonly", width=10)
        search_by_combo.pack(side=tk.LEFT, padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame, text="Search", command=self.search).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.show_all).pack(side=tk.LEFT, padx=5)
        
        # Treeview Frame
        tree_frame = tk.Frame(root)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        columns = ("no", "barcode", "name", "quantity", "price")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("no", text="No")
        self.tree.heading("barcode", text="Barcode")
        self.tree.heading("name", text="Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price")
        
        self.tree.column("no", width=50)
        self.tree.column("barcode", width=120)
        self.tree.column("name", width=250)
        self.tree.column("quantity", width=80)
        self.tree.column("price", width=80)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Update Frame
        update_frame = tk.Frame(root)
        update_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.selected_label = tk.Label(update_frame, text="Selected: None")
        self.selected_label.pack(side=tk.TOP, pady=5)
        
        tk.Label(update_frame, text="Amount:").pack(side=tk.LEFT, padx=5)
        self.amount_entry = tk.Entry(update_frame, width=10)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        self.action_var = tk.StringVar(value="add")
        tk.Radiobutton(update_frame, text="Add", variable=self.action_var, value="add").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(update_frame, text="Remove", variable=self.action_var, value="remove").pack(side=tk.LEFT, padx=5)
        
        tk.Button(update_frame, text="Apply", command=self.apply_update).pack(side=tk.LEFT, padx=10)
        
        self.selected_no = None
        self.refresh_data()

    def refresh_data(self):
        self.data = load_data()
        if self.data and 'no' in self.data[0]:
            self.fieldnames = list(self.data[0].keys())
        self.show_all()

    def show_all(self):
        self.update_treeview(self.data)
        self.search_entry.delete(0, tk.END)

    def search(self):
        search_by = self.search_by_var.get()
        query = self.search_entry.get().strip().lower()
        
        if not query:
            self.show_all()
            return
            
        filtered_data = []
        for row in self.data:
            val = str(row.get(search_by, "")).lower()
            if query in val:
                filtered_data.append(row)
                
        self.update_treeview(filtered_data)

    def update_treeview(self, data_to_show):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in data_to_show:
            self.tree.insert("", tk.END, values=(row.get("no",""), row.get("barcode",""), row.get("name",""), row.get("quantity",""), row.get("price","")))

    def on_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            self.selected_no = None
            self.selected_label.config(text="Selected: None")
            return
            
        item = self.tree.item(selected_items[0])
        values = item['values']
        self.selected_no = str(values[0])
        name = values[2]
        qty = values[3]
        self.selected_label.config(text=f"Selected: [{self.selected_no}] {name} (Current Qty: {qty})")

    def apply_update(self):
        if not self.selected_no:
            messagebox.showwarning("Warning", "Please select an item first.")
            return
            
        amount_str = self.amount_entry.get().strip()
        if not amount_str:
            messagebox.showwarning("Warning", "Please enter an amount.")
            return
            
        try:
            amount = int(amount_str)
            if amount < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Amount must be a positive integer.")
            return

        action = self.action_var.get()
        
        # Find item and update
        item_found = False
        new_qty = 0
        for row in self.data:
            if str(row.get("no")) == self.selected_no:
                item_found = True
                try:
                    current_qty = int(row.get("quantity", 0))
                except ValueError:
                    current_qty = 0
                
                if action == "add":
                    new_qty = current_qty + amount
                else: # remove
                    new_qty = current_qty - amount
                    if new_qty < 0:
                        messagebox.showerror("Error", "Resulting quantity cannot be negative.")
                        return
                
                row["quantity"] = str(new_qty)
                break
                
        if not item_found:
            messagebox.showerror("Error", "Item not found in data.")
            return
            
        # Save to csv
        save_data(self.data, self.fieldnames)
        messagebox.showinfo("Success", f"Quantity updated successfully to {new_qty}.")
        
        # Clear amount and refresh
        self.amount_entry.delete(0, tk.END)
        self.refresh_data()
        self.search() # re-apply search filter if any

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchUpdateApp(root)
    root.mainloop()
