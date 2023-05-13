pipeline {
    agent any

    stages {
        stage('Train') {
            steps {
                echo 'Training..'
                sh 'whoami'
                sh 'ls -l'
                sh 'pwd'
                sh 'curl -LO https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh'
                sh 'chmod +x Miniconda3-py310_23.3.1-0-Linux-x86_64.sh'
                sh './Miniconda3-py310_23.3.1-0-Linux-x86_64.sh -b -p $(pwd)'
                sh '. miniconda3/bin/activate && pip install tensorflow'
                sh '. miniconda3/bin/activate && python train.py'
            }
        }
    }
}