import tkinter as tk
from tkinter import ttk
from Database import *

class App:
    # INITIALIZE
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.geometry("900x650")

        # Initialise the Class Database
        self.database = Database()
        self.db_path = None

        # Set background color
        self.root.configure(background="#2D2A4A")

        # Create the left and right frames
        self.left_frame()
        self.right_frame()

        # Create the buttons on the left frame
        self.button_left(self.database)

        # Source and destination of the database
        self.source = None
        self.destination = self.db_path

    # METHODES

    # Methode to create the left frame
    def left_frame(self):
        self.left_frame = ttk.Frame(self.root, width=250, height=600, relief=tk.RIDGE)
        self.left_frame.pack(side=tk.LEFT, padx=0, pady=0)

    # Methode to create the right frame
    def right_frame(self):
        self.right_frame = ttk.Frame(self.root, width=1000, height=600, relief=tk.RIDGE)
        self.right_frame.pack(side=tk.RIGHT, padx=0, pady=0)
        self.show_logs()

    # Methode to create the buttons on the left frame
    def button_left(self, database):

        database = self.database

        # Button to create a database
        self.button_left = ttk.Button(self.left_frame, text="Create a database")
        self.button_left.pack()

        # Choose a database
        self.button_left = ttk.Button(self.left_frame, text="Choose a database", command=database.choose_db)
        self.button_left.pack()

        # Save the database
        self.button_left = ttk.Button(self.left_frame, text="Save database", command=database.save_db)
        self.button_left.pack()

        # Clear the database
        self.button_left = ttk.Button(self.left_frame, text="Clear the database", command=database.clear_db)
        self.button_left.pack()
        self.table_name_entry_to_clear()

        # Dowload data
        self.button_left = ttk.Button(self.left_frame, text="Dowload data", command=self.download_data)
        self.button_left.pack()

        # Drop the table
        self.button_left = ttk.Button(self.left_frame, text="Drop the table", command=self.drop_table)
        self.button_left.pack()
        self.table_name_entry_to_drop()

        # Drop all tables
        self.button_left = ttk.Button(self.left_frame, text="Drop all tables", command=database.drop_all_tables)
        self.button_left.pack()

        # Exit
        self.button_left = ttk.Button(self.left_frame, text="Exit", command=self.root.quit)
        self.button_left.pack()

    # Create the entry to enter the name of the table
    def table_name_entry_to_clear(self):
        self.table_name = tk.StringVar()
        self.table_name_entry = ttk.Entry(self.left_frame, textvariable=self.table_name)
        self.table_name_entry.pack()

    # Create the entry to enter the name of the table
    def table_name_entry_to_drop(self):
        self.table_name = tk.StringVar()
        self.table_name_entry = ttk.Entry(self.left_frame, textvariable=self.table_name)
        self.table_name_entry.pack()

    # Show the logs of the database in the right frame
    def show_logs(self):
        self.log_display = tk.Text(self.right_frame, height=30, width=80)
        self.log_display.pack()

    def append_log(self, log_entry):
        self.log_display.insert(tk.END, log_entry + "\n")
        self.log_display.see(tk.END)
    
    def download_data(self):
        table_name = self.table_name.get()
        self.database.download_data(table_name)

    def drop_table(self):
        table_name = self.table_name.get()
        self.database.drop_table(table_name)

    def Menu(self):
        pass

    def about(self):
        pass
