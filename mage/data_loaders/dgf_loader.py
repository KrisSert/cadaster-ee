import io
import os
import requests
import shutil
import zipfile

import pandas as pd
from dbfread import DBF


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def download_and_extract_from_api(*args, **kwargs):
    """
    shema details:
    https://geoportaal.maaamet.ee/est/ruumiandmed/maakatastri-andmed/katastriuksuste-allalaadimine-p592.html
    """
    
    url = 'https://geoportaal.maaamet.ee/docs/katastripiirid/paev/KATASTER_EESTI_SHP.zip'
    src_filename = 'SHP_KATASTRIYKSUS.dbf'
    src_file_encoding = 'utf-8'
    
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

    return f'{extraction_path}/{src_filename}'
    # returns: path of dbf file


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
