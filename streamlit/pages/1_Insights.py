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

choice = st.sidebar.selectbox(
    'Top Games By :',
    ('New reviews', 'Gross revenue', 'New followers'))

if choice == 'Gross revenue':
    
    #create plot
    df = pd.read_sql("SELECT * FROM top_games_revenue",conn)
    
    st.dataframe(df)
    
elif choice == 'New followers':
    
    #create plot
    dff = pd.read_sql("SELECT * FROM top_games_followers",conn)
    
    st.dataframe(dff)

#st.pyplot(df.plot.bar(x='game_name', y='revenue_vgi',color='green', figsize=(10, 10)).figure)
