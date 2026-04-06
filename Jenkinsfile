pipeline {
    agent any

    environment {
        // SonarQube Configuration
        SONAR_HOST_URL = 'http://localhost:9000'
        
        // Application Configuration
        APP_NAME = 'python-calculator-api'
        DOCKER_IMAGE = 'calculator-api'
        DOCKER_TAG = "${env.BUILD_ID}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Run Unit Tests with Coverage') {
            steps {
                echo 'Running unit tests in Docker container...'
                script {
                    docker.image('python:3.11-slim').inside {
                        sh '''
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install pytest pytest-cov
                            pytest test_app.py --cov=. --cov-report=xml --cov-report=term
                        '''
                    }
                }
            }
            post {
                always {
                    // Archive test results
                    junit allowEmptyResults: true, testResults: '**/pytest.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                script {
                    // Run sonar-scanner using Docker
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
        }

        stage('Quality Gate Check') {
            steps {
                echo 'Waiting for SonarQube quality gate...'
                script {
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
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image for the application...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run Container Locally') {
            steps {
                echo 'Running application container...'
                sh '''
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }

        stage('Test Running Container') {
            steps {
                echo 'Testing the running container...'
                sh '''
                    sleep 5
                    curl -f http://localhost:5000/health || exit 1
                    curl -f -X POST http://localhost:5000/add \
                        -H "Content-Type: application/json" \
                        -d '{"a":5,"b":3}' || exit 1
                    echo "All tests passed!"
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed. Cleaning up...'
            cleanWs()
        }
        success {
            echo '''
                ========================================
                ✅ PIPELINE SUCCESSFUL!
                ========================================
                Application is running at: http://localhost:5000
                SonarQube dashboard: http://localhost:9000
                
                Test the API:
                curl http://localhost:5000/health
                curl -X POST http://localhost:5000/add -H "Content-Type: application/json" -d '{"a":5,"b":3}'
                ========================================
            '''
        }
        failure {
            echo '''
                ========================================
                ❌ PIPELINE FAILED!
                ========================================
                Check the following:
                1. Is SonarQube container running? (docker ps | grep sonarqube)
                2. Check SonarQube quality gates at http://localhost:9000
                3. Review Jenkins console output for specific errors
                ========================================
            '''
        }
    }
}
