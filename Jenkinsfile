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

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('https://registry.hub.docker.com', 'docker-Hub-credentials') {
            app.push("${env.BUILD_NUMBER}")
            app.push("latest")
        }
    }
    
    withEnv(["PATH+KUBECTL=/home/ubuntu/bin"]) {
        stage('Apply Kubernetes files') {
                withAWS(credentials: 'awsjenkins', region: 'us-west-2') {
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
