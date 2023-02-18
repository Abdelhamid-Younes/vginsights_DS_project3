import mysql.connector

db_user='root'
db_password='password'
db_host='127.0.0.1'
db_name='vgi_db'



def create_db(user, password, host, db_name):

    try:
        #establishing the connection to db
        conn = mysql.connector.connect(user=user, password=password, host=host)
        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

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

create_db(db_user, db_password, db_host, db_name)
