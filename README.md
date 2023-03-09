# Pipeline for Data Processing


This repository contains a data processing pipeline that runs inside a Docker container.
The pipeline is written in Python and consists of the following components:


main.py is the main Python script that handles data processing.

requirements.txt: a list of Python packages that the main.py script requires.

Dockerfile: a Dockerfile that defines the Docker image that will be used to run the data processing pipeline.


The pipeline can be run locally using make commands or on a continuous integration (CI) platform like Jenkins. 


----------------------------------------------------------------------------

## Execution at the local level


To run the pipeline locally, perform the following steps:


Install Python 3.9 and then run make.

Clone the repository: git clone https://github.com/<username>/<repository>.git.


#### Go to the cloned repository:

Navigate to the repository directory: cd <repository>.

#### Make and activate a Python virtual environment:

python3 -m venv venv && . venv/bin/activate

#### Install the project's dependencies and Hadolint with the command: 
make install

#### check for Linting issues in the Dockerfile and Python source code:
make lint.

#### Create the Docker image:
make build

#### Create the Docker image:
make run

----------------------------------------------------------------------------
## Pipeline Jenkins

The pipeline can also be run on the Jenkins Continuous Integration platform.
Here are the steps for configuring the pipeline on Jenkins:


Make a fresh Jenkins pipeline job.

Select "Pipeline script from SCM" in the "Pipeline" section and enter the Git repository URL and the appropriate branch.

Select "Delete workspace before build starts" in the "Build Environment" section to ensure a clean workspace for each build.

The job configuration should be saved.

Start the pipeline.


The following steps will be carried out by the pipeline:


Check out the Git repository for the source code.

Make and activate a Python virtual environment.

Install Hadolint and the project's dependencies.

Linting errors should be found in the Dockerfile and Python source code.

Create the Docker image.

Execute the Docker container. 

### Prerequisites

To run the data processing pipeline, the following prerequisites must be met:
-    Python 3.9
-    make
-    Docker
You will also need access to a Jenkins instance and permission to create and run Jenkins pipelines to run the pipeline on a Jenkins CI platform. 


## Usage

Note that the pipeline assumes that your Python code is in a file called main.py, and that your Dockerfile is in the root directory of your project. If your files are named differently or located in a different directory, you will need to modify the pipeline accordingly.

If you are running the pipeline on a Jenkins CI platform, you will need to copy the Jenkinsfile into the root directory of your project, modify it if necessary, and create a new pipeline job on your Jenkins instance pointing to the Jenkinsfile. You can then trigger the pipeline manually or set up automatic triggers using a webhook.



## Author

This data processing pipeline was created by [Name]. Feel free to contact me at [your email] if you have any questions or comments.

## License

Cisco Systems, Inc End User License Agreement 2020.


