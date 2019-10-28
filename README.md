[![CircleCI](https://circleci.com/gh/erarik/SentimentAnalysisAPI.svg?style=svg)](https://circleci.com/gh/erarik/SentimentAnalysisAPI)

# Sentiment prediction with a Machine Learning Microservice API
This repository contains scipts and codes to deploy a microservice using kubernetes that serves out predictions on whether a review is positive or negative.

## Overview
The model is based on a pre-trained, `sklearn` model that has been trained to predict whether the review is positive or negative. 

## Setup the Environment
* Build AWS EKS (Kubernetes Cluster) environment. Follow the tutorial https://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html
* Create your Jenkins master.

### Pipeline description
* Clone repository
* Build docker image
* Push image to docker hub
* Update deploy yaml file to take into account the build number
* Deploy the image to AWS EKS

### Useful External links
* https://kubernetes.io/fr/docs/reference/kubectl/cheatsheet/
* https://amazon-eks.s3-us-west-2.amazonaws.com/cloudformation/2019-10-08/amazon-eks-vpc-sample.yaml
