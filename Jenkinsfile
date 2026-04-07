pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose-jenkins.yml'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository from GitHub...'
                git branch: 'main',
                    url: 'https://github.com/poiboiq/sms-app.git'
            }
        }

        stage('Stop Previous Containers') {
            steps {
                echo 'Stopping any previously running containers...'
                sh 'docker-compose -f ${COMPOSE_FILE} down || true'
            }
        }

        stage('Build and Deploy') {
            steps {
                echo 'Building and deploying containerized application...'
                sh 'docker-compose -f ${COMPOSE_FILE} up -d --build'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Waiting for containers to be ready...'
                sh 'sleep 15'
                sh 'docker ps'
                echo 'Deployment successful!'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! SMS app is running.'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
            sh 'docker-compose -f ${COMPOSE_FILE} logs || true'
        }
    }
}
