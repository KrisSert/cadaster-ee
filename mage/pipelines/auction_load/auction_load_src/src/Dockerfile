FROM python:3.12

# Install dependencies
# RUN apt-get install wget
RUN pip install psycopg2-binary sqlalchemy
RUN pip install requests tqdm pandas pyarrow


# Set the working directory inside the container
WORKDIR /app

COPY . .

# Add the script's directories to the PATH
RUN echo 'export PATH="/app:$PATH"' >> ~/.bashrc
RUN chmod +x *.py

# enter bash shell, keeps the container running...
CMD ["bash"]