pipeline {
    agent any

    environment {
        TF_VAR_region = 'eu-west-2'  // Global Terraform variable
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AdeleyeAdeyemi/calculator'
            }
        }

        stage('Provision Infrastructure') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'aws-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    dir('terraform') {
                        sh '''
                            export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                            export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
                            
                            terraform init
                            
                            terraform apply -auto-approve \
                                -var="aws_access_key=${AWS_ACCESS_KEY_ID}" \
                                -var="aws_secret_key=${AWS_SECRET_ACCESS_KEY}" \
                                -var="vpc_id=your-vpc-id"    # <-- Replace with your actual VPC ID
                        '''
                    }
                }
            }
        }

        stage('Configure & Deploy with Ansible') {
            steps {
                dir('ansible') {
                    sh 'ansible-playbook -i inventory.ini playbook.yml'
                }
            }
        }

        stage('Build App') {
            steps {
                sh 'chmod +x build.sh && ./build.sh'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def result = sh(script: 'docker compose build --no-cache', returnStatus: true)
                    if (result != 0) {
                        sh 'docker compose logs || true'
                        error 'Docker Compose build failed'
                    }
                }
            }
        }

        stage('Run Containers') {
            steps {
                script {
                    def result = sh(script: 'docker compose up -d', returnStatus: true)
                    if (result != 0) {
                        sh 'docker compose logs || true'
                        error 'Failed to start containers with Docker Compose'
                    }
                }
            }
        }

        stage('Verify Docker & Flask Status') {
            steps {
                sh '''
                    echo "Running containers:"
                    docker ps

                    echo "Flask container logs:"
                    docker logs $(docker ps -q --filter "name=calculator") || true

                    echo "Installed Python packages:"
                    docker exec $(docker ps -q --filter "name=calculator") pip list || true
                '''
            }
        }

        stage('Wait for App to be Ready') {
            steps {
                script {
                    def maxRetries = 20
                    def waitSeconds = 6
                    def ready = false

                    for (int i = 0; i < maxRetries; i++) {
                        def result = sh(script: 'curl -sf http://localhost:8977 || true', returnStatus: true)
                        if (result == 0) {
                            echo "App is ready"
                            ready = true
                            break
                        } else {
                            echo "App not ready, waiting ${waitSeconds}s..."
                            sleep(waitSeconds)
                        }
                    }

                    if (!ready) {
                        sh 'docker logs $(docker ps -q --filter "name=calculator") || true'
                        error "App did not become ready in time"
                    }
                }
            }
        }

        stage('Test with Selenium') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip selenium
                '''
            }
        }
    }

    post {
        always {
            echo "Cleaning up / restarting Docker Compose in post step"
            sh 'docker compose up -d || true'
        }
    }
}
