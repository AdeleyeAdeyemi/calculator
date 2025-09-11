# Calculator Web App

A Flask-based Calculator application with full CI/CD setup using **Jenkins**, **Docker**, **Terraform**, **Ansible**, and **Selenium** tests.




## Project Overview
This project demonstrates a full infrastructure-as-code and DevOps workflow for a Python Flask application. It includes:

- **Docker**: Containerized Flask app
- **Terraform**: Infrastructure provisioning on AWS Ec2 intances
- **Ansible**: Server configuration and app deployment
- **Jenkins**: CI/CD pipeline for automated builds and deployment
- **Selenium / Pytest**: End-to-end testing of the application


## Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Terraform
- Ansible
- Jenkins
- AWS CLI configured

## Jenkins CI/CD Pipeline
Your pipeline performs:
-Git checkout
-Terraform provisioning
-Generate Ansible inventory
-Deploy Flask app via Ansible
-Build Docker image
-Verify image (python3 --version, pip list)
-Push image to Docker Hub
-Run Selenium tests for validation


## Setup

1. Clone the repository:
```bash
git clone https://github.com/AdeleyeAdeyemi/calculator.git
cd calculator


