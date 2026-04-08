pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/poiboiq/sms-app.git'
            }
        }
        stage('Stop Previous Containers') {
            steps {
                sh 'docker stop sms-web-jenkins sms-db-jenkins 2>/dev/null || true'
                sh 'docker rm -f sms-web-jenkins sms-db-jenkins 2>/dev/null || true'
                sh 'docker network rm sms-pipeline_default 2>/dev/null || true'
            }
        }
        stage('Build and Deploy') {
            steps {
                sh 'cp -r /var/lib/jenkins/workspace/sms-pipeline/* /opt/sms-app/'
                sh 'cd /opt/sms-app && docker-compose -f docker-compose-jenkins.yml up -d'
            }
        }
        stage('Verify') {
            steps {
                sh 'sleep 15 && docker ps'
            }
        }
    }
    post {
        success { echo 'SMS app running on port 8090!' }
        failure { echo 'Pipeline failed. Check logs.' }
    }
}
