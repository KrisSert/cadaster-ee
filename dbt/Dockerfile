# Use an official Python runtime as the base image
FROM ghcr.io/dbt-labs/dbt-bigquery:1.4.latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /dbt

# Copy dbt project files
COPY . .

# Expose any necessary ports
# (Not needed for dbt, but included for completeness)
EXPOSE 80

# Define the command to run dbt
CMD ["dbt"]
