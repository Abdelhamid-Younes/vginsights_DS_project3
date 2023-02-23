# vginsights_DS_project3
This project aims to create an ETL pipeline in order to load data (about 1GB) of video games with their statistics and their history performances.
We segmented and merged csv and json files into multiple dataframes and then brought everything back together in a clean and organized database using MYSQL and Pandas.

The raw data is sourced from : https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/VG_Insights.7z

## ERD:
Our first goal was to visualize the database we were creating by generating an ERD diagram using www.quickdatabasediagrams.com. Once generated we decided on a relational database as we would be able to connect multiple tables based on steam_id.

![VGI_DB](https://user-images.githubusercontent.com/114106183/220757184-e5f107df-410d-4e8a-8243-c901a0f99217.png)

## Workflow :

- Extract :
   - Downloading a zip file containing the data of the project and unziping it in a defined folder (script : download_extract.py).
  
- Transform : In this phase we built a cleaned dataframes in order to export it to different tables. It involves the following steps: 
  - Creating dataframes with raw data from json files.
  - Dropping unnecessary columns in dataframes.
  - Adding and renaming other columns to a more recognizable set of labels.
  - Tidying up Fields to get a better understanding of the data.
  - Using .str() methods to clean columns.
  - Rebuilding Missing Data.
  - Saving the complete data to csv files.

- Load : After the data was cleaned, and merged, we have created a MYSQL Database, and  data was successfully uploaded into different tables by using sqlaclhemy.
