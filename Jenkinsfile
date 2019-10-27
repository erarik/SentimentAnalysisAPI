node {
    def app    
    
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }
    
    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
        app = docker.build("erarik/sentimentanalysis")
    }
    
    withEnv(["PATH+KUBECTL=/home/ubuntu/bin"]) {
        stage('Apply Kubernetes files') {
             withAWS(credentials: 'awsjenkins', region: 'us-west-2') {
                    sh 'kubectl apply -f aws-auth-cm.yaml'
                    sh 'kubectl apply -f kubectl_deploy.yaml'
                    sh 'kubectl get deployments'
                    sh 'kubectl apply -f kubectl_service.yaml'
                    sh 'kubectl get services'
                    sh 'kubectl get pods'
                    sh 'kubectl get events'
             }   
        }
    }
}
