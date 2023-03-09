# This Makefile includes instructions for environment setup, installation of dependencies from the requirements.txt file, and lint tests for Dockerfiles and Python source code.

# Define a variable for the virtual environment name
ifndef VIRTUALENV
    $(error VIRTUALENV is not set)
endif

# Define a variable for the Docker image name
ifndef DOCKER_IMAGE_NAME
    $(error DOCKER_IMAGE_NAME is not set)
endif

# Define a variable for the Docker image tag
ifndef DOCKER_IMAGE_TAG
    $(error DOCKER_IMAGE_TAG is not set)
endif

# Define a variable for the Docker Hub username
ifndef DOCKER_HUB_USERNAME
    $(error DOCKER_HUB_USERNAME is not set)
endif

# Define a variable for the Docker Hub password
ifndef DOCKER_HUB_PASSWORD
    $(error DOCKER_HUB_PASSWORD is not set)
endif

# Define a target that creates a virtual environment and activates it
.PHONY: install-venv
install-venv:
	# Create Python virtual environment
	python3 -m venv $(VIRTUALENV)
	# Activate the virtual environment
	. $(VIRTUALENV)/bin/activate

# Define a target that installs the project's dependencies and Hadolint
.PHONY: install-deps
install-deps:
	# Upgrade pip and install project dependencies from requirements.txt
	pip install --upgrade pip && \
	pip install -r requirements.txt

.PHONY: install-hadolint
install-hadolint:
	wget -O hadolint https://github.com/hadolint/hadolint/releases/download/v2.7.0/hadolint-Linux-x86_64
	chmod +x hadolint

# Define a target that checks the Dockerfile for linting issues using Hadolint
.PHONY: lint-docker
lint-docker: 
	/usr/local/bin/hadolint --ignore DL3013 Dockerfile

# Define a target that checks the Python source code for linting issues using Pylint
.PHONY: lint-python
lint-python:
	# Note that Pylint must be run from within the virtual environment
	# pip install pylint
	. $(VIRTUALENV)/bin/activate && pip install pylint\
       	pylint --disable=R,C,W1203,W1202 main.py

# Define a target that builds the Docker image and tags it
.PHONY: build-image
build-image: lint-docker lint-python
	docker build -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) .

# Define a target that runs the Docker image
.PHONY: run-image
run-image:
	docker run -p 8000:8000 $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)

# Define a target that logs in to Docker Hub and pushes the Docker image
.PHONY: push-image
push-image:
	docker login -u $(DOCKER_HUB_USERNAME) -p $(DOCKER_HUB_PASSWORD)
	docker push $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)

# Define a target that runs all steps: setup, install, lint, build, and run
.PHONY: all
all: install-venv install-deps install-hadolint lint-docker lint-python build-image run-image push-image

