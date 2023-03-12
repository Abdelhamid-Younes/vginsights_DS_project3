import streamlit as st
import matplotlib.pyplot as plt
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
def max_width():
    max_width_str = "max-width:900px;"
    st.markdown(
        f"""
    <style>
    .block-container {{
        {max_width_str}
        }}
    <style>
    """,
        unsafe_allow_html=True,
    )
    
max_width()

df_games = pd.read_sql("SELECT * FROM game_overview",conn)
steam_id_df = pd.read_sql(f"SELECT DISTINCT steam_id FROM regionals",conn)
df_games = pd.merge(df_games, steam_id_df, how ='inner', on =['steam_id'])
df_games = df_games.sort_values('steam_id', ascending=True)
game_name = df_games['game_name'].drop_duplicates()

df_game_stats = pd.read_sql("SELECT * FROM game_stats",conn)
df_game_stats = pd.merge(df_game_stats, steam_id_df, how ='inner', on =['steam_id'])

game_selected = st.sidebar.selectbox('Select a game:', game_name)

game_selected_df = df_games.loc[df_games["game_name"] == game_selected]
stats_selected_df = df_game_stats.loc[df_games["game_name"] == game_selected]

id = df_games['steam_id'].loc[df_games["game_name"] == game_selected].iloc[0]

df_regionals = pd.read_sql(f"SELECT * FROM regionals WHERE steam_id = {id} ",conn)

df_performances = pd.read_sql(f"SELECT * FROM performances WHERE steam_id = {id} ",conn)

text = f'''<hr>'''
st.title(f"{game_selected} - Steam stats")
st.markdown(text,unsafe_allow_html=True)

    
columns = st.columns((1, 1))

with columns[0]:
    st.subheader(f"Game overview")
    st.write("**Developers:** " , game_selected_df['Developers'].iloc[0])
    st.write("**Publishers**: " , game_selected_df['Publishers'].iloc[0])
    st.write("**Release Date:** " , str(game_selected_df['Release Date'].iloc[0]))
    st.write("**Current price:**  $" , str(game_selected_df['Current Price'].iloc[0]))
    st.write("**Avg price during last 6 months:** " , '$',str(game_selected_df['Avg Price during last 6 months'].iloc[0]))
    st.write("**Genres:** " , game_selected_df['Genres'].iloc[0])
    st.write("**Languages:** " , game_selected_df['Languages'].iloc[0])
    #st.write("**Description:** " , game_selected_df['Description'].iloc[0])
    st.write("**Steam link:** " , game_selected_df['Game URL Link'].iloc[0])

with columns[1]:
    st.subheader(f"Player Insights - Players by Region")
    if (df_regionals.empty):
        st.write("This information is not available")
    else:
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.patch.set_facecolor('beige')
        plt.pie(df_regionals.playersPrct, labels=df_regionals.region, autopct='%1.1f%%', wedgeprops=dict(width=0.5), textprops={'fontsize': 11}, labeldistance=None, startangle=90)
        plt.legend(loc="best")
        st.pyplot(fig)


columns2 = st.columns((1, 1), gap="medium")

with columns2[0]:
    st.subheader(f"Quick stats")
    st.write("**Active player** (latest players) : " , str(stats_selected_df['players_latest'].iloc[0]))
    st.write("**Active player** (24h peak) : " , str(stats_selected_df['max_players_24h'].iloc[0]))
    st.write("**Positive reviews**  : " , str(stats_selected_df['reviews_positive'].iloc[0]))
    stats_selected_df['revenue_vgi'] = stats_selected_df.apply(lambda row: '$' + str(round(row['revenue_vgi'] / 1000000,2)) + 'm', axis=1)
    st.write("**Gross revenue**  : " , str(stats_selected_df['revenue_vgi'].iloc[0]))
    stats_selected_df['units_sold_vgi'] = stats_selected_df.apply(lambda row: '$' + str(round(row['units_sold_vgi'] / 1000000,2)) + 'm', axis=1)
    st.write("**Units sold** : " , str(stats_selected_df['units_sold_vgi'].iloc[0]))
    st.write("**Avg play time (hour)** : " , str(stats_selected_df['avg_playtime'].iloc[0]))
    st.write("**Median play time (hour)** : " , str(stats_selected_df['med_playtime'].iloc[0]))
        
with columns2[1]:
    st.subheader(f"Performance and critical acclaim")
    df_performances.rename(columns = {"perf_name": "Performance", "perf_rank":"Rank","prct":"Top rate" }, inplace=True)
    df_performances["Rank"] = df_performances['Rank'].astype(str) +" / " + df_performances["nb_games"].astype(str)
    df_performances["Top rate"] = df_performances["Top rate"].astype(str) +  " %"
    df_performances.drop(columns=['steam_id', 'nb_games'], inplace=True)
    df_performances.style.set_properties(subset=['text'], **{'width': '300px'})
    st.dataframe(df_performances)