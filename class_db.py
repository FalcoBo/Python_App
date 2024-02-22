import os
import sqlite3
import shutil
from logging import Logger

# Class to handle the database
class Database:
    # Constructor
    def __init__(self, db):
        self.db = db
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.logger = Logger(name="Database_Logger")

    # Function to create a table in the database
    def create_table(self, table_name, columns):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.cursor.execute(create_table_query)
        self.conn.commit()
        self.logger.log(f"The table {table_name} was created successfully.")

    # Function to iclear a table in the database
    def clear_table(self, table_name):
        clear_table_query = f"DELETE FROM {table_name}"
        self.cursor.execute(clear_table_query)
        self.conn.commit()
        self.logger.log(f"The table {table_name} was cleared successfully.")

    # Function to choose the database
    def choose_db(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self.logger.log(f"The database {db} was chosen successfully.")

    # Function to save the database
    def save_db(source, destination):
        try:
            shutil.copy(source, destination)
            print("Database was saved successfully.")
        except:
            print("Database was not saved.")
        
    # Function to clear the database
    def clear_db(db):
        try:
            connection = sqlite3.connect(db)
            cursor = connection.cursor()
            cursor.execute('DELETE FROM users')
            connection.commit()
            connection.close()
            print("Database was cleared successfully.")
        except:
            print("Database was not cleared.")

    # Function to close the database
    def close_db(self):
        self.connection.close()
        self.logger.log("The connection to the database was closed successfully.")