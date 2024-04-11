import shutil

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(completed: bool, *args, **kwargs):
    if completed:
        try:
            # Delete the folder and all its contents
            shutil.rmtree("./downloaded_files")
            return True
        except Exception as e:
            print(f"Error occurred while deleting the folder: {e}")
            return False
    else:
        # Throw an error if the task is not completed
        raise ValueError("The clean_downloaded_files task was not completed successfully.")
        


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
