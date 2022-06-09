#!/bin/bash

# Script for serverless-lambda-function-with-layer-nodejs.yaml

# CLI Parameters
stack_name=test-lambda
s3_bucket=test-bucket                                 # bucket for storing deployment files
s3_key=deployments  
region=us-west-2

# Cloudformation Parameters
layer_name="test-lambda-layer"
role_arn="arn:aws:iam::123456789:role/<lambda-role-name>"   

#Deploy lambda
sam build -t template.yaml --parameter-overrides "ParameterKey=RoleArn,ParameterValue=$role_arn ParameterKey=LayerName,ParameterValue=$layer_name" --use-container && sam deploy --stack-name $stack_name --s3-bucket $s3_bucket --s3-prefix $s3_key --region $region --parameter-overrides "ParameterKey=RoleArn,ParameterValue=$role_arn ParameterKey=LayerName,ParameterValue=$layer_name" --capabilities CAPABILITY_NAMED_IAM