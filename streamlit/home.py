import streamlit as st

st.set_page_config(
    page_title="VGI Project",
    page_icon="📰",
)

centered_container = st.container()
col1, col2, col3 = centered_container.columns([1,2,1])
col1.write("")
# Add the image to the second column
col2.image("./images/VGI_logo.png", width=300)
col3.write("")

st.write("# Video games insights Project")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This data engineering project aims at using the site vginsights.com to find data, transform and store it,
    and then display insights and some statictics about video games.
    This is the final project for the Data Engineering course at [Datascientest](https://datascientest.com/formation-data-engineer).
    ### Tech Stack
    - Python and pandas to extract, transform and load data.
    - MYSQL to store the video games data
    - Streamlit for the dashboard
    ### Contributors :
    - [Abdelhamid YOUNES](https://https://github.com/Abdelhamid-Younes)

"""
)