import streamlit as st
#import matplotlib.pyplot as plt
import mysql.connector
import io
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', True)
# Initializing connection.
conn = mysql.connector.connect(**st.secrets["mysql"])

st.set_page_config(
    page_title="VGI Project",
    page_icon="📰",
)

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()



    
# Samples data from views tables.
st.markdown('## Raw data:')
st.write("Here is some raw data samples displayed from views tables : ")

# Samples data from views tables.
st.markdown('### From game_overview view :')
sql = sql ="SELECT * FROM game_overview LIMIT 20"
result = run_query(sql)
df = pd.DataFrame(result, columns=['steam_id','game_name', 'Developers', 'Publishers', 'Release Date', 'Current Price', 'Avg_6_months', 'Genres', 'Languages', 'Description', 'Url_link'])
df = df.set_index(['steam_id'])
st.dataframe(df)