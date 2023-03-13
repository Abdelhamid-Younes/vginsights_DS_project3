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



df_publishers = pd.read_sql("SELECT * FROM publisher_stats",conn)
df_publishers = df_publishers.sort_values('Total Lifetime Revenue', ascending=False)
publisher_name = df_publishers['Publisher name'].drop_duplicates()

publisher_selected = st.sidebar.selectbox('Select a publisher:', publisher_name)
publisher_selected_df = df_publishers.loc[df_publishers["Publisher name"] == publisher_selected]

df_genre_selected = pd.read_sql(f'''SELECT genres.genre, COUNT(*) AS count_genre
                           FROM games
                           JOIN publishers ON games.steam_id = publishers.steam_id
                           JOIN genres ON games.steam_id = genres.steam_id
                           WHERE publishers.publisher = '%s'
                           GROUP BY genres.genre;''' % publisher_selected,conn)

df_games_pub = pd.read_sql(f'''SELECT games.game_name, games.release_date, games.price, games.rating, games.reviews, games.rank_reviews, games.revenue_vgi
                                    FROM games
                                    JOIN publishers ON games.steam_id = publishers.steam_id
                                    WHERE publishers.publisher = '%s';''' % publisher_selected,conn)

st.title(f"Publisher : {publisher_selected}")
text = f'''<hr>'''
st.markdown(text,unsafe_allow_html=True)

def my_autopct(pct):
    return '{:.1f}%'.format(pct) if pct >= 2 else ''

columns = st.columns((1, 1))

with columns[0]:
    st.markdown(f"#### Overview of {publisher_selected}")
    st.write("**Name :** " , publisher_selected_df['Publisher name'].iloc[0])
    st.write("**Published games :** " , str(publisher_selected_df['Published Games'].iloc[0]))
    st.write("**First Game published :** " , str(publisher_selected_df['First Game published'].iloc[0]))
    st.write("**Last Game published :** " , str(publisher_selected_df['Last Game published'].iloc[0]))
    publisher_selected_df['Total Lifetime Revenue'] = publisher_selected_df.apply(lambda row: '$' + str(round(row['Total Lifetime Revenue'] / 1000000,2)) + 'm', axis=1)
    st.write("**Total Lifetime Revenue :** " , publisher_selected_df['Total Lifetime Revenue'].iloc[0])
    publisher_selected_df['Average Revenue per Game'] = publisher_selected_df.apply(lambda row: '$' + str(round(row['Average Revenue per Game'] / 1000000,2)) + 'm', axis=1)
    st.write("**Average Revenue per Game :** " , publisher_selected_df['Average Revenue per Game'].iloc[0])
    st.write("**Publisher type :** " , publisher_selected_df['Publisher type'].iloc[0])

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
    st.markdown(f"#### All Steam games published by {publisher_selected}")
    df_games_pub.index.name='#'
    st.write(df_games_pub)
    