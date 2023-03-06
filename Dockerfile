# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Add maintainer label
LABEL maintainer=""

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt ./

# Install required packages using pip
RUN pip install --upgrade --no-cache-dir pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Expose port 80 to allow outside traffic to connect to the container
EXPOSE 80

# Set the command to run when the container starts
CMD ["python", "main.py"]
