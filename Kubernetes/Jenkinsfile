pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        GITHUB_CREDENTIALS = 'github-credentials'
        DOCKER_IMAGE = "mkislam2015/flask-api"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/mkislam-wipro-2015/BrainStation23-Assignmentts.git',
                    credentialsId: "${GITHUB_CREDENTIALS}"
            }
        }

        stage('Read Version') {
            steps {
                script {
                    echo "Reading .env file..."
                    sh 'cat .env'
                    VERSION = sh(script: "grep VERSION .env | awk -F= '{print \$2}'", returnStdout: true).trim()
                    echo "VERSION: '${VERSION}'"
                    if (!VERSION) {
                        error("VERSION not found!")
                    }
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh "docker build -t ${DOCKER_IMAGE}:${VERSION} ."
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${DOCKER_IMAGE}:${VERSION}
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh '''
                        kubectl apply -f kubernetes/secrets.yaml
                        kubectl apply -f kubernetes/configmap.yaml
                        kubectl apply -f kubernetes/deployment.yaml
                        kubectl apply -f kubernetes/service.yaml
                    '''
                }
            }
        }
    }
}

