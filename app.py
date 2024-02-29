import tkinter as tk
from tkinter import ttk
from Database import *

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.geometry("900x650")
        self.database = Database()
        self.db_path = None
        self.root.configure(background="#2D2A4A")

        self.create_widgets()

    # Other methods

    # Method to create the widgets
    def create_widgets(self):
        self.create_left_frame()
        self.create_right_frame()

    # Method to create the left frame
    def create_left_frame(self):
        self.left_frame = ttk.Frame(self.root, width=250, height=600, relief=tk.RIDGE)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Button(self.left_frame, text="Create a database").pack(pady=5)
        ttk.Button(self.left_frame, text="Choose a database", command=self.database.choose_db).pack(pady=5)
        ttk.Button(self.left_frame, text="Save database", command=self.database.save_db).pack(pady=5)

        clear_db_button = ttk.Button(self.left_frame, text="Clear the database", command=self.clear_database)
        clear_db_button.pack(pady=5)
        self.table_name_entry_clear = ttk.Entry(self.left_frame)
        self.table_name_entry_clear.pack()

        create_table_button = ttk.Button(self.left_frame, text="Create a table", command=self.create_table)
        create_table_button.pack(pady=5)
        self.table_name_entry_create = ttk.Entry(self.left_frame)
        self.table_name_entry_create.pack()

        download_data_button = ttk.Button(self.left_frame, text="Download data", command=self.download_data)
        download_data_button.pack(pady=5)
        self.table_name_entry_download = ttk.Entry(self.left_frame)
        self.table_name_entry_download.pack()

        drop_table_button = ttk.Button(self.left_frame, text="Drop table", command=self.drop_table)
        drop_table_button.pack(pady=5)
        self.table_name_entry_drop = ttk.Entry(self.left_frame)
        self.table_name_entry_drop.pack()

        ttk.Button(self.left_frame, text="Drop all tables", command=self.database.drop_all_tables).pack(pady=5)
        ttk.Button(self.left_frame, text="Exit", command=self.root.quit).pack(pady=5)

    # Method to create the right frame
    def create_right_frame(self):
        self.right_frame = ttk.Frame(self.root, width=600, height=600, relief=tk.RIDGE)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.log_display = tk.Text(self.right_frame, height=30, width=60)
        self.log_display.pack()

    # Method to clear the database
    def clear_database(self):
        table_name = self.table_name_entry_clear.get()
        self.database.clear_db(table_name)
        self.append_log(f"The database {table_name} was cleared successfully.")

    # Method to download the data
    def download_data(self):
        table_name = self.table_name_entry_download.get()
        if not table_name.strip():
            self.append_log("Please enter a valid table name.")
            return
        self.database.download_data(table_name)
        self.append_log(f"The data was downloaded and stored in the table {table_name} successfully.")

    # Method to drop a table
    def drop_table(self):
        table_name = self.table_name_entry_drop.get()
        if table_name.strip():
            self.database.drop_table(table_name)
            self.append_log(f"The table {table_name} was dropped successfully.")
        else:
            self.append_log("Please enter a valid table name.")

    # Method to create a table
    def create_table(self):
        table_name = self.table_name_entry_create.get()
        if table_name.strip():
            self.database.create_table(table_name)  # Pass the table_name here
            self.append_log(f"The table {table_name} was created successfully.")
        else:
            self.append_log("Please enter a valid table name.")
            
    # Method to append a log entry
    def append_log(self, log_entry):
        self.log_display.insert(tk.END, log_entry + "\n")
        self.log_display.see(tk.END)
        self.log_display.update()