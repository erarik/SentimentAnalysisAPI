node {
    def app
    
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }
    
    
    stage('Apply Kubernetes files') {
        withKubeConfig([credentialsId: 'awsjenkins', serverUrl: 'https://api.k8s.my-company.com']) {
            sh 'kubectl apply -f kubectl_deploy.yaml'
        }
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
}
