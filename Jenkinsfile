#!groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                sh '. /Users/kairaneha/.local/share/virtualenvs/OktaAppSelfServe-lDy_E8lw/bin/activate && pip install -r requirements.txt && python CreateGroup.py'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}