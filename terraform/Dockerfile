FROM hashicorp/terraform:latest

# Set the working directory
WORKDIR /app

COPY . .


# Run Terraform init and apply commands
RUN terraform init
RUN terraform apply -auto-approve

# Keep the container running indefinitely
CMD ["sleep", "86400"]