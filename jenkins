pipeline {
    agent any

    stages {
        stage('Compile') {
            steps {
                dir('src') {
                    bat 'javac Hello.java'
                }
            }
        }

        stage('Run') {
            steps {
                dir('src') {
                    bat 'java Hello'
                }
            }
        }
    }

    post {
        success {
            echo 'BUILD SUCCESSFUL'
        }
        failure {
            echo 'BUILD FAILED'
        }
    }
}