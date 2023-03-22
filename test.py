import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv

class InventoryManagementSystem:
    def __init__(self):
        self.host = input("Enter the host: ")
        self.user = input("Enter the user: ")
        self.password = input("Enter the password: ")
        self.database = input("Enter the database: ")
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            auth_plugin="mysql_native_password"
        )
        self.cursor = self.db.cursor()

        self.root = Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")

        self.columns = ("id", "name", "description", "price", "quantity", "category_id")
        self.products_tree = ttk.Treeview(self.root, columns=self.columns, show="headings")
        self.products_tree.place(x=50, y=50, width=700, height=400)
        
        self.scrollbary = ttk.Scrollbar(self.root, orient="vertical", command=self.products_tree.yview)
        self.scrollbary.place(x=750, y=50, height=400)
        self.products_tree.configure(yscrollcommand=self.scrollbary.set)
        self.scrollbarz = ttk.Scrollbar(self.root, orient="horizontal", command=self.products_tree.xview)
        self.scrollbarz.place(x=50, y=450, width=700)
        self.products_tree.configure(xscrollcommand=self.scrollbarz.set)
        

        self.products_tree["columns"] = self.columns
        self.products_tree.column("id", width=50, anchor="center")
        self.products_tree.column("name", width=100, anchor="center")
        self.products_tree.column("description", width=100, anchor="center")
        self.products_tree.column("price", width=100, anchor="center")
        self.products_tree.column("quantity", width=100, anchor="center")
        self.products_tree.column("category_id", width=100, anchor="center")

        self.products_tree.heading("id", text="ID")
        self.products_tree.heading("name", text="Name")
        self.products_tree.heading("description", text="Description")
        self.products_tree.heading("price", text="Price")
        self.products_tree.heading("quantity", text="Quantity")
        self.products_tree.heading("category_id", text="Category ID")

        self.cursor.execute("SELECT * FROM product")
        self.products = self.cursor.fetchall()
        for product in self.products:
            id = product[0]
            name = product[1]
            description = product[2]
            price = product[3]
            quantity = product[4]
            category_name = product[5]
            sql = "SELECT name FROM category WHERE id = %s"
            val = (category_name,)
            self.cursor.execute(sql, val)
            category_name = self.cursor.fetchone()[0]
            self.products_tree.insert(parent="", index="end", values=(id, name, description, price, quantity, category_name))

        self.cursor.execute("SELECT id FROM category")
        self.categories = self.cursor.fetchall()
        self.category_combobox = ttk.Combobox(self.root, values=self.categories, state="readonly")
        self.category_combobox.bind("<<ComboboxSelected>>", self.update_selected_category_id)

        self.category_combobox.place(x=280, y=570)
        self.selected_category_id = self.category_combobox.get()
        
        self.filter_button = Button(self.root, text="Filter", command=self.filter_products_category)
        self.filter_button.place(x=450, y=570)

        self.show_all_button = Button(self.root, text="Show All Products", command=self.show_all_products)
        self.show_all_button.place(x=650, y=570)

        self.export_csv_button = Button(self.root, text="Export to CSV", command=self.export_to_csv)
        self.export_csv_button.place(x=550, y=570)

        self.add_product_button = Button(self.root, text="Add Product", command=self.add_product_window)
        self.add_product_button.place(x=50, y=20)

        self.edit_product_button = Button(self.root, text="Edit Product", command=self.edit_product_window)
        self.edit_product_button.place(x=150, y=20)

        self.delete_product_button = Button(self.root, text="Delete Product", command=self.delete_product)
        self.delete_product_button.place(x=250, y=20)

        self.root.mainloop()
    def get_category_combobox_value(self):
        self.selected_category_id = self.category_combobox.get()
        return self.selected_category_id
   
    def filter_products_category(self):
        # Clear the Treeview
        self.products_tree.delete(*self.products_tree.get_children())

    # Get the selected category
        selected_category = self.get_category_combobox_value()
        print(selected_category)
    # Fetch all the products from the database
        self.cursor.execute("SELECT * FROM product")
        products = self.cursor.fetchall()

        # Insert the products into the Treeview
        for product in products:
            id = product[0]
            name = product[1]
            description = product[2]
            price = product[3]
            quantity = product[4]
            category_id = product[5]
            print(category_id)
            if category_id == selected_category:
                sql = "SELECT name FROM category WHERE id = %s"
                val = (category_id,)
                self.cursor.execute(sql, val)
                category_name = self.cursor.fetchone()[0]
                self.products_tree.insert(parent="", index="end", values=(id, name, description, price, quantity, category_name))
                
    def update_selected_category_id(self, event):
        self.selected_category_id = self.category_combobox.get()

          
    def show_all_products(self):
        self.cursor.execute("SELECT * FROM product")
        self.products_tree.delete(*self.products_tree.get_children())
        for product in self.cursor.fetchall():
            id = product[0]
            name = product[1]
            description = product[2]
            price = product[3]
            quantity = product[4]
            category_name = product[5]
            sql = "SELECT name FROM category WHERE id = %s"
            val = (category_name,)
            self.cursor.execute(sql, val)
            category_name = self.cursor.fetchone()[0]
            self.products_tree.insert(parent="", index="end", values=(id, name, description, price, quantity, category_name))
    def edit_product_window(self):
        
        self.edit_window = Toplevel(self.root)
        self.edit_window.title("Edit Product")
        self.edit_window.geometry("300x300")

        name_label = Label(self.edit_window, text="Name: ")
        name_label.place(x=20, y=20)
        self.name_entry = Entry(self.edit_window)
        self.name_entry.place(x=100, y=20)

        description_label = Label(self.edit_window, text="Description: ")
        description_label.place(x=20, y=60)
        self.description_entry = Entry(self.edit_window)
        self.description_entry.place(x=100, y=60)

        price_label = Label(self.edit_window, text="Price: ")
        price_label.place(x=20, y=100)
        self.price_entry = Entry(self.edit_window)
        self.price_entry.place(x=100, y=100)

        quantity_label = Label(self.edit_window, text="Quantity: ")
        quantity_label.place(x=20, y=140)
        self.quantity_entry = Entry(self.edit_window)
        self.quantity_entry.place(x=100, y=140)

        category_label = Label(self.edit_window, text="Category: ")
        category_label.place(x=20, y=180)
        self.cursor.execute("SELECT id FROM category")
        self.categories = self.cursor.fetchall()
        self.category_combobox = ttk.Combobox(self.edit_window, values=self.categories, state="readonly")
        self.category_combobox.place(x=100, y=180)

        save_button = Button(self.edit_window, text="Save", command=self.edit_product)
        save_button.place(x=100, y=220)
    
    def add_product_window(self):
        self.add_window = Toplevel(self.root)
        self.add_window.title("Add Product")
        self.add_window.geometry("300x300")

        name_label = Label(self.add_window, text="Name:")
        name_label.place(x=20, y=20)
        self.name_entry = Entry(self.add_window)
        self.name_entry.place(x=100, y=20)

        description_label = Label(self.add_window, text="Description:")
        description_label.place(x=20, y=60)
        self.description_entry = Entry(self.add_window)
        self.description_entry.place(x=100, y=60)

        price_label = Label(self.add_window, text="Price:")
        price_label.place(x=20, y=100)
        self.price_entry = Entry(self.add_window)
        self.price_entry.place(x=100, y=100)

        quantity_label = Label(self.add_window, text="Quantity:")
        quantity_label.place(x=20, y=140)
        self.quantity_entry = Entry(self.add_window)
        self.quantity_entry.place(x=100, y=140)

        category_label = Label(self.add_window, text="Category:")
        category_label.place(x=20, y=180)
        self.category_combobox = ttk.Combobox(self.add_window, values=self.categories, state="readonly")
        self.category_combobox.place(x=100, y=180)
        self.add_button=Button(self.add_window,text="Add Product",command=self.add_product)
        self.add_button.place(x=100,y=220)

    def filter_products_category(self):
        
        self.cursor.execute("SELECT * FROM product WHERE category_id = %s", (self.selected_category_id,))
        filtered_products = self.cursor.fetchall()
        self.products_tree.delete(*self.products_tree.get_children())
        for product in filtered_products:
            id = product[0]
            name = product[1]
            description = product[2]
            price = product[3]
            quantity = product[4]
            category_name = product[5]
            sql = "SELECT name FROM category WHERE id = %s"
            val = (category_name,)
            self.cursor.execute(sql, val)
            category_name = self.cursor.fetchone()[0]
            self.products_tree.insert(parent="", index="end", values=(id, name, description, price, quantity, category_name))

    def show_all_products(self):
        self.cursor.execute("SELECT * FROM product")
        self.products = self.cursor.fetchall()
        self.products_tree.delete(*self.products_tree.get_children())
        for product in self.products:
            id = product[0]
            name = product[1]
            description = product[2]
            price = product[3]
            quantity = product[4]
            category_name = product[5]
            sql = "SELECT name FROM category WHERE id = %s"
            val = (category_name,)
            self.cursor.execute(sql, val)
            category_name = self.cursor.fetchone()[0]
            self.products_tree.insert(parent="", index="end", values=(id, name, description, price, quantity, category_name))

    def delete_product(self):
        selected_product_id = self.products_tree.item(self.products_tree.selection())["values"][0]
        self.cursor.execute("DELETE FROM product WHERE id = %s", (selected_product_id,))
        self.db.commit()
        self.show_all_products()
    def edit_product(self):
        selected_product_id = self.products_tree.item(self.products_tree.selection())["values"][0]
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        category_id = self.category_combobox.get()
        sql = "UPDATE product SET name = %s, description = %s, price = %s, quantity = %s, category_id = %s WHERE id = %s"
        val = (name, description, price, quantity, category_id, selected_product_id)
        self.cursor.execute(sql, val)
        self.db.commit()
        self.show_all_products()
        self.edit_window.destroy()
    
    def export_to_csv(self):
        self.cursor.execute("SELECT * FROM product")
        self.products = self.cursor.fetchall()
        with open("products.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.columns)
            for product in self.products:
                writer.writerow(product)
        messagebox.showinfo("Success", "Products exported to CSV")
        
    def add_product(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        category_id = self.category_combobox.get()
        sql = "INSERT INTO product (name, description, price, quantity, category_id) VALUES (%s, %s, %s, %s, %s)"
        val = (name, description, price, quantity, category_id)
        self.cursor.execute(sql, val)
        self.db.commit()
        self.add_window.destroy()
        self.show_all_products()

inventory = InventoryManagementSystem()
inventory.root.mainloop()

