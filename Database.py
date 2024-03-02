import sqlite3
import shutil
from tkinter import filedialog
import logging
import requests
from logging import Logger
import pandas as pd

class Database:
    def __init__(self, app_instance):
        self.db = None
        self.db_path = None
        self.connection = None
        self.cursor = None
        self.logger = Logger(name="Database_Logger")
        self.logger.setLevel(logging.INFO)
        self.app = app_instance 

        # Function to create a logger
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    # Method to create a database
    def create_database(self):
        try:
            self.db_path = filedialog.asksaveasfilename(title="Create Database File", filetypes=[("SQLite files", "*.db *.sqlite")])
            if self.db_path:
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()
                self.logger.info(f"The database {self.db_path} was created successfully.")
                self.app.append_log(f"The database {self.db_path} was created successfully.")
        except Exception as e:
            self.logger.error(f"Error while creating the database: {str(e)}")
            
            self.app.append_log(f"Error while creating the database: {str(e)}", error=True)

    # Method to create a table in the database
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
            self.app.append_log(f"The table {table_name} was created successfully.")
        except Exception as e:
            self.logger.error(f"Error while creating the table {table_name}: {str(e)}")
            
            self.app.append_log(f"Error while creating the table {table_name}: {str(e)}", error=True)
        
    # Method to check if a table exists in the database
    def table_exists(self, table_name):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        self.cursor.execute(query)
        return bool(self.cursor.fetchone())
        
    # Method to clear the database
    @staticmethod
    def clear_db(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()

            for table in tables:
                table_name = table[0]
                clear_table_query = f"DELETE FROM {table_name}"
                self.cursor.execute(clear_table_query)

            self.connection.commit()
            self.logger.info("All tables in the database were cleared successfully.") 
            self.app.append_log("All tables in the database were cleared successfully.")
        except Exception as e:
            self.logger.error(f"Error while clearing the database: {str(e)}")
            self.app.append_log(f"Error while clearing the database: {str(e)}", error=True)
            
    # Method to choose the database
    def choose_db(self):
        try:
            selected_file = filedialog.askopenfilename(title="Select Database File", filetypes=[("SQLite files", "*.db *.sqlite")])
            if selected_file:
                self.db_path = selected_file
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()  # Initialiser le curseur ici
                self.logger.info(f"The database {self.db_path} was chosen successfully.")
                self.app.append_log(f"The database {self.db_path} was chosen successfully.")
        except Exception as e:
            self.logger.error(f"Error while choosing the database: {str(e)}")
            
            self.app.append_log(f"Error while choosing the database: {str(e)}", error=True)

    # Method to save the database
    def save_db(self, source, destination):
        try:
            shutil.copy(source, destination)
            self.logger.info("The database was saved successfully.")
            self.app.append_log("The database was saved successfully.")
        except Exception as e:
            self.logger.error(f"Error while saving the database: {str(e)}")
            self.app.append_log(f"Error while saving the database: {str(e)}", error=True)

    # Method to download the data in the database
    @staticmethod
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
                self.app.append_log(f"The data from {json_url} was downloaded and stored in the database successfully.")
            else:
                self.logger.error(f"Failed to download data from {json_url}. Status code: {response.status_code}")
                self.app.append_log(f"Failed to download data from {json_url}. Status code: {response.status_code}", error=True)

        except FileNotFoundError:
            self.logger.error(f"The Database file {self.db_path} was not found.")
            self.app.append_log(f"The Database file {self.db_path} was not found.", error=True)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while downloading the data from {json_url}: {e}")
            self.app.append_log(f"An error occurred while downloading the data from {json_url}: {e}", error=True)
        except ValueError:
            self.logger.error(f"The data from {json_url} is not in the expected format.")
            self.app.append_log(f"The data from {json_url} is not in the expected format.", error=True)

    # Method to get the data from the database
    @staticmethod
    def get_data(self, table_name):
        try:
            select_query = f"SELECT * FROM {table_name}"
            self.cursor.execute(select_query)
            data = self.cursor.fetchall()
            self.logger.info(f"The data from the table {table_name} was retrieved successfully.")
            self.app.append_log(f"The data from the table {table_name} was retrieved successfully.")
            df = pd.DataFrame(data, columns=[desc[0] for desc in self.cursor.description])
            return df
        except FileNotFoundError:
            self.logger.error(f"The file {self.db_path} was not found.")
            self.app.append_log(f"The file {self.db_path} was not found.", error=True)
            return pd.DataFrame()
        except ValueError:
            self.logger.error(f"None of the tables in the database match the name {table_name}.")
            self.app.append_log(f"None of the tables in the database match the name {table_name}.", error=True)
            return pd.DataFrame()

    # Method to drop a table from the database
    @staticmethod
    def drop_table(self, table_name):
        try:
            drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(drop_table_query)
            self.connection.commit()
            self.logger.info(f"The table {table_name} was dropped successfully.")
            self.app.append_log(f"The table {table_name} was dropped successfully.")
        except ValueError:
            self.logger.error(f"None of the tables in the database match the name {table_name}.")
            self.app.append_log(f"None of the tables in the database match the name {table_name}.", error=True)
        except FileNotFoundError:
            self.logger.error(f"The file {self.db_path} was not found.")
            self.app.append_log(f"The file {self.db_path} was not found.", error=True)

    # Methode to drop all tables from the database
    @staticmethod
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
            self.app.append_log("All tables in the database were dropped successfully.")
        except FileNotFoundError:
            self.logger.error(f"The file {self.db_path} was not found.")
            self.app.append_log(f"The file {self.db_path} was not found.", error=True)

    # Methode to close the database
    @staticmethod
    def close_db(self):
        try:
            self.connection.close()
            self.logger.info("The connection to the database was closed successfully.")
            self.app.append_log("The connection to the database was closed successfully.")
        except FileNotFoundError:
            self.logger.error(f"The file {self.db_path} was not found.")
            self.app.append_log(f"The file {self.db_path} was not found.", error=True)
            