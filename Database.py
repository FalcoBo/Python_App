import os
import sqlite3
import shutil
from tkinter import filedialog
import logging
from logging import Logger


# Class to handle the database
class Database:
    # Constructor
    def __init__(self):
        self.db = None
        self.db_path = None
        self.connection = None
        self.cursor = None
        self.logger = Logger(name="Database_Logger")
        self.logger.setLevel(logging.INFO)

        # Configure logging to send messages to stdout
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    # Function to create a table in the database
    def create_table(self, table_name, columns):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(create_table_query)
        self.connection.commit()
        self.logger.info(f"The table {table_name} was created successfully.")

    # Function to clear all tables in the database
    def clear_db(self):
        try:
            # Get a list of all tables in the database
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()

            # Clear each table
            for table in tables:
                table_name = table[0]
                clear_table_query = f"DELETE FROM {table_name}"
                self.cursor.execute(clear_table_query)

            self.connection.commit()
            self.logger.info("All tables in the database were cleared successfully.")
        except Exception as e:
            self.logger.error(f"Error while clearing the database: {str(e)}")

    # Function to choose the database
    def choose_db(self):
        selected_file = filedialog.askopenfilename(title="Select Database File", filetypes=[("SQLite files", "*.db *.sqlite")])
        if selected_file:
            self.db_path = selected_file
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.logger.info(f"The database {self.db_path} was chosen successfully.")

    # Function to save the database
    def save_db(self, source, destination):
        try:
            shutil.copy(source, destination)
            self.logger.info("The database was saved successfully.")
        except Exception as e:
            self.logger.error(f"Error while saving the database: {str(e)}")
            
    # Method to download the data in the database
    def download_data(self):
        # Implement your download logic here
        pass

    # Function to close the database
    def close_db(self):
        self.connection.close()
        self.logger.info("The connection to the database was closed successfully.")
