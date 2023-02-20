import mysql.connector


def create_db(user, password, host, db_name):

    
        #establishing the connection to db
    conn = mysql.connector.connect(user=user, password=password, host=host)
        #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    
    try:
        #Droping database if already exists.
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        #Creating the database
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database {db_name} created successfully")

    except mysql.connector.Error as err:
          print(f"Something went wrong while creating database: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("The connection to database is closed")

#########################################################################################


