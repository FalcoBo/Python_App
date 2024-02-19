import sqlite3
import os
import time
import functions


db_path = "C:/Users/Theo Boucebaine/Desktop/Projet_Python"
source = "data.db"
destination = "C:/Users/Theo Boucebaine/Desktop/Projet_Python/save/data.db"


# Check if the database exists in the specified path
database = os.path.exists(db_path)

if database == True:
    time.sleep(1)
    print("Database exists.")
    try :
        # Create a connection to the database
        time.sleep(1)
        connection = sqlite3.connect('data.db')
        print('Connection to the database was successful.')

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        # Execute SQL commands
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id int, username text, password text)')

        # Save the changes
        connection.commit()

        # Close the connection
        time.sleep(1)
        connection.close()
        print('The connection to the database was closed successfully.')

        functions.save_db(source, destination)

    except sqlite3.Error:
        print("The connection to the database failed.")
else:
    print("Database does not exist.")

    # Create the database
    connection = sqlite3.connect('data.db')
    print("The database was created successfully.")