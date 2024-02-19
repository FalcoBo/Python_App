import tkinter as tk
from tkinter import ttk

# Create the main window
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        
        self.create_widgets()

    def create_widgets(self):
        # Creating a label
        self.label = ttk.Label(self.root, text="Welcome to My Application!")
        self.label.pack(pady=10)
        
        # Creating a button
        self.button = ttk.Button(self.root, text="Click Me", command=self.button_clicked)
        self.button.pack()
    
    def button_clicked(self):
        self.label.config(text="Button Clicked!")