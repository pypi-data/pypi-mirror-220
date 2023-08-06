podTemplate(yaml: '''
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: python
        image: nctiggy/python-build-image
        command:
        - sleep
        args:
        - 99d
''')

{
  node(POD_LABEL) {
      checkout scmGit(
        branches: [[name: '*/tags/*']],
        userRemoteConfigs: [[
            refspec: '+refs/tags/*’:’refs/remotes/origin/tags/*',
            url: 'https://github.com/nctiggy/cnvrg_experiment_chart.git']]
        )
      container('python') {
        stage('Python version') {
          sh '''
            python --version
            ls -ltra
            printenv
            git --version
            git remote show origin
            git tag -l
            git describe
          '''
        }
        stage('Run Tests') {
          sh '''
            tox -e lint
            tox
          '''
        }
        stage('Build pypi package') {
          sh '''
            tox -e build
          '''
        }
        withCredentials([usernamePassword(credentialsId: 'pypi_user_pass', passwordVariable: 'TWINE_PASSWORD', usernameVariable: 'TWINE_USERNAME')]) {
          stage('Publish pypi package') {
            sh '''
              export TWINE_PASSWORD=$TWINE_PASSWORD
              export TWINE_USERNAME=$TWINE_USERNAME
              tox -e publish -- --repository pypi
              tox -e clean
            '''
          }
        }
      }
  }
}
