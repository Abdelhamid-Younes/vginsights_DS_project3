import mysql.connector
from mysql.connector import Error


def create_insights(sql_insights, host, db_name, user, password):
    """This function serves to Create some insights using SQL queries

    Args:
        stat_views (dict): Contains the schema of each view.
        user (str): Database user defined in config file.
        password (_type_): The password of the user to connect to db, defined in config file.
        host (str): IP address of the hostname, it defines the location of MySQL server and database.
        db_name (str): the name of the database, defined in config file. 
    """

    try:
        # Establishing the connection to db
        conn = mysql.connector.connect(host=host,
                                         database=db_name,
                                         user=user,
                                         password=password)
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        
        print(f"Connection to database {db_name} established successfully")

        for view in sql_insights.keys():
            try: 
                cursor = conn.cursor()
                cursor.execute(f"CREATE OR REPLACE VIEW {view} AS {sql_insights.get(view)}")
                conn.commit()
                print(f"The insights TABLE {view} created successfully {view}")
                
            except mysql.connector.Error as error:
                print(f"Failed to create insights view {view}: {error}")

    except mysql.connector.Error as error:
        print(f"Failed to connect to database {db_name}: {error}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print(f"Connection to database {db_name} is closed")  
            
sql_insights = {
       
    "top_games_revenue": """
                            SELECT game_overview.game_name, game_stats.revenue_vgi
                            FROM game_overview
                            JOIN game_stats ON game_overview.steam_id = game_stats.steam_id
                            ORDER BY game_stats.revenue_vgi DESC LIMIT 10;
                            """,
                            
    "top_games_followers": """
                            SELECT g.game_name, SUM(h.members) AS total_members
                            FROM game_overview AS g
                            JOIN history AS h ON g.steam_id = h.steam_id
                            WHERE h.date BETWEEN '2022-11-10' AND '2022-11-16'
                            GROUP BY g.steam_id
                            ORDER BY total_members DESC LIMIT 10;
                            """,
                            
    "top_games_reviews": """
                        SELECT g.game_name, SUM(h.reviews) AS total_reviews
                        FROM game_overview g
                        JOIN history h ON g.steam_id = h.steam_id
                        WHERE h.date BETWEEN '2022-11-10' AND '2022-11-16'
                        GROUP BY g.game_name
                        ORDER BY total_reviews DESC LIMIT 10;
                            """
}