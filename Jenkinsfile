pipeline {
    agent any

    environment {
        TERRAFORM_DIR = "terraform"
        PEM_CREDENTIALS_ID = "aws-pem-key"   /* Jenkins credential ID for PEM file */
        AWS_CREDENTIALS_ID = "aws-credentials"
        BRANCH_NAME = "main"
        REGION = "us-west-2"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: "*/${BRANCH_NAME}"]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/AdeleyeAdeyemi/calculator',
                        credentialsId: "${AWS_CREDENTIALS_ID}"
                    ]]
                ])
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${AWS_CREDENTIALS_ID}",
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    dir("${TERRAFORM_DIR}") {
                        sh '''
                            terraform init
                            terraform apply -auto-approve
                        '''
                    }
                }
            }
        }

        stage('Prepare Ansible Inventory') {
            steps {
                script {
                    def publicIp = sh(script: "terraform -chdir=${TERRAFORM_DIR} output -raw public_ip", returnStdout: true).trim()
                    def pemFile = "${TERRAFORM_DIR}/jenkins-key.pem"
                    sh "chmod 600 ${pemFile}"

                    def inventory = """
all:
  hosts:
    ${publicIp}:
      ansible_user: ec2-user
      ansible_ssh_private_key_file: ${pemFile}
      ansible_python_interpreter: /usr/bin/python3
      ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
"""
                    writeFile file: 'inventory_generated.yml', text: inventory
                    echo "Ansible inventory created:\n${inventory}"
                }
            }
        }

        stage('Configure & Deploy with Ansible') {
            steps {
                sh 'ansible-playbook -i inventory_generated.yml ansible/playbook.yml'
            }
        }

        stage('Build & Run Docker') {
            steps {
                sh 'docker compose up -d --remove-orphans'
               
            }
        } 

        stage('Build Docker Image') {
            steps {
                script {
                    def buildResult = sh(script: 'docker build -t calculator-app:latest .', returnStatus: true)
                    if (buildResult != 0) {
                        sh 'docker logs $(docker ps -q --filter "name=calculator-app") || true'
                        error "Docker build failed"
                    }
                }
            }
        }

        stage('Verify Image') {
            steps {
                sh '''
                    docker run --rm calculator-app:latest python3 --version
                    docker run --rm calculator-app:latest pip list
                '''
            }
        }
        

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker tag ecommerce-app:latest \$DOCKER_USER/calculator-app:${IMAGE_TAG}
                        docker push \$DOCKER_USER/calculator-app:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: '**/*.py', fingerprint: true
            }
        }

        stage('Verify App & Containers') {
            steps {
                sh 'docker ps'
            }
        }

        stage('Wait for App Ready') {
            steps {
                sh 'sleep 30'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    if [ ! -d "venv" ]; then
                        python3 -m venv --copies --upgrade-deps venv
                    fi
                    chmod +x venv/bin/python3
                    ./venv/bin/python3 -m pip install --upgrade "pip<24" setuptools wheel
                    ./venv/bin/python3 -m pip install -r requirements.txt pytest selenium
                    ./venv/bin/python3 -m pytest tests/selenium --maxfail=1 --disable-warnings -q
                '''
            }
        }
    }

    post {
        always {
            echo 'Ensuring all containers are running'
            sh 'docker compose up -d --remove-orphans'
        }
    }
}




