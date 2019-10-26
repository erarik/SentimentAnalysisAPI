node {
    def app    
    
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }
    
    withEnv(["PATH+KUBECTL=/home/ubuntu/bin"]) {
        stage('Apply Kubernetes files') {
                withAWS(credentials: 'awsjenkins', region: 'us-west-2') {
                    sh 'aws s3 ls'
                    sh 'aws eks --region us-west-2 create-cluster --name ekscluster3 --kubernetes-version 1.14 --role-arn arn:aws:iam::307015418607:role/eks_role --resources-vpc-config subnetIds=subnet-09bb1b2f0533c084c,subnet-035f47b1eb1236c69,subnet-0991faca317be20c7,securityGroupIds=sg-04be0d254b1bf5c8c'
                    sh 'aws eks --region us-west-2 update-kubeconfig --name ekscluster3'
                    sh 'kubectl get svc --v=10'
                    sh 'kubectl apply -f kubectl_deploy.yaml'
                }
            
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
