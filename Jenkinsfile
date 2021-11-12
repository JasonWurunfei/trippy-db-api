pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh """
                    chmod +x deploy.sh
                    sudo ./deploy.sh
                """
            }
        }
    }
}