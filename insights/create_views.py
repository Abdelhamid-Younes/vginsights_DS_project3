import mysql.connector
from mysql.connector import Error


def create_views(stat_views, host, db_name, user, password):
    """This function serves to Create views needed for data visualization

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
        
        for view in stat_views.keys():
            try: 
                cursor = conn.cursor()
                cursor.execute(f"CREATE OR REPLACE VIEW {view} AS {stat_views.get(view)}")
                conn.commit()
                print(f" The view  {view} created successfully")
                
            except mysql.connector.Error as error:
                print(f"Failed to create the view {view}: {error}")

    except mysql.connector.Error as error:
        print(f"Failed to connect to database {db_name}: {error}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print(f"Connection to database {db_name} is closed")    



stat_views = {
    "developer_stats": """
                        SELECT 
                            d.developer AS 'Developer name',
                            COUNT(DISTINCT g.steam_id) AS 'Developed Games',
                            MIN(g.release_date) AS 'First Game Developed',
                            MAX(g.release_date) AS 'Last Game Developed',
                            SUM(g.revenue_vgi) AS 'Total Lifetime Revenue',
                            AVG(g.revenue_vgi) AS 'Average Revenue per Game'
                        FROM developers d
                        JOIN games g ON g.steam_id = d.steam_id
                        GROUP BY d.developer;     
                                                    """,
                            
    "publisher_stats": """
                        SELECT 
                            publishers.publisher AS `Publisher name`,
                            COUNT(DISTINCT games.steam_id) AS `Published Games`,
                            MIN(games.release_date) AS `First Game published`,
                            MAX(games.release_date) AS `Last Game published`,
                            SUM(games.revenue_vgi) AS `Total Lifetime Revenue`,
                            AVG(games.revenue_vgi) AS `Average Revenue per Game`,
                            publishers.publisher_type AS `Publisher type`
                        FROM 
                            publishers
                        JOIN games ON publishers.steam_id = games.steam_id
                        GROUP BY 
                            publishers.publisher, 
                            publishers.publisher_type; 
                                                    """,

    "game_overview": """
                        SELECT g.steam_id, g.game_name,
                            GROUP_CONCAT(DISTINCT dev.developer ORDER BY dev.developer ASC SEPARATOR ', ') AS Developers,
                            GROUP_CONCAT(DISTINCT pub.publisher ORDER BY pub.publisher ASC SEPARATOR ', ') AS Publishers,
                            g.release_date AS `Release Date`,
                            g.price AS `Current Price`,
                            s.avg6Months AS `Avg Price during last 6 months`,
                            GROUP_CONCAT(DISTINCT gen.genre ORDER BY gen.genre ASC SEPARATOR ', ') AS Genres,
                            GROUP_CONCAT(DISTINCT lang.language ORDER BY lang.language ASC SEPARATOR ', ') AS Languages,
                            m.shortDescription AS Description,
                            g.url_vgi AS `Game URL Link`
                        FROM
                            games g
                                LEFT JOIN developers dev ON g.steam_id = dev.steam_id
                                LEFT JOIN publishers pub ON g.steam_id = pub.steam_id
                                LEFT JOIN genres gen ON g.steam_id = gen.steam_id
                                LEFT JOIN languages lang ON g.steam_id = lang.steam_id
                                LEFT JOIN meta m ON g.steam_id = m.steam_id
                                LEFT JOIN stats s ON g.steam_id = s.steam_id
                        GROUP BY
                            g.steam_id 
                                                    """,
                            
    "game_stats": """
                        SELECT g.steam_id, s.max_players_24h, s.players_latest, g.reviews_positive, g.revenue_vgi, g.units_sold_vgi, s.avg_playtime, s.med_playtime
                        FROM stats s
                        JOIN games g ON s.steam_id = g.steam_id;
                                            """,



}
