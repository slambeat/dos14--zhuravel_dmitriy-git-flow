pipeline {
  agent any
    stages {
      stage('Lint') {
        agent {
            docker {
                image 'python:3.11.3-buster'
                args '-u 0'
            }
        }
        when {
          anyOf {
            branch pattern: "feature-*"
          }
        }
        steps {
          sh "pip install poetry"
          sh "poetry install --with dev"
          sh "poetry run black ./"
          sh "poetry run -- black --check *.py"
          script { build = false }
        }
      }
      stage('Build') {
      when {
        anyOf {
          branch pattern: "develop"
        }
      }
      steps {
        script {
          def image = docker.build "slambeat/bank_app:${env.GIT_COMMIT}"
          docker.withRegistry('','dockerhub-slambeat') {
            image.push()
          build = "${env.GIT_COMMIT}"
          }
        }
      }
    }
    stage('Update Helm Chart') {
      when { expression { build == "${env.GIT_COMMIT}" } }
      steps {
        sh "git checkout feature-helm-CD"
        sh "git config --global pull.rebase true"
        sh "git pull origin"
        script {
        def filename = 'helm_CD/bank/values.yaml'
        def data = readYaml file: filename

        // Change something in the file
        data.image.tag = "${env.GIT_COMMIT}"

        sh "rm $filename"
        writeYaml file: filename, data: data

          withCredentials([string(credentialsId: 'zdo_github_token', variable: 'SECRET')]) {
                sh('git config --global user.email "sphynxx.mail@gmail.com" && git config --global user.name "Jenkins"')
                sh('git add .')
                sh('git commit -m "JENKINS: add new image tag ("${env.GIT_COMMIT}") tag in helm chart tag for CD"')
                sh('git remote set-url origin https://${SECRET}@github.com/slambeat/dos14--zhuravel_dmitriy-git-flow.git')
                sh('git push origin feature-helm-CD')
          }
        }
      }
    }
  }
}