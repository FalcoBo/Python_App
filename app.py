import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.geometry("900x650")

        # Set background color to black
        self.root.configure(background="black")

        # Create a frame for the left part
        self.left_frame = ttk.Frame(self.root, width=500, height=800, relief=tk.RIDGE)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.left_frame.configure(borderwidth=15)

        # Create a frame for the right part
        self.right_frame = ttk.Frame(self.root, width=200, height=400, relief=tk.RIDGE)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Add widgets to the left frame
        self.label_left = ttk.Label(self.left_frame, text="Left Part", foreground="blue")  # Set font color to blue
        self.label_left.pack(pady=10)

        self.button_left = ttk.Button(self.left_frame, text="Button in Left Part")
        self.button_left.pack()

        # Add widgets to the right frame
        self.label_right = ttk.Label(self.right_frame, text="Right Part", foreground="blue")  # Set font color to blue
        self.label_right.pack(pady=10)

        self.button_right = ttk.Button(self.right_frame, text="Button in Right Part")
        self.button_right.pack()

        # Create a menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Create 'File' menu
        file_menu = tk.Menu(self.menu, tearoff=False)
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu.add_cascade(label="File", menu=file_menu)

        # Create 'Help' menu
        help_menu = tk.Menu(self.menu, tearoff=False)
        help_menu.add_command(label="About", command=self.about)
        self.menu.add_cascade(label="Help", menu=help_menu)

    def about(self):
        pass