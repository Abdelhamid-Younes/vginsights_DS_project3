# vginsights_DS_project3
This project aims to create an ETL pipeline in order to load data (about 1GB) of video games with their statistics and their history performances.
We segmented and merged csv and json files into multiple tables and then brought everything back together in a clean, organized database using MYSQL and Pandas.

The raw data is sourced from : https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/VG_Insights.7z

## ERD:
Our first goal was to visualize the database we were creating by generating an ERD diagram using www.quickdatabasediagrams.com. Once generated we decided on a relational database as we would be able to connect multiple tables based on steam_id.

![VGI_DB](https://user-images.githubusercontent.com/114106183/220757184-e5f107df-410d-4e8a-8243-c901a0f99217.png)

## Workflow :

- Extract :
   Download a zip file containing the data of the project and unzip it in a defined folder (download_extract.py script).
  
- Transform :
  - Create dataframes with raw data from json files
  - 

- Load :
