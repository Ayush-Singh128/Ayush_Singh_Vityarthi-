import tkinter as tk
from tkinter import ttk
import json
class FarmTracker:
    def __init__(self, window):
        self.window = window
        self.window.title("Farm Items")
        self.window.geometry("700x500")
        self.data_file = "farm_data.json"
        self.items = []
        self.load_data()
        self.setup_gui()
        self.show_items()
    def setup_gui(self):
        # Input area
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Item:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)
        tk.Label(input_frame, text="Qty:").grid(row=0, column=2, padx=5)
        self.qty_entry = tk.Entry(input_frame, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5)
        tk.Label(input_frame, text="Type:").grid(row=0, column=4, padx=5)
        self.type_var = tk.StringVar(value="Tools")
        type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, 
                                 values=["Tools", "Seeds", "Fertilizers"], width=12)
        type_combo.grid(row=0, column=5, padx=5)
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add", command=self.add_item, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Remove", command=self.remove_item, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_all, width=10).pack(side=tk.LEFT, padx=5)
        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search)
        list_frame = tk.Frame(self.window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Qty", "Type"), show="headings", height=15)
        self.tree.heading("ID", text="#")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Type", text="Type")
        self.tree.column("ID", width=40)
        self.tree.column("Name", width=200)
        self.tree.column("Qty", width=60)
        self.tree.column("Type", width=100)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind('<Double-1>', self.edit_item)
    def add_item(self):
        name = self.name_entry.get().strip()
        qty = self.qty_entry.get().strip()
        if not name or not qty:
            tk.messagebox.showwarning("Error", "Please fill all fields")
            return
        try:
            int(qty)
        except:
            tk.messagebox.showwarning("Error", "Quantity must be a number")
            return
        new_id = len(self.items) + 1
        new_item = {
            "id": new_id,
            "name": name,
            "qty": qty,
            "type": self.type_var.get()
        }
        self.items.append(new_item)
        self.save_data()
        self.show_items()
        self.clear_entries()
    def remove_item(self):
        selected = self.tree.selection()
        if not selected:
            tk.messagebox.showwarning("Error", "Select an item first")
            return
        item_id = self.tree.item(selected[0])['values'][0]
        self.items = [item for item in self.items if item['id'] != item_id]
        for i, item in enumerate(self.items, 1):
            item['id'] = i   
        self.save_data()
        self.show_items()
    def edit_item(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.qty_entry.delete(0, tk.END)
            self.qty_entry.insert(0, values[2])
            self.type_var.set(values[3])
    def search(self, event):
        term = self.search_entry.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.items:
            if (term in item['name'].lower() or 
                term in item['type'].lower() or
                term in str(item['qty'])):
                self.tree.insert("", "end", values=(
                    item['id'], item['name'], item['qty'], item['type']
                ))
    def clear_all(self):
        if not self.items:
            return  
        if tk.messagebox.askyesno("Confirm", "Clear all items?"):
            self.items = []
            self.save_data()
            self.show_items()
    def show_items(self):
        for item in self.tree.get_children():
            self.tree.delete(item)    
        for item in self.items:
            self.tree.insert("", "end", values=(
                item['id'], item['name'], item['qty'], item['type']
            ))
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                self.items = json.load(f)
        except:
            self.items = []
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.items, f)
if __name__ == "__main__":
    root = tk.Tk()
    app = FarmTracker(root)
    root.mainloop()