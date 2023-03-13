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
    max_width_str = "max-width:1000px;"
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

df_developers = pd.read_sql("SELECT * FROM developer_stats",conn)
df_developers = df_developers.sort_values('Total Lifetime Revenue', ascending=False)
developer_name = df_developers['Developer name'].drop_duplicates()

developer_selected = st.sidebar.selectbox('Select a developer:', developer_name)
developer_selected_df = df_developers.loc[df_developers["Developer name"] == developer_selected]

df_genre_selected = pd.read_sql(f'''SELECT genres.genre, COUNT(*) AS count_genre
                           FROM games
                           JOIN developers ON games.steam_id = developers.steam_id
                           JOIN genres ON games.steam_id = genres.steam_id
                           WHERE developers.developer = '%s'
                           GROUP BY genres.genre;''' % developer_selected,conn)

df_games_dev = pd.read_sql(f'''SELECT games.game_name, games.release_date, games.price, games.rating, games.reviews, games.rank_reviews, games.revenue_vgi
                                    FROM games
                                    JOIN developers ON games.steam_id = developers.steam_id
                                    WHERE developers.developer = '%s';''' % developer_selected,conn)

#st.write(df_genre_selected)

st.title(f"Developer : {developer_selected}")
text = f'''<hr>'''
st.markdown(text,unsafe_allow_html=True)

def my_autopct(pct):
    return '{:.1f}%'.format(pct) if pct >= 2 else ''

columns = st.columns((1, 1))

with columns[0]:
    st.markdown(f"#### Overview of {developer_selected}")
    st.write("**Name :** " , developer_selected_df['Developer name'].iloc[0])
    st.write("**Developed games :** " , str(developer_selected_df['Developed Games'].iloc[0]))
    st.write("**First Game developed :** " , str(developer_selected_df['First Game Developed'].iloc[0]))
    st.write("**Last Game developed :** " , str(developer_selected_df['Last Game Developed'].iloc[0]))
    developer_selected_df['Total Lifetime Revenue'] = developer_selected_df.apply(lambda row: '$' + str(round(row['Total Lifetime Revenue'] / 1000000,2)) + 'm', axis=1)
    st.write("**Total Lifetime Revenue :** " , developer_selected_df['Total Lifetime Revenue'].iloc[0])
    developer_selected_df['Average Revenue per Game'] = developer_selected_df.apply(lambda row: '$' + str(round(row['Average Revenue per Game'] / 1000000,2)) + 'm', axis=1)
    st.write("**Average Revenue per Game :** " , developer_selected_df['Average Revenue per Game'].iloc[0])
    

with columns[1]:
    st.markdown("#### Genre Distribution")
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('beige')
    plt.pie(df_genre_selected.count_genre, labels=df_genre_selected.genre, autopct=my_autopct, wedgeprops=dict(width=0.5), textprops={'fontsize': 11}, labeldistance=None, startangle=90)
    plt.legend(loc="best")
    st.pyplot(fig)
    
st.markdown("---")

container = st.container()

with container:
    st.markdown(f"#### All Steam games developed by {developer_selected}")
    df_games_dev.index.name='#'
    st.write(df_games_dev)
    