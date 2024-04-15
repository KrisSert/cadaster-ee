from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader, ConfigKey
import os
from google.cloud import storage
from datetime import datetime


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_exporter
def export_data_to_google_cloud_storage(csv_filepath: str, **kwargs):

    # get the gcp credentials path from mage config file.
    config_path = os.path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    config = ConfigFileLoader(config_path, config_profile)
    gsa_acc_key = config.get(ConfigKey.GOOGLE_SERVICE_ACC_KEY_FILEPATH)

    # Set the GCS application credentials environment variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gsa_acc_key

    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket_name = "cadaster_data_bucket"
    bucket = storage_client.bucket(bucket_name)

    blob_name = 'KATASTRIYKSUS.csv'
    blob = bucket.blob(blob_name)

    if blob.exists():
        print(f"The blob '{blob_name}' already exists in the bucket. Overwriting.")
    
    # Upload the CSV file to GCS
    with open(csv_filepath, 'rb') as file:
        blob.upload_from_file(file, timeout=1000)
        print(f"The blob '{blob_name}' uploaded successfully to the bucket.")

    return True