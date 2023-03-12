import streamlit as st

st.set_page_config(
    page_title="VGI Project",
    page_icon="📰",
)


st.write("# Video games insights Project")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This data engineering project aims at using the the site vginsights.com to find data, transform and store it,
    and then display insights and some statictics about video games.
    This is the final project for the Data Engineering course at [Datascientest](https://datascientest.com/formation-data-engineer).
    ### Tech Stack
    - Python to extract, transform and load data.
    - MYSQL to store the video games data
    - Streamlit for the dashboards
    ### Contributors :
    - [Abdelhamid YOUNES](https://https://github.com/Abdelhamid-Younes)

"""
)