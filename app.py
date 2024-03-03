import tkinter as tk
from tkinter import simpledialog
from tkinter import IntVar
from Database import Database
from Plot import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from Ebooks import Ebooks

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.geometry("900x650")
        self.database = Database(self)
        self.db_path = None
        self.ebooks = Ebooks(self)

        ctk.set_default_color_theme("themes\\dark-blue.json")

        self.mode_var = IntVar(value=0)

        self.create_widgets()

    # Method to create the widgets
    def create_widgets(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.log_display = tk.Text(self.main_frame, height=10, width=50)
        self.log_display.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame, width=250, height=600, relief=tk.RIDGE)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.database_button = tk.Button(self.left_frame, text="Database", command=self.show_database)
        self.database_button.pack(side=tk.TOP, fill=tk.X)

        self.ebooks_button = tk.Button(self.left_frame, text="Ebooks", command=self.show_ebooks)
        self.ebooks_button.pack(side=tk.TOP, fill=tk.X)

        self.dark_light = ctk.CTkSwitch(self.left_frame, command=self.dark_light_mode, variable=self.mode_var)
        self.dark_light.pack(side=tk.TOP, fill=tk.X)

        self.database_widgets = self.create_database_widgets()

        self.ebooks_widgets = self.create_ebooks_widgets()

        self.exit_button = ctk.CTkButton(self.left_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.show_database()

    # Method to create the database widgets
    def create_database_widgets(self):
        widgets = {}

        widgets["create_database_button"] = ctk.CTkButton(self.left_frame, text="Create a database", command=self.create_database)
        widgets["choose_database_button"] = ctk.CTkButton(self.left_frame, text="Choose a database", command=self.choose_db)
        widgets["save_database_button"] = ctk.CTkButton(self.left_frame, text="Save database", command=self.database.save_db)
        widgets["clear_db_button"] = ctk.CTkButton(self.left_frame, text="Clear the database", command=self.clear_database)
        widgets["create_table_button"] = ctk.CTkButton(self.left_frame, text="Create a table", command=self.create_table)
        widgets["download_data_button"] = ctk.CTkButton(self.left_frame, text="Download data", command=self.download_data)
        widgets["drop_table_button"] = ctk.CTkButton(self.left_frame, text="Drop table", command=self.drop_table)
        widgets["drop_all_tables_button"] = ctk.CTkButton(self.left_frame, text="Drop all tables", command=self.database.drop_all_tables)
        widgets["show_plot_button"] = ctk.CTkButton(self.left_frame, text="Show plot", command=self.show_plot)

        for widget in widgets.values():
            widget.pack(side=tk.TOP, fill=tk.X, pady=5)

        return widgets

    # Method to create the ebooks widgets
    def create_ebooks_widgets(self):
        widgets = {}

        widgets["download_ebook_button"] = ctk.CTkButton(self.left_frame, text="Download Ebook", command=self.download_ebook)
        widgets["plot_paragraph_lengths_button"] = ctk.CTkButton(self.left_frame, text="Plot Paragraph Lengths", command=self.plot_paragraph_lengths)
        widgets["create_word_document_button"] = ctk.CTkButton(self.left_frame, text="Create Word Document", command=self.create_word_document)

        for widget in widgets.values():
            widget.pack(side=tk.TOP, fill=tk.X, pady=5)

        return widgets

    # Method to set the database path
    def set_db_path(self, db_path):
        self.db_path = db_path
        self.append_log(f"Database chosen: {db_path}")

    # Method to choose the database
    def choose_db(self):
        db_path = self.database.choose_db()
        print(db_path)
        if db_path:
            self.set_db_path(db_path)
            print(db_path)

    # Method to show the database
    def show_database(self):
        for widget in self.ebooks_widgets.values():
            widget.pack_forget()
        for widget in self.database_widgets.values():
            widget.pack()

    # Method to show the ebooks
    def show_ebooks(self):
        for widget in self.database_widgets.values():
            widget.pack_forget()
        for widget in self.ebooks_widgets.values():
            widget.pack()

    # Method dark and light mode
    def dark_light_mode(self):
        value = self.mode_var.get()
        if value == 0:
            self.root.configure(background="white")
        else:
            self.root.configure(background="#2D2A4A")

    # Method to create a database
    def create_database(self):
        self.db_path = None
        self.database.create_database()
        self.append_log("Database created successfully.")

    # Method to clear the database
    def clear_database(self):
        if self.db_path == None:
            self.append_log("Please choose a database first.")
            return
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        self.database.clear_db(table_name)
        self.append_log(f"The database {table_name} was cleared successfully.")

    # Method to download the data
    def download_data(self):
        if self.db_path == None:
            self.append_log("Please choose a database first.")
            return
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if not table_name.strip():
            self.append_log("Please enter a valid table name.")
            return
        self.database.download_data(table_name)
        self.append_log(f"The data was downloaded and stored in the table {table_name} successfully.")

    # Method to drop a table
    def drop_table(self):
        if self.db_path == None:
            self.append_log("Please choose a database first.")
            return
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if table_name.strip():
            self.database.drop_table(table_name)
            self.append_log(f"The table {table_name} was dropped successfully.")
        else:
            self.append_log("Please enter a valid table name.")

    # Method to create a table
    def create_table(self):
        if self.db_path == None:
            self.append_log("Please choose a database first.")
            return
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if table_name is not None and table_name.strip():
            self.database.create_table(table_name)
            self.append_log(f"The table {table_name} was created successfully.")
        elif table_name is None:
            self.append_log("Please enter a valid table name.")

    # Method to append a log entry
    def append_log(self, log_entry, error=False):
        self.log_display.insert(tk.END, log_entry + "\n")
        self.log_display.see(tk.END)
        self.log_display.update()

    # Method to show the plot
    def show_plot(self):
        if self.db_path == None:
            self.append_log("Please choose a database first.")
            return
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if table_name:
            data = self.database.get_data(table_name)
            if data.empty:
                self.append_log(f"No data found in table '{table_name}'.")
                return
            plot = Plot()

            fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

            plot.bar_chart(data, "taille", "longueur", "Bar Chart", "Taille", "Longueur", ax=axes[0, 0])
            plot.line_chart(data, "taille", "longueur", "Line Chart", "Taille", "Longueur", ax=axes[0, 1])
            plot.scatter_chart(data, "taille", "longueur", "Scatter Chart", "Taille", "Longueur", ax=axes[1, 0])
            plot.pie_chart(data, "taille", "Pie Chart", ax=axes[1, 1])

            for ax in axes.flat:
                ax.label_outer()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        else:
            self.append_log("No table name entered.")


    # Methods for the Ebooks

    # Method to download an ebook
    def download_ebook(self):
        try:
            self.ebooks.download_ebook()
        except FileNotFoundError as e:
            self.append_log(f"An error occurred: {str(e)}")

    # Method to extract the ebook info
    def extract_ebook_info(self):
        if self.ebooks.book_title and self.ebooks.author_name and self.ebooks.first_chapter:
            self.append_log("Book Info: ")
            self.append_log(f"Title: {self.ebooks.book_title}")
            self.append_log(f"Author: {self.ebooks.author_name}")
            self.append_log(f"First Chapter: {self.ebooks.first_chapter}")
        else:
            self.append_log("Please download an ebook first.")

    # Method to plot the paragraph lengths
    def plot_paragraph_lengths(self):
        if self.ebooks.first_chapter:
            self.ebooks.count_paragraph_words()
            self.ebooks.plot_paragraph_lengths()
            self.append_log("Paragraph lengths plotted successfully.")
        else:
            self.append_log("Please download an ebook first.")

    # Method to create a word document
    def create_word_document(self):
        if self.ebooks.book_title and self.ebooks.author_name and self.ebooks.first_chapter:
            self.ebooks.create_word_document("ebook_document.docx")
            self.append_log("Word document created successfully.")
        else:
            self.append_log("Please download an ebook first.")