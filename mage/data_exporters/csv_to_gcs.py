from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_exporter
def export_data_to_google_cloud_storage(csv_filepath: str, **kwargs):

    print(f"filepath: {csv_filepath}")
    df = pd.read_csv(csv_filepath, sep=';', low_memory=False)
    print("dataframe read from csv")

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'mage-zoomcamp-kris-sert'
    object_key = 'test.csv'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )

    return True

