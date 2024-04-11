import os
import pandas as pd
from dbfread import DBF

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def dbf_to_df(dbf_filepath: str, *args, **kwargs):
    dbf_file_encoding = 'utf-8'

    dbf = DBF(dbf_file, encoding=dbf_file_encoding)
    # Convert the DBF data to a DataFrame
    df = pd.DataFrame(iter(dbf))
    
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
