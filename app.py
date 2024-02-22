import tkinter as tk
from tkinter import ttk
from class_db import *

class App:
    # INITIALIZE
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.geometry("900x650")

        # Initialise the Class Database 
        self.class_db = Database

        # Set background color to black
        self.root.configure(background="#2D2A4A")

        # Create the left and right frames
        self.left_frame()
        self.right_frame()

        # Create the buttons on the left frame
        self.button_left(self.class_db)

        # Create a menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # 'Help' menu
        help_menu = tk.Menu(self.menu, tearoff=False)
        help_menu.add_command(label="About", command=self.about)
        self.menu.add_cascade(label="Help", menu=help_menu)

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
    def button_left(self, class_db):

        class_db = self.class_db

        # Button to create a database
        self.button_left = ttk.Button(self.left_frame, text="Create a database")
        self.button_left.pack()

        # Choose a database
        self.button_left = ttk.Button(self.left_frame, text="Choose a database", command=class_db.choose_db)
        self.button_left.pack()

        # Save the database
        self.button_left = ttk.Button(self.left_frame, text="Save database", command=class_db.save_db)
        self.button_left.pack()

        # Clear the database
        self.button_left = ttk.Button(self.left_frame, text="Clear the database", command=class_db.clear_table)
        self.button_left.pack()

        # Dowload data
        self.button_left = ttk.Button(self.left_frame, text="Dowload data", command=class_db.dowload_data)
        self.button_left.pack()

    # Show the logs of the database in the right frame
    def show_logs(self):
        vscode = ttk.Label(self.right_frame, text="Logs")
        vscode.pack()

    def Menu(self):
        pass

    def about(self):
        pass
