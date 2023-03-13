from urllib.request import urlopen
import py7zr
from tqdm import tqdm
import os


def download_data(data_dir_path, url, save_as):
    """This function allows to download a zip folder containing the data of the project, from this url:
    "https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/VG_Insights.7z"

    Args:
        data_dir_path (str): The path directory where the zip folder will be stored
        url (str): The web address from where the data is received
        save_as (str): The path to the zipped folder
    """

    os.mkdir( data_dir_path, 0o755 );

    with urlopen(url) as file:
        content = file.read()
 
    with open(save_as, 'wb') as download:
        download.write(content)
        
        
def extract_data(save_as, data_dir_path):
    """This function allows to unzip the folder contaning project's data and save it in a defined loaction.

    Args:
        save_as (str): the name and the path to the zipped folder 
        data_dir_path (str): the path where the unzipped folder will be stored.
    """
    with py7zr.SevenZipFile(save_as, 'r') as archive:
        archive.extractall(data_dir_path)
        
###########################################################################