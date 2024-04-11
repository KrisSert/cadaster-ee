import io
import os
import requests
import shutil
import zipfile

import pandas as pd
from dbfread import DBF


def download_and_extract(url):
    # download the source file .zip and extract the content
    response = requests.get(url)

    if response.status_code == 200:
        # Create a temporary directory to extract files
        extraction_path = "./downloaded_files"
        os.makedirs(extraction_path, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
            zip_ref.extractall(extraction_path)
        print("Download and extraction successful.")
    else:
        print("Failed to download the file.")

    return extraction_path


def load_data_from_api():
    """
    Template for loading data from API
    """
    url = 'https://geoportaal.maaamet.ee/docs/katastripiirid/paev/KATASTER_EESTI_SHP.zip'
    src_filename = 'SHP_KATASTRIYKSUS.dbf'
    src_file_encoding = 'utf-8'
    

    dsf_file_root_path = download_and_extract(url)
    dsf_file_path = f'{dsf_file_root_path}/{src_filename}'

    dbf = DBF(dsf_file_path, encoding='utf-8')
    df = pd.DataFrame(iter(dbf))

    if df is not None:
        print(df.head())  # Display the first few rows of the DataFrame

    # remove the downloaded dir with files.
    shutil.rmtree(dsf_file_root_path)

    return df

load_data_from_api()