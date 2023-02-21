import mysql.connector
from sqlalchemy.types import *
from tables import games_table, meta_table, history_table, stats_table, performances_table, companies_table, genres_table, subgenres_table, regionals_table, languages_table, developers_table, publishers_table

def create_tables(user, password, host, db_name):
    """This function serves to create the sql tables of the database

    Args:
        user (str): Database user defined in config file.
        password (str): The password of the user to connect to db, defined in config file.
        host (str): IP address of the hostname, it defines the location of MySQL server and database.
        db_name (str): the name of the database, defined in config file.
    """

    try:
        # Establishing the connection to db
        conn = mysql.connector.connect(user=user, password=password, host=host, database=db_name)
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()


################################################# meta table ##################################################

        try:
            cursor.execute("DROP TABLE IF EXISTS meta")
            cursor.execute(meta_table)
            print("meta table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create meta table: {err}")

################################################# history table ###############################################

        try:
            cursor.execute("DROP TABLE IF EXISTS history")
            cursor.execute(history_table)
            print("history table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create history table: {err}")


################################################# stats table ###########################################

        try:
            cursor.execute("DROP TABLE IF EXISTS stats")
            cursor.execute(stats_table)
            print("stats table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create stats table: {err}")

################################################# performances table ##########################################

        try:
            cursor.execute("DROP TABLE IF EXISTS performances")
            cursor.execute(performances_table)
            print("performances table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create performances table: {err}")


################################################# companies table #############################################
        try:
            cursor.execute("DROP TABLE IF EXISTS companies")
            cursor.execute(companies_table)
            print("companies table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create companies table: {err}")

################################################# games table ##################################################
        try:
            cursor.execute("DROP TABLE IF EXISTS games")
            cursor.execute(games_table)
            print("games table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create games table: {err}")
                
################################################# developers table ##################################################
        try:
            cursor.execute("DROP TABLE IF EXISTS developers")
            cursor.execute(developers_table)
            print("developers table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create developers table: {err}")
                
################################################# publishers table ##################################################
        try:
            cursor.execute("DROP TABLE IF EXISTS publishers")
            cursor.execute(publishers_table)
            print("publishers table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create publishers table: {err}")

################################################# genres table ################################################

        try:
            cursor.execute("DROP TABLE IF EXISTS genres")
            cursor.execute(genres_table)
            print("genres table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create genres table: {err}")

################################################# subgenres table #############################################

        try:
            cursor.execute("DROP TABLE IF EXISTS subgenres")
            cursor.execute(subgenres_table)
            print("subgenres table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create subgenres table: {err}")

################################################# regionals table #############################################

        try:
            cursor.execute("DROP TABLE IF EXISTS regionals")
            cursor.execute(regionals_table)
            print("regionals table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create regionals table: {err}")

################################################# languages table #############################################

        try:
            cursor.execute("DROP TABLE IF EXISTS languages")
            cursor.execute(languages_table)
            print("languages table created successfully ")

        except mysql.connector.Error as err:
                print(f"Failed to create languages table: {err}")

    except mysql.connector.Error as err:
          print("Something went wrong while conneting to database ..")
###############################################################################################################