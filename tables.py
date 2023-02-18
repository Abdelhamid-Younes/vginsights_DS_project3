from sqlalchemy.types import *

games_table = """CREATE TABLE games
                                    (
                                     steam_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                     game_name VARCHAR(255),
                                     release_date DATE,
                                     price FLOAT,
                                     price_final FLOAT,
                                     rating INTEGER,
                                     reviews INTEGER,
                                     reviews_positive INTEGER,
                                     reviews_negative INTEGER,
                                     rank_reviews INTEGER,
                                     units_sold_vgi INTEGER,
                                     revenue_vgi INTEGER,
                                     url_vgi VARCHAR(50)

                                     );"""
                         #            developer VARCHAR(255),
                          #           publisher VARCHAR(255),
                           #          publisher_type VARCHAR(10),
                                     
                                     #FOREIGN KEY (developer) REFERENCES companies(company_name),
                                     #FOREIGN KEY (publisher) REFERENCES companies(company_name)

meta_table = """CREATE TABLE meta
                                    (
                                     steam_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                     website VARCHAR(255),
                                     comingSoon BOOLEAN,
                                     isReleased BOOLEAN,
                                     releaseDate DATE,
                                     shortDescription VARCHAR(500),
                                     earliestReviewDate DATE
                                     );"""


history_table = """CREATE TABLE history
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     date DATE NOT NULL,
                                     players_avg INTEGER,
                                     units INTEGER,
                                     units_increase INTEGER,
                                     members INTEGER,
                                     reviews INTEGER,
                                     rating FLOAT,
                                     PRIMARY KEY (steam_id, date)
                                     );"""

stats_table = """CREATE TABLE stats
                                    (
                                     steam_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                     avg_playtime INTEGER,
                                     med_playtime INTEGER,
                                     max_players_24h INTEGER,
                                     players_latest INTEGER,
                                     players_latest_time INTEGER,
                                     avg6Months INTEGER 
                                     );"""

performances_table = """CREATE TABLE performances
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     perf_name VARCHAR(100),
                                     perf_rank INTEGER,
                                     prct FLOAT,
                                     nb_games INTEGER,
                                     PRIMARY KEY (steam_id, perf_name)
                                     );"""

companies_table = """CREATE TABLE companies
                                    (
                                     company_name VARCHAR(255) NOT NULL PRIMARY KEY,
                                     company_id INTEGER,
                                     slug VARCHAR(255)
                                     );"""

genres_table = """CREATE TABLE genres
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     genre VARCHAR(50),
                                     PRIMARY KEY (steam_id, genre)
                                     );"""

subgenres_table = """CREATE TABLE subgenres
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     genreName VARCHAR(50) NOT NULL,
                                     nrOfGames INTEGER,
                                     RankOfRatings INTEGER,
                                     rankOfPositiveRatings INTEGER,
                                     PRIMARY KEY (steam_id, genreName)
                                     );"""

regionals_table = """CREATE TABLE regionals
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     region VARCHAR(50),
                                     playersPrct FLOAT,
                                     PRIMARY KEY (steam_id, region)
                                     );"""

languages_table = """CREATE TABLE languages
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     language VARCHAR(50),
                                     PRIMARY KEY (steam_id, language)
                                     );"""
                                     
developers_table = """CREATE TABLE developers
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     developer VARCHAR(100) NOT NULL,
                                     PRIMARY KEY (steam_id, developer)
                                     );"""              

publishers_table = """CREATE TABLE publishers
                                    (
                                     steam_id INTEGER NOT NULL AUTO_INCREMENT,
                                     publisher VARCHAR(100) NOT NULL,
                                     publisher_type VARCHAR(20),
                                     PRIMARY KEY (steam_id, publisher)
                                     );""" 

################################################# Dataframes schema #################################################
languages_schema = {
                     "steam_id": Integer,    
                      "language": String(50)
                    }

genres_schema = {
                    "steam_id": Integer,    
                    "genre": String(50)
                    }

games_schema = {
                    "steam_id": Integer,    
                    "game_name": String(255),
                    "release_date": Date,
                    "price": Float,
                    "price_final": Float,    
                    "rating": Integer,
                    "reviews": Integer,
                    "reviews_positive": Integer,
                    "reviews_negative": Integer,
                    "rank_reviews": Integer,    
                    "units_sold_vgi": Integer,
                    "revenue_vgi": Integer,    
                    "url_vgi": String(50)
                    }

developers_schema = {
                         "steam_id": Integer,    
                         "developer": String(100)
}
publishers_schema = {
                         "steam_id": Integer,    
                         "publisher": String(100),
                         "publisher_type": String(20)
}


companies_schema = {
                       "company_name": String(255),
                       "company_id": Integer, 
                       "slug": String(100)
}

meta_schema = {
                "steam_id": Integer,    
                "website": String(255),
                "comingSoon": Boolean,
                "isReleased": Boolean,    
                "releaseDate": Date,
                "shortDescription": String(500),
                "earliestReviewDate": Date
}
regionals_schema = {
                       "steam_id": Integer,    
                       "region": String(50),
                       "playersPrct": Float
}

stats_schema = {
                    "steam_id": Integer,    
                    "avg_playtime": Integer,
                    "med_playtime": Integer,    
                    "max_players_24h": Integer,
                    "players_latest": Integer,
                    "players_latest_time": Integer,
                    "avg6Months": Integer
}

history_schema = {
                      "steam_id": Integer,    
                      "date": Date,
                      "players_avg": Integer,
                      "units": Integer,    
                      "units_increase": Integer,
                      "members": Integer,
                      "reviews": Integer,
                      "rating": Float
}

performances_schema = {
                          "steam_id": Integer,    
                          "perf_name": String(100),
                          "perf_rank": Integer,    
                          "prct": Float,
                          "nb_games": Integer
}

subgenres_schema = {
                    "steam_id": Integer,    
                    "genreName": String(100),
                    "nrOfGames": Integer,
                    "RankOfRatings": Integer,    
                    "rankOfPositiveRatings": Integer
}