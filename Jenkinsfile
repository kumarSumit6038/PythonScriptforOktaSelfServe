#!groovy
pipeline {
    agent any

    stages {

        stage('Clone Repo'){
            steps{
                script{
                    git url: "https://github.com/kumarSumit6038/OktaAppSelfServe.git"
                    url: "https://github.com/kumarSumit6038/OktaAppSelfServe/blob/master/app-details.properties"
                }

            }

        }
        stage("Read Properties"){
            steps{
                script{
                    def props = readProperties file: './app-details.properties'
                }

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