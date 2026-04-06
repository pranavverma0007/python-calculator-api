pipeline {
    agent any

    environment {
        SONAR_HOST_URL = 'http://172.30.68.218:9000'  // Your WSL IP
        SONAR_AUTH_TOKEN = credentials('sonar-token')
        
        APP_NAME = 'python-calculator-api'
        DOCKER_IMAGE = 'calculator-api'
        DOCKER_TAG = "${env.BUILD_ID}"
    }

    stages {
        stage('Run Unit Tests with Coverage') {
            steps {
                echo 'Running unit tests in Docker container...'
                script {
                    docker.image('python:3.11-slim').inside("-u root") {
                        sh '''
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install pytest pytest-cov
                            pytest test_app.py --junitxml=pytest.xml --cov=. --cov-report=xml --cov-report=term
                        '''
                    }
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: '**/pytest.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                sh '''
                    docker run --rm \
                        -v ${PWD}:/usr/src \
                        -w /usr/src \
                        sonarsource/sonar-scanner-cli:latest \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN} \
                        -Dsonar.projectKey=python-calculator-api \
                        -Dsonar.projectName="Python Calculator API" \
                        -Dsonar.sources=. \
                        -Dsonar.exclusions="**/venv/**,**/__pycache__/**,test_*.py" \
                        -Dsonar.tests=. \
                        -Dsonar.test.inclusions="test_*.py" \
                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                        -Dsonar.python.version=3.11
                '''
            }
        }

        stage('Quality Gate Check') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    sh '''
                        docker run --rm \
                            sonarsource/sonar-scanner-cli:latest \
                            sonar-quality-gate --wait \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN}
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Deploy & Test') {
            steps {
                sh '''
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 5
                    curl -f http://localhost:5000/health || exit 1
                    echo "Container is healthy!"
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
