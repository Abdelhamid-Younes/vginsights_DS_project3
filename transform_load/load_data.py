import pandas as pd
import numpy as np
import os, json
import glob
from unidecode import unidecode
from sqlalchemy import create_engine
from sqlalchemy.types import *


def create_DataFrames(data_dir_path):
    """ This function serves to create clean dataframes from json files 

    Args:
        data_dir_path (str): The path directory where the raw data is stored

    Returns:
        Dataframe: Returns many dataframes with a cleaned data ready to load to db.
    """
    files_list = glob.glob('{}/Games5/*game_url.json'.format(data_dir_path))
    
    #df_games_raw = pd.concat((pd.json_normalize(json.load(open(file))) for file in files_list), ignore_index=True)
    
    df_games_raw = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing games and companies files... {round(((i+1)/len(files_list))*100, 2)}% complete                  ", end='\r')
        data = pd.json_normalize(json.load(open(file)))
        df_games_raw = pd.concat([df_games_raw,data],axis=0)
    
    # Create_df_languages
    df_languages = df_games_raw[['steam_id', 'languages']].copy()
    df_languages.rename(columns = {'languages':'language'}, inplace = True)
    df_languages["language"] = df_languages["language"].astype(str).str.split(',')
    df_languages = df_languages.explode(column="language", ignore_index = True)
    df_languages['language'] = df_languages['language'].str.strip()
    df_languages = df_languages.drop_duplicates()
    
    # Create df_genres
    df_genres = df_games_raw[['steam_id', 'genres']].copy()
    df_genres.columns.values[1] = "genre"
    df_genres["genre"] = df_genres["genre"].astype(str).str.split(',')
    df_genres = df_genres.explode(column='genre', ignore_index = True) 
    df_genres['genre'] = df_genres['genre'].str.strip()
    df_genres = df_genres.drop_duplicates()
    
    # Create df_games
    df_games = df_games_raw.copy()
    df_games.drop(["genres", "languages", "rank_positive_rating"], axis=1, inplace=True)
    vgi_games = pd.read_csv('./data/vgi_games.csv')
    df_columns = vgi_games[['steam_id','publishers_type', 'url_vgi']]
    df_games = pd.merge(df_games, df_columns, how ='inner', on =['steam_id'])
    df_games.rename(columns = {'name':'game_name', 'released':'release_date', 'developers':'developer', 'publishers':'publisher', 'publishers_type':'publisher_type',}, inplace = True)
    df_games['release_date'] = df_games['release_date'].str.split('T').str[0]
    
    # Create df_developers from df_games
    df_developers = df_games[['steam_id', 'developer']].copy()
    df_developers["developer"] = df_developers["developer"].astype(str).str.split(',')
    df_developers = df_developers.explode(column='developer', ignore_index = True)
    df_developers['developer'] = df_developers['developer'].str.strip()
    df_developers['developer'] = df_developers['developer'].apply(unidecode)
    df_developers['developer2'] = df_developers['developer'].str.upper()
    df_developers.drop_duplicates(subset=['steam_id','developer2'], inplace=True, keep="first")
    df_developers.drop(columns = 'developer2', inplace = True)
    
    # Create df_publishers from df_games
    df_publishers = df_games[['steam_id', 'publisher', 'publisher_type']].copy()
    df_publishers["publisher"] = df_publishers["publisher"].astype(str).str.split(',')
    df_publishers["publisher_type"] = df_publishers["publisher_type"].astype(str).str.split(',')
    df_publishers = df_publishers.explode(column='publisher', ignore_index = True)
    df_publishers['publisher'] = df_publishers['publisher'].str.strip()
    df_publishers = df_publishers.explode(column='publisher_type', ignore_index = True)
    df_publishers['publisher_type'] = df_publishers['publisher_type'].str.strip()
    df_publishers['publisher'] = df_publishers['publisher'].apply(unidecode)
    df_publishers['publisher2'] = df_publishers['publisher'].str.upper()
    df_publishers = df_publishers.drop_duplicates(subset=['steam_id','publisher2'])
    df_publishers.drop(columns = 'publisher2', inplace = True)
   
    df_games.drop(["developer", "publisher", "publisher_type"], axis=1, inplace=True)
    
    # Create df_companies
    df_dev = df_developers.copy()
    df_pub = df_publishers.copy()
    df_dev.rename(columns = {'developer':'company_name'}, inplace = True)
    df_pub.rename(columns = {'publisher':'company_name'}, inplace = True)
    df_companies = pd.concat([df_dev,df_pub],ignore_index = True)
    df_companies.drop(["publisher_type", "steam_id"], axis=1, inplace=True)

    files_list = glob.glob('{}/Games5/*companies_url.json'.format(data_dir_path))
    df_companies_raw = pd.DataFrame()
    for file in files_list:
        data = json.load(open(file))
        df1 = pd.DataFrame(data['developers'])
        df2 = pd.DataFrame(data['publishers'])
        df = pd.concat([df1, df2], axis=0)
        df_companies_raw = pd.concat([df_companies_raw,df],ignore_index = True)
    df_comp = df_companies_raw.copy()
    
    df_comp.drop(["isPublisher", "isDeveloper", "id"], axis=1, inplace=True)
    df_comp = df_comp.drop_duplicates(subset=['name'])
    df_comp['slug'] = df_comp['slug'].replace('-', np.NaN)
    df_comp.rename(columns = {'name':'company_name'}, inplace = True)
    df_companies = pd.merge(df_companies, df_comp, how ='left', on =['company_name'])
    df_companies['company_name2'] = df_companies['company_name'].str.upper()
    df_companies = df_companies.drop_duplicates(subset=['company_name2'])
    df_companies.drop(["company_name2"], axis=1, inplace=True)
    
    return df_languages, df_genres, df_developers, df_publishers, df_games, df_companies
    
def create_df_meta(data_dir_path):
    """This function serves to create a dataframe from meta json files 

    Args:
        data_dir_path (str): The path directory where the raw data is stored

    Returns:
        Dataframe: Returns a dataframe with a cleaned data ready to load to db.
    """
    files_list = glob.glob('{}/Games5/*meta_url.json'.format(data_dir_path))
    #df_meta = pd.concat((pd.json_normalize(json.load(open(file))) for file in files_list), ignore_index=True)
    
    df_meta = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing metadata files... {round(((i+1)/len(files_list))*100, 2)}% complete                   ", end='\r')
        data = pd.json_normalize(json.load(open(file)))
        df_meta = pd.concat([df_meta,data],axis=0)
    
    df_meta.drop(["meta.releaseDateAlt", "name", "game_id"], axis=1, inplace=True)
    df_meta.rename(columns = {'meta.website':'website',
                              'meta.comingSoon':'comingSoon',
                              'meta.isReleased':'isReleased',
                              'meta.releaseDate':'releaseDate',
                              'meta.shortDescription':'shortDescription',
                              'meta.earliestReviewDate':'earliestReviewDate'}, inplace = True)
    return df_meta
    
    
def create_df_regionals(data_dir_path):
    """This function serves to create a dataframe from regionals json files 

    Args:
        data_dir_path (str): The path directory where the raw data is stored

    Returns:
        Dataframe: Returns a dataframe with a cleaned data ready to load to db.
    """
    files_list = glob.glob('{}/Games5/*regional_url.json'.format(data_dir_path))
    df_regionals = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing regionals files...  {round(((i+1)/len(files_list))*100, 2)}% complete                           ", end='\r')
    #    print(f"Processing regionals files.. {files_list.index(file)+1}/{len(files_list)}", end='\r')
        title = os.path.basename(file)
        steam_id = title.split('_')[0]
        data = json.load(open(file))
        if (list(data.keys())[0] == 'error'):
            continue
        df = pd.DataFrame(data['regions'])
        df.insert(0, 'steam_id', steam_id)
        df_regionals = pd.concat([df_regionals,df],axis=0, ignore_index = True)
    df_regionals.rename(columns = {'labels':'region', 'data':'playersPrct'}, inplace = True)
    
    return df_regionals

def create_df_subgenres(data_dir_path):
    """This function serves to create a dataframe from subgenres json files 

    Args:
        data_dir_path (str): The path directory where the raw data is stored

    Returns:
        Dataframe: Returns a dataframe with a cleaned data ready to load to db.
    """
    files_list = glob.glob('{}/Games5/*subgenre_url.json'.format(data_dir_path))
    df_subgenres = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing subgenres files... {round(((i+1)/len(files_list))*100, 2)}% complete                         ", end='\r')
        title = os.path.basename(file)
        steam_id = title.split('_')[0]
        data = pd.json_normalize(json.load(open(file)))
        data.insert(0, 'steam_id', steam_id)
        df_subgenres = pd.concat([df_subgenres,data],axis=0)
    
    return df_subgenres

def create_df_stats(data_dir_path):
    """This function serves to create a dataframe from stats and price json files 

    Args:
        data_dir_path (str): The path directory where the raw data is stored

    Returns:
        Dataframe: Returns a dataframe with a cleaned data ready to load to db.
    """
    files_list = glob.glob('{}/Games5/*stats_url.json'.format(data_dir_path))
    df_stats = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing stats files... {round(((i+1)/len(files_list))*100, 2)}% complete                               ", end='\r')
        title = os.path.basename(file)
        steam_id = title.split('_')[0]
        data = pd.json_normalize(json.load(open(file)))
        data.insert(0, 'steam_id', steam_id)
        df_stats = pd.concat([df_stats,data],axis=0)
        
    files_list = glob.glob('./data/Games5/*price_url.json')
    df_price = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing price files... {round(((i+1)/len(files_list))*100, 2)}% complete                               ", end='\r')        
        title = os.path.basename(file)
        steam_id = title.split('_')[0]
        data = pd.json_normalize(json.load(open(file)))
        data.insert(0, 'steam_id', steam_id)
        df_price = pd.concat([df_price,data],axis=0)
    
    df_price.drop(["isFree"], axis=1, inplace=True)
    df_stats = pd.merge(df_stats, df_price, how ='inner', on =['steam_id'])
    
    return df_stats    
    
def create_df_performances(data_dir_path):
    """This function serves to create a dataframe from performances json files 

    Args:
        data_dir_path (str): The path directory where the raw data is stored

    Returns:
        Dataframe: Returns a dataframe with a cleaned data ready to load to db.
    """
    files_list = glob.glob('{}/Games5/*performance_url.json'.format(data_dir_path))
    df_performances = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing performances files... {round(((i+1)/len(files_list))*100, 2)}% complete                               ", end='\r')
        title = os.path.basename(file)
        steam_id = title.split('_')[0]
        data = pd.json_normalize(json.load(open(file)), record_path = ['ranks'], meta = ['games'])
        data.insert(0, 'steam_id', steam_id)
        df_performances = pd.concat([df_performances,data], axis=0)
    df_performances.rename(columns = {'name':'perf_name', 'rank':'perf_rank', 'games':'nb_games'}, inplace = True)    
    
    return df_performances

def create_df_history(data_dir_path):
    """This function serves to create a dataframe from history json files 

    Args:
        data_dir_path (str): The path directory where the raw data is stored

    Returns:
        Dataframe: Returns a dataframe with a cleaned data ready to load to db.
    """
    '''files_list = glob.glob('{}/Games5/*history_url.json'.format(data_dir_path))
    df_history = pd.DataFrame()
    for i, file in enumerate(files_list):
        print(f"Processing history files... {round(((i+1)/len(files_list))*100, 2)}% complete", end='\r')
        title = os.path.basename(file)
        steam_id = title.split('_')[0]
        data = pd.json_normalize(json.load(open(file)))
        data.drop(['steam_id'], axis=1, inplace=True)
        data.insert(0, 'steam_id', steam_id)
        df_history = pd.concat([df_history,data],axis=0)
    df_history.to_csv('{}/history.csv'.format(data_dir_path), index=False)'''
    #df_history = pd.read_csv('{}/history.csv'.format(data_dir_path))
    df_history = pd.read_csv('./database//history.csv')

    return df_history
    
def load_to_db(df_name, table_name, table_schema, db_user, db_password, db_host, db_name):
    """This function allows to write records stored in a DataFrame to a SQL database

    Args:
        df_name (DataFrame): The dataframe that contanins the records to be loaded to db.
        table_name (str): The name of SQL table where the data will be written
        table_schema (str): Contains the name of columns in dataframe that match the attributes in SQL table
        user (str): Database user defined in config file.
        password (str): The password of the user to connect to db, defined in config file.
        host (str): IP address of the hostname, it defines the location of MySQL server and database.
        db_name (str): the name of the database, defined in config file.
    """
    
    print(f' Writing data to {table_name} table ......', end='\r')
       
    mysql_engine = create_engine(f'mysql://{db_user}:{db_password}@{db_host}/{db_name}')
    df_name.to_sql(table_name, mysql_engine, if_exists='replace', dtype = table_schema, index=False, chunksize=50000)
    
    print(f"Data written successfully to {table_name} table ({len(df_name.index)} rows inserted) !")

########################################################################################
