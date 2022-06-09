#!/bin/bash

# Script for lambda-node-with-role-non-serverless.yaml
# Usage
# ./1.sample_shell_script_for_deployment.sh <create or update>

# CLI Parameters
stack_name=test-lambda
s3_bucket=test-bucket                                 # bucket for storing deployment files
s3_key=deployments                                    # s3 folder for storing deployment files
lambda_layer_s3_key=lambda-layers                     # s3 folder for lambda layer zip files
lambda_function_s3_key=lambda-function                # s3 folder for lambda function zip file
region=us-west-2
lambda_function_zip="test_$(date +%Y%m%d%H%M).zip"

# zip -r node_utils_func.zip src > /dev/null
aws s3 cp node_utils_func.zip s3://$s3_bucket/$lambda_function_s3_key/$lambda_function_zip
aws s3 cp node_utils.zip s3://$s3_bucket/$lambda_layer_s3_key/

# Cloudformation Parameters
vpc_name=vpc-2
sec_group_ids='"sg-0a12345b345fe678,sg-0b45678c345fe123"'
lambda_role="test-lambda-role"
lambda_layer_s3_key_zip="$lambda_layer_s3_key/layer.zip"   

# Get VPC Id
vpc_id=`aws ec2 describe-vpcs --region us-west-2 --filters 'Name=tag:Name,Values='$vpc_name --query 'Vpcs[0].VpcId'`

#Deploy lambda
if [ "$1" = "create" ]; then
  aws cloudformation create-stack --stack-name $stack_name --region $region --template-body file://template.yaml --parameters ParameterKey=SecurityGroupIds,ParameterValue=$sec_group_ids ParameterKey=VPCId,ParameterValue=$vpc_id ParameterKey=LambdaRoleName,ParameterValue=$lambda_role ParameterKey=S3Bucket,ParameterValue=$s3_bucket ParameterKey=S3FunctionKey,ParameterValue=$lambda_function_s3_key ParameterKey=S3FunctionZip,ParameterValue=$lambda_function_zip ParameterKey=S3Key,ParameterValue=$lambda_layer_s3_key_zip  --capabilities CAPABILITY_NAMED_IAM
else
  aws cloudformation update-stack --stack-name $stack_name --region $region --template-body file://template.yaml --parameters ParameterKey=SecurityGroupIds,ParameterValue=$sec_group_ids ParameterKey=VPCId,ParameterValue=$vpc_id ParameterKey=LambdaRoleName,ParameterValue=$lambda_role ParameterKey=S3Bucket,ParameterValue=$s3_bucket ParameterKey=S3FunctionKey,ParameterValue=$lambda_function_s3_key ParameterKey=S3FunctionZip,ParameterValue=$lambda_function_zip ParameterKey=S3Key,ParameterValue=$lambda_layer_s3_key_zip --capabilities CAPABILITY_NAMED_IAM
fi