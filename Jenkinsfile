#!groovy
pipeline {
    agent any

    stages {

        stage('Clone Repo'){
            steps{
                git url: "https://github.com/kumarSumit6038/OktaAppSelfServe.git"
                url: "https://github.com/kumarSumit6038/OktaAppSelfServe/blob/15e5ff089cc79881a58342706acd0dd427b36602/app-details.properties"
            }

        }
        stage("Read Properties"){
            steps{
                def props = readProperties file: './app-details.properties'
            }
        }
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