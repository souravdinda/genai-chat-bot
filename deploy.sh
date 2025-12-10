#!/bin/bash
set -e

BUCKET_NAME="mytest1804new"
STACK_NAME="chatbot"
REGION="us-east-1"
VPC_ID="vpc-08085f6e34008acb7"
SUBNET_IDS="subnet-0f988d9b766a53b36,subnet-0f2049aee06cfe5a0"

echo "Deploying to Region: $REGION"
echo "Using Bucket: $BUCKET_NAME"

# 2. Upload Templates
echo "Uploading templates..."
aws s3 cp . s3://$BUCKET_NAME/genai-bot-copy/ --recursive --exclude "*" --include "*.yaml"

# 3. Deploy Root Stack
echo "Deploying Root Stack..."
aws cloudformation deploy \
    --template-file root.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        Environment=dev \
        S3TemplateBucket=$BUCKET_NAME \
        VpcId=$VPC_ID \
        SubnetIds=$SUBNET_IDS \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
    --region $REGION

echo "Deployment Complete!"
