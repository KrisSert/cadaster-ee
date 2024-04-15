from dbt.cli.main import dbtRunner, dbtRunnerResult
import os
import nest_asyncio


if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):

    nest_asyncio.apply()
    original_path = os.getcwd()
    
    try:
        # dbt command has to be run from dbt folder
        os.chdir("/home/src/mage/dbt")

        # Initialize dbt
        dbt = dbtRunner()
        
        # Create CLI args as a list of strings
        cli_args = ["run-operation", "stage_external_sources", "--vars", "ext_full_refresh: true"]
        
        # Run the command
        res: dbtRunnerResult = dbt.invoke(cli_args)
        
        # Return the result
        return {res.result}

    except Exception as e:
        # Handle the exception and return an error message or handle accordingly
        print(f"An error occurred: {str(e)}")
        return {"status": "error"}

    finally:
        # Revert back to the original working directory
        os.chdir(original_path)

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
