pipeline {
  agent {
        docker {
            image 'python:3.9-slim-buster'
        }
    }
  stages {
    stage('Check code') {
      steps {
        checkout()
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          make install
          make lint
        '''
      }
    }
    stage('Build and push Docker image') {
      steps {
        checkout()
        sh '''
          make build
          make run
        '''
      }
    }
  }
}

