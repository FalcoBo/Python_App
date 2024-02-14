import os
import sqlite3
import shutil

def save_db(source, destination):
    try:
        shutil.copy(source, destination)
        print("Database was saved successfully.")
    except:
        print("Database was not saved.")