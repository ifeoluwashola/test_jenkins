# This Makefile includes instructions for environment setup, installation of dependencies from the requirements.txt file, and lint tests for Dockerfiles and Python source code.

# Set the name of the virtual environment
VIRTUALENV = ~/.dataprocessing
IMAGE_NAME = data-processing

# Define a target that creates a virtual environment and activates it
setup:
	# Create Python virtual environment
	python3 -m venv $(VIRTUALENV)
	# Activate the virtual environment
	. $(VIRTUALENV)/bin/activate

# Define a target that installs the project's dependencies and Hadolint
install:
	# Upgrade pip and install project dependencies from requirements.txt
	pip install --upgrade pip &&\
		pip install -r requirements.txt
	# Download and install Hadolint
	wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.16.3/hadolint-Linux-x86_64 &&\
		chmod +x /bin/hadolint

# Define a target that runs the linting tests for Dockerfile and app.py
lint:
	# Check the Dockerfile for linting issues using Hadolint
	hadolint --ignore DL3013 Dockerfile
	# Check the Python source code for linting issues using Pylint
	# Note that Pylint must be run from within the virtual environment
	. $(VIRTUALENV)/bin/activate && pylint --disable=R,C,W1203,W1202,W0401,W0614 main.py

# Define a target that builds the Docker image and tags it
build:
	# Build the Docker image with the specified name and tag
	docker build -t $(IMAGE_NAME) .

# Define a target that runs the Docker image and exposes port 8080
run:
	# List Docker images
	docker images
	# Start a container with the IMAGE_NAME image and expose port 8080
	docker run -d -p 8080:80 $(IMAGE_NAME)
# Define a target that runs all steps: setup, install, lint, build, and run
all: setup install lint build run