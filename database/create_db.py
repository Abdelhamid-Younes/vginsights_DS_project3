import mysql.connector

def create_db(user, password, host, db_name):
    """This function allows to create the database.

    Args:
        user (str): Database user defined in config file.
        password (_type_): The password of the user to connect to db, defined in config file.
        host (str): IP address of the hostname, it defines the location of MySQL server and database.
        db_name (str): the name of the database, defined in config file. 
    """
    
    # Establishing the connection to db
    conn = mysql.connector.connect(user=user, password=password, host=host)
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    try:
        # Droping database if already exists.
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        # Creating the database
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database {db_name} created successfully")

    except mysql.connector.Error as err:
          print(f"Something went wrong while creating database: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("The connection to database is closed")

######################################################################################################
