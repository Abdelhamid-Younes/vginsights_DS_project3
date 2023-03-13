import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


pd.set_option('display.max_columns', True)

# Initializing connection.
conn = mysql.connector.connect(**st.secrets["mysql"])

st.set_page_config(
    page_title="VGI Project",
    page_icon="📰",
)


def max_width():
    max_width_str = "max-width:800px;"
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



st.write("### Steam Games Top Charts")

choice = st.selectbox(
    'Top Games By :',
    ('Gross revenue', 'New reviews', 'New followers'))

fig, ax = plt.subplots(figsize=(12, 4))
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)
plt.xticks(rotation = 30, ha="right")
plt.grid(axis='y')


if choice == 'Gross revenue':
    
    #create plot
    df = pd.read_sql("SELECT * FROM top_games_revenue",conn)
    df['revenue_vgi'] = df['revenue_vgi'].apply(lambda x:x/1000000)

    ax.set_ylabel("Value in $")
    ax.set_xlabel("Games")
    ax.set_title("Top Games Last Week by Gross Revenue")
    plt.bar(df.game_name, df.revenue_vgi, color='green')
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%dm'))
    st.pyplot(fig)
    st.dataframe(df)
  
elif choice == 'New reviews':
    
    #create plot
    df = pd.read_sql("SELECT * FROM top_games_reviews",conn)

    plt.bar(df.game_name, df.total_reviews, color='green')
    ax.set_ylabel("Niew Reviews")
    ax.set_xlabel("Games")
    ax.set_title("Top Games Last Week by New Reviews")
    st.pyplot(fig)
    st.dataframe(df)

elif choice == 'New followers':
    
    #create plot
    df = pd.read_sql("SELECT * FROM top_games_followers",conn)
    plt.bar(df.game_name, df.total_members, color='green')
    ax.set_ylabel("Niew Followers")
    ax.set_xlabel("Games")
    ax.set_title("Top Games Last Week by Niew Followers")
    st.pyplot(fig)
    st.dataframe(df)