from urllib.request import urlopen
import py7zr
import os


def download_data(data_dir_path, url, save_as):

    os.mkdir( data_dir_path, 0o755 );

    with urlopen(url) as file:
        content = file.read()
 
    with open(save_as, 'wb') as download:
        download.write(content)
        
        
def extract_data(save_as, data_dir_path):
    with py7zr.SevenZipFile(save_as, 'r') as archive:
        archive.extractall(data_dir_path)
        
###########################################################################