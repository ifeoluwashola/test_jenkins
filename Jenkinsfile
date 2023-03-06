def notifyStart() {
    echo "Starting stage: ${env.STAGE_NAME}"
}

def notifySuccess() {
    echo "Stage ${env.STAGE_NAME} succeeded!"
}

def notifyFailure() {
    echo "Stage ${env.STAGE_NAME} failed!"
}

pipeline {
    agent any
    environment {
        DOCKER_IMAGE_NAME = 'your-docker-hub-username/your-image-name'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_HUB_USERNAME = 'your-docker-hub-username'
        DOCKER_HUB_PASSWORD = 'your-docker-hub-password'
        VIRTUALENV = 'name-of-env'
    }

    stages {
        stage ('Install virtual environment') {
            steps {
                script {
                    notifyStart()
                    sh 'make install-venv VIRTUALENV="${VIRTUALENV}"'
                    notifySuccess()
                }
            }
        }

        stage ('Install dependencies') {
            steps {
                script {
                    notifyStart()
                    sh 'make install-deps'
                    notifySuccess()
                }
            }
        }

        stage ('Install Hadolint') {
            steps {
                script {
                    notifyStart()
                    sh 'make install-hadolint'
                    notifySuccess()
                }
            }
        }

        stage ('Lint Dockerfile') {
            steps {
                script {
                    notifyStart()
                    sh 'make lint-docker'
                    notifySuccess()
                }
            }
        }

        stage ('Lint Python code') {
            steps {
                script {
                    notifyStart()
                    sh 'make lint-python VIRTUALENV="${VIRTUALENV}"'
                    notifySuccess()
                }
            }
        }

        stage ('Build image') {
            steps {
                script {
                    notifyStart()
                    sh 'make build-image DOCKER_IMAGE_NAME="${DOCKER_IMAGE_NAME}" DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG}"'
                    notifySuccess()
                }
            }
        }

        stage ('Run image') {
            steps {
                script {
                    notifyStart()
                    sh 'make run-image DOCKER_IMAGE_NAME="${DOCKER_IMAGE_NAME}" DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG}"'
                    notifySuccess()
                }
            }
        }

        stage ('Push image') {
            steps {
                script {
                    notifyStart()
                    sh 'make push-image DOCKER_IMAGE_NAME="${DOCKER_IMAGE_NAME}" DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG}" DOCKER_HUB_USERNAME="${DOCKER_HUB_USERNAME}" DOCKER_HUB_PASSWORD="${DOCKER_HUB_PASSWORD}"'
                    notifySuccess()
                }
            }
        }
    }

    post {
        always {
            // Notification in case of build failure or success
            script {
                if (currentBuild.result == "SUCCESS") {
                    notifySuccess()
                } else {
                    notifyFailure()
                }
            }
        }
    }
}

