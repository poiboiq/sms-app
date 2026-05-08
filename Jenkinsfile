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
                sh 'docker compose -f docker-compose-jenkins.yml down 2>/dev/null || true'
                sh 'docker compose -f docker-compose.ci.yml down --volumes 2>/dev/null || true'
            }
        }

        stage('Build and Deploy') {
            steps {
                sh 'mkdir -p /opt/sms-app'
                sh 'cp -r /var/lib/jenkins/workspace/sms-pipeline/* /opt/sms-app/'
                sh 'cd /opt/sms-app && docker compose -f docker-compose-jenkins.yml up -d'
                sh 'sleep 15 && docker ps'
            }
        }

        stage('Test') {
            steps {
                sh """
                    cd /var/lib/jenkins/workspace/sms-pipeline
                    docker compose -f docker-compose.ci.yml build
                    docker compose -f docker-compose.ci.yml run --rm tests
                """
            }
            post {
                always {
                    sh 'cd /var/lib/jenkins/workspace/sms-pipeline && docker compose -f docker-compose.ci.yml down --volumes 2>/dev/null || true'
                    junit 'selenium-tests/reports/selenium-results.xml'
                }
            }
        }
    }

    post {
        always {
            script {
                def pusher = sh(
                    script: "git -C /var/lib/jenkins/workspace/sms-pipeline log -1 --format='%ae'",
                    returnStdout: true
                ).trim()
                emailext(
                    to: "${pusher}",
                    subject: "SMS App Test Results - Build #${BUILD_NUMBER} - ${currentBuild.currentResult}",
                    body: """Pipeline: ${JOB_NAME}
Build #: ${BUILD_NUMBER}
Result: ${currentBuild.currentResult}
Duration: ${currentBuild.durationString}
Full results: ${BUILD_URL}
Test Report: ${BUILD_URL}testReport/
""",
                    attachmentsPattern: 'selenium-tests/reports/selenium-results.xml'
                )
            }
        }
        success { echo 'All tests passed! SMS app deployed on port 8090.' }
        failure { echo 'Pipeline failed. Check logs.' }
    }
}