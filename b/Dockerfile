# Use the official Python image, which is based on Debian
FROM python:3.10

# Set the working directory in the container
WORKDIR /code

# Copy the Python dependency files to the container
COPY pyproject.toml poetry.lock /code/

# Install Poetry for Python dependency management
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Install LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice

# Copy the rest of your application's code to the container
COPY . /code

# Copy your Google Cloud credentials file to the container
COPY proyecto-desarrollo-cloud.json /code/proyecto-desarrollo-cloud.json

# Set the environment variable for Google Cloud authentication
ENV GOOGLE_APPLICATION_CREDENTIALS=/code/proyecto-desarrollo-cloud.json

# Expose port 8000 for your application
EXPOSE 8000

# Command to run your application using Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]