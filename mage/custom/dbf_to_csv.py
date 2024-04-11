if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



@custom
def transform_custom(*args, **kwargs):
    
    print('Proceeding to convert .dbf to pandas dataframe...')
    dbf = DBF(dsf_file_path, encoding=src_file_encoding)
    df = pd.DataFrame(iter(dbf))

    if df is not None:
        print(df.head())  # Display the first few rows of the DataFrame

    # remove the downloaded dir with files.
    shutil.rmtree(dsf_file_root_path)

    return df

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
