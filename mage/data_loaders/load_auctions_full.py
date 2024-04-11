import io
import pandas as pd
import requests
import json

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_auctions_full(*args, **kwargs):
    """
    Template for loading data from API
    """

    size = 3

    url = f'https://andmed.stat.ee/api/v1/et/stat/RLV003'
    response = requests.get(url).json()

    return pd.read_json(response.text)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
