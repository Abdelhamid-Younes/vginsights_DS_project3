#import os
import time
import db_config as cfg
from extract.download_extract import download_data, extract_data
from database.create_db import create_db
from database.create_tables import create_tables
from transform_load.load_data import create_df_meta, create_DataFrames, create_df_history, create_df_performances, create_df_regionals, create_df_stats, create_df_subgenres, load_to_db
from database.tables import games_schema, genres_schema, languages_schema, companies_schema, subgenres_schema, meta_schema, developers_schema, publishers_schema, regionals_schema, stats_schema, history_schema, performances_schema
from insights.create_views import create_views, stat_views
from insights.create_insights import create_insights, sql_insights

db_user=cfg.MY_DB["user"]   
db_password=cfg.MY_DB["password"] 
db_host=cfg.MY_DB["host"]   
db_name=cfg.MY_DB["db_name"]

url=cfg.paths['url']
save_as=cfg.paths['save_as']
data_dir_path=cfg.paths['data_dir_path']

start_time=time.time()

print("---------------------------------------- Start ETL process -----------------------------------------", end='\r')

print("Downloading compressed file .........................                                                   ", end='\r')
download_data( data_dir_path, url, save_as)

print("Extracting data .................................                                                   ", end='\r')
extract_data(save_as, data_dir_path)
print("Time taken  .... :   %s seconds ---" % (time.time() - start_time))

print("Creating database ................................                                                  ", end='\r')
create_db(db_user, db_password, db_host, db_name)

print("Creating tables ..................................                                                  ", end='\r')
create_tables(db_user, db_password, db_host, db_name)

print("Creating dataframes from json files and cleaning raw data ......                                    ", end='\r')

df_languages, df_genres, df_developers, df_publishers, df_games, df_companies = create_DataFrames(data_dir_path)
df_meta = create_df_meta(data_dir_path)
df_regionals = create_df_regionals(data_dir_path)
df_subgenres = create_df_subgenres(data_dir_path)
df_stats = create_df_stats(data_dir_path)
df_performances = create_df_performances(data_dir_path)
df_history = create_df_history(data_dir_path)

print("Loading data to db ..................................", end='\r')
load_to_db(df_games, 'games', games_schema, db_user, db_password, db_host, db_name)
load_to_db(df_publishers, 'publishers', publishers_schema, db_user, db_password, db_host, db_name)
load_to_db(df_developers, 'developers', developers_schema, db_user, db_password, db_host, db_name)
load_to_db(df_companies, 'companies', companies_schema, db_user, db_password, db_host, db_name)
load_to_db(df_genres, 'genres', genres_schema, db_user, db_password, db_host, db_name)
load_to_db(df_languages, 'languages', languages_schema, db_user, db_password, db_host, db_name)
load_to_db(df_meta, 'meta', meta_schema, db_user, db_password, db_host, db_name)
load_to_db(df_regionals, 'regionals', regionals_schema, db_user, db_password, db_host, db_name)
load_to_db(df_subgenres, 'subgenres', subgenres_schema, db_user, db_password, db_host, db_name)
load_to_db(df_stats, 'stats', stats_schema, db_user, db_password, db_host, db_name)
load_to_db(df_performances, 'performances', performances_schema, db_user, db_password, db_host, db_name)
load_to_db(df_history, 'history', history_schema, db_user, db_password, db_host, db_name)

print("Time taken  .... :   %s seconds ---" % (time.time() - start_time))

print("-------------------------------------ETL Process completed -----------------------------------------", end="\n")

print ("------------------------------------ Generating insights ------------------------------------------")

create_views(stat_views, db_host, db_name, db_user, db_password)
create_insights(sql_insights, db_host, db_name, db_user, db_password)

print("The streamlit application is now ready to run ")
print ("Run these commands to launch it : ")
print ("$ cd ./streamlit/")
print ("$ streamlit run home.py")