from dbt.cli.main import dbtRunner, dbtRunnerResult

try:
	# Initialize dbt
	dbt = dbtRunner()

	# Create CLI args as a list of strings
	cli_args = ["run"]

	# Run the command
	res: dbtRunnerResult = dbt.invoke(cli_args)

	print(res.result)
	
except Exception as e:
	# Handle the exception and return an error message or handle accordingly
	print(f"An error occurred: {str(e)}")
	print(res.result)
	