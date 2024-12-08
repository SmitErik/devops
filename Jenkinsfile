pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/SmitErik/devops.git'
            }
        }
        stage('Terraform Init') {
            steps {
                script {
                    sh 'terraform init'
                }
            }
        }
        stage('Terraform Plan') {
            steps {
                script {
                    sh 'terraform plan -out=tfplan'
                }
            }
        }
        stage('Terraform Apply') {
            steps {
                script {
                    sh 'terraform apply -auto-approve tfplan'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    sh '''
                        chmod +x run_tests.sh
                        ./run_tests.sh
                    '''
                }
            }
        }
    }
    post {
        always {
            echo "End of Pipeline"
        }
        success {
            echo "The Terraform app is running succesfully."
        }
        failure {
            echo "Job failed. Running terraform destroy..."
            sh 'terraform destroy -auto-approve'
        }
    }
}
