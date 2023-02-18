from urllib.request import urlopen
import py7zr
import os
# Download and extract data

save_as = 'VG_Insights.7z'
url = 'https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/VG_Insights.7z'


def download_data():

    path = "./data"
    os.mkdir( path, 0o755 );

    with urlopen(url) as file:
        content = file.read()
 
    with open(save_as, 'wb') as download:
        download.write(content)
        
        
def extract_data():
    with py7zr.SevenZipFile(save_as, 'r') as archive:
        archive.extractall(path='./data')
        
###########################################################################

download_data()
extract_data()