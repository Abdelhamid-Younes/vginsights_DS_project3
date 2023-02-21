#import os
#import yaml
import time
import db_config as cfg
from download_extract import download_data, extract_data
from create_db import create_db
from create_tables import create_tables
from load_data import create_df_meta, create_DataFrames, create_df_companies, create_df_history, create_df_performances, create_df_regionals, create_df_stats, create_df_subgenres, load_to_db
from tables import games_schema, genres_schema, languages_schema, companies_schema, subgenres_schema, meta_schema, developers_schema, publishers_schema, regionals_schema, stats_schema, history_schema, performances_schema


db_user=cfg.MY_DB["user"]   
db_password=cfg.MY_DB["password"] 
db_host=cfg.MY_DB["host"]   
db_name=cfg.MY_DB["db_name"]

url=cfg.paths['url']
save_as=cfg.paths['save_as']
data_dir_path=cfg.paths['data_dir_path']

start_time=time.time()

# print("------------------ Starting process --------------", end='\r')
#print("------------------------------------------------------------")

#print("Loading compressed file ..........................", end='\r')
#download_data( data_dir_path, url, save_as)

#print("Extracting data ..................................", end='\r')
#extract_data(save_as, data_dir_path)

# print("Creating database ................................", end='\r')
# create_db(db_user, db_password, db_host, db_name)

# print("Creating tables ..................................", end='\r')
# create_tables(db_user, db_password, db_host, db_name)

print("Creating dataframes from json files and cleaning raw data ...............")


df_languages, df_genres, df_developers, df_publishers, df_games = create_DataFrames(data_dir_path)
#df_companies = create_df_companies(data_dir_path)
#df_meta = create_df_meta(data_dir_path)
#df_regionals = create_df_regionals(data_dir_path)
#df_subgenres = create_df_subgenres(data_dir_path)
#df_stats = create_df_stats(data_dir_path)
#df_performances = create_df_performances(data_dir_path)
#df_history = create_df_history(data_dir_path)

#print(df_history)
load_to_db(df_games, 'games', games_schema, db_user, db_password, db_host, db_name)

'''
loading_to_db(df_name=df_games, table_name='games', table_schema=games_schema)
loading_to_db(df_name=df_publishers, table_name='publishers', table_schema=publishers_schema)
loading_to_db(df_name=df_developers, table_name='developers', table_schema=developers_schema)
loading_to_db(df_name=df_languages, table_name='languages', table_schema=languages_schema)
loading_to_db(df_name=df_genres, table_name='genres', table_schema=genres_schema)
loading_to_db(df_name=df_companies, table_name='companies', table_schema=companies_schema)

loading_to_db(df_name=df_meta, table_name='meta', table_schema=meta_schema)

loading_to_db(df_name=df_regionals, table_name='regionals', table_schema=regionals_schema)

loading_to_db(df_name=df_subgenres, table_name='subgenres', table_schema=subgenres_schema)

loading_to_db(df_name=df_stats, table_name='stats', table_schema=stats_schema)

loading_to_db(df_name=df_performances, table_name='performances', table_schema=performances_schema)

loading_to_db(df_name=df_history, table_name='history', table_schema=history_schema)
'''





'''    
    
print("------------------------------------------------------------")
print("------------------- END OF LOAD ----------------------------")
'''


print("Time taken  .... :   %s seconds ---" % (time.time() - start_time))
