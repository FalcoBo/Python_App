import sqlite3
import shutil
from tkinter import filedialog
import logging
import requests
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
    def create_table(self, table_name):
        try:
            if self.table_exists(table_name):
                self.logger.warning(f"The table {table_name} already exists.")
                return
            columns = ["taille", "nom", "etat", "longueur"]
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
            create_table_query += ", ".join([f"{column} TEXT" for column in columns])
            create_table_query += ")"
            self.cursor.execute(create_table_query)
            self.connection.commit()
            self.logger.info(f"The table {table_name} was created successfully.")
        except Exception as e:
            self.logger.error(f"Error while creating the table {table_name}: {str(e)}")
        
    # Function to check if a table exists in the database
    def table_exists(self, table_name):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        self.cursor.execute(query)
        return bool(self.cursor.fetchone())
        
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
            self.cursor = self.connection.cursor()  # Initialiser le curseur ici
            self.logger.info(f"The database {self.db_path} was chosen successfully.")

    # Function to save the database
    def save_db(self, source, destination):
        try:
            shutil.copy(source, destination)
            self.logger.info("The database was saved successfully.")
        except Exception as e:
            self.logger.error(f"Error while saving the database: {str(e)}")
            
    # Method to download the data in the database
    def download_data(self, table_name):
        json_url = "https://jsonplaceholder.typicode.com/posts"

        try:
            response = requests.get(json_url)
            if response.status_code == 200:
                data = response.json()
                
                for row in data:
                    values = [row.get(column) for column in ["taille", "nom", "etat", "longueur"]]
                    insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(values))})"
                    self.cursor.execute(insert_query, values)
                
                self.connection.commit()
                self.logger.info(f"The data from {json_url} was downloaded and stored in the database successfully.")
            else:
                self.logger.error(f"Failed to download data from {json_url}. Status code: {response.status_code}")

        except FileNotFoundError:
            self.logger.error(f"The Database file {self.db_path} was not found.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while downloading the data from {json_url}: {e}")
        except ValueError:
            self.logger.error(f"The data from {json_url} is not in the expected format.")

    def drop_table(self, table_name):
        try:
            drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(drop_table_query)
            self.connection.commit()
            self.logger.info(f"The table {table_name} was dropped successfully.")
        except ValueError:
            self.logger.error(f"None of the tables in the database match the name {table_name}.")
        except FileNotFoundError:
            self.logger.error(f"The file {self.db_path} was not found.")

    def drop_all_tables(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            for table in tables:
                table_name = table[0]
                drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
                self.cursor.execute(drop_table_query)
            self.connection.commit()
            self.logger.info("All tables in the database were dropped successfully.")
        except FileNotFoundError:
            self.logger.error(f"The file {self.db_path} was not found.")

    # Function to close the database
    def close_db(self):
        try:
            self.connection.close()
            self.logger.info("The connection to the database was closed successfully.")
        except FileNotFoundError:
            self.logger.error(f"The file {self.db_path} was not found.")