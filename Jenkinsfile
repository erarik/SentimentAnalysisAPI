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
                 sh 'aws s3 ls'
                 sh 'aws eks --region us-west-2 create-cluster --name ekscluster --kubernetes-version 1.14 --role-arn arn:aws:iam::307015418607:role/eks_role --resources-vpc-config subnetIds=subnet-04ac01e17e69e733a,subnet-0eabc150169202bbc,subnet-02c48a96d7758c295,securityGroupIds=sg-093e52ad0675eb522'
             }   
        }
    }
}
