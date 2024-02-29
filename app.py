import tkinter as tk
from tkinter import ttk, simpledialog
from Database import *
from Plot import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.geometry("900x650")
        self.database = Database()
        self.db_path = None
        self.root.configure(background="#2D2A4A")

        self.create_widgets()

    # Method to create the widgets
    def create_widgets(self):
        self.left_frame = ttk.Frame(self.root, width=250, height=600, relief=tk.RIDGE)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Button(self.left_frame, text="Create a database").pack(pady=5)
        ttk.Button(self.left_frame, text="Choose a database", command=self.database.choose_db).pack(pady=5)
        ttk.Button(self.left_frame, text="Save database", command=self.database.save_db).pack(pady=5)

        clear_db_button = ttk.Button(self.left_frame, text="Clear the database", command=self.clear_database)
        clear_db_button.pack(pady=5)

        create_table_button = ttk.Button(self.left_frame, text="Create a table", command=self.create_table)
        create_table_button.pack(pady=5)

        download_data_button = ttk.Button(self.left_frame, text="Download data", command=self.download_data)
        download_data_button.pack(pady=5)

        drop_table_button = ttk.Button(self.left_frame, text="Drop table", command=self.drop_table)
        drop_table_button.pack(pady=5)

        ttk.Button(self.left_frame, text="Drop all tables", command=self.database.drop_all_tables).pack(pady=5)
        ttk.Button(self.left_frame, text="Exit", command=self.root.quit).pack(pady=5)

        self.plot_frame = ttk.Frame(self.root, width=600, height=600, relief=tk.RIDGE)
        self.plot_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.log_display = tk.Text(self.plot_frame, height=10, width=60)
        self.log_display.pack()

        plot_button = ttk.Button(self.plot_frame, text="Show the plots", command=self.show_plot)
        plot_button.pack(pady=5)

    # Method to clear the database
    def clear_database(self):
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        self.database.clear_db(table_name)
        self.append_log(f"The database {table_name} was cleared successfully.")

    # Method to download the data
    def download_data(self):
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if not table_name.strip():
            self.append_log("Please enter a valid table name.")
            return
        self.database.download_data(table_name)
        self.append_log(f"The data was downloaded and stored in the table {table_name} successfully.")

    # Method to drop a table
    def drop_table(self):
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if table_name.strip():
            self.database.drop_table(table_name)
            self.append_log(f"The table {table_name} was dropped successfully.")
        else:
            self.append_log("Please enter a valid table name.")

    # Method to create a table
    def create_table(self):
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if table_name is not None and table_name.strip():
            self.database.create_table(table_name)
            self.append_log(f"The table {table_name} was created successfully.")
        elif table_name is not None:
            self.append_log("Please enter a valid table name.")

    # Method to append a log entry
    def append_log(self, log_entry):
        self.log_display.insert(tk.END, log_entry + "\n")
        self.log_display.see(tk.END)
        self.log_display.update()

    # Method to show the plot
    def show_plot(self):
        table_name = simpledialog.askstring("Table Selection", "Enter table name:")
        if table_name:
            data = self.database.get_data(table_name)
            if data.empty:
                self.append_log(f"No data found in table '{table_name}'.")
                return
            plot = Plot()

            fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

            plot.bar_chart(data, "taille", "longueur", "Bar Chart", "Taille", "Longueur", ax=axes[0, 0])
            plot.line_chart(data, "taille", "longueur", "Line Chart", "Taille", "Longueur", ax=axes[0, 1])  # Ajout de l'argument ax
            plot.scatter_chart(data, "taille", "longueur", "Scatter Chart", "Taille", "Longueur", ax=axes[1, 0])
            plot.pie_chart(data, "taille", "Pie Chart", ax=axes[1, 1])

            for ax in axes.flat:
                ax.label_outer()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        else:
            self.append_log("No table name entered.")

