import io
import os
import requests
import shutil
import zipfile

def download_and_extract(url):
    # Download the source file .zip and extract the content
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the DBF file content into memory
        with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
            dbf_files = [name for name in zip_ref.namelist() if name.endswith('.dbf')]
            if dbf_files:
                dbf_file_name = dbf_files[0]
                dbf_file_content = zip_ref.read(dbf_file_name)
                print("Download and extraction successful.")
                return dbf_file_content
            else:
                print("No .dbf file found in the zip archive.")
    else:
        print("Failed to download the file.")
    return None

def load_data_from_api():

    url = 'https://geoportaal.maaamet.ee/docs/katastripiirid/paev/KATASTER_EESTI_SHP.zip'

    dbf_file_content = download_and_extract(url)

    if dbf_file_content is not None:
        return dbf_file_content


load_data_from_api()
print("success")