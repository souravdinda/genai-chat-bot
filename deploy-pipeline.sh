#!/bin/bash
set -e

BUCKET_NAME="mytest1804new"
STACK_NAME="transcript"
REGION="us-east-1"

echo "Deploying Document Pipeline to Region: $REGION"
echo "Using S3 Bucket for Templates: $BUCKET_NAME"

# Upload Templates (to 'doc-pipeline' prefix to differentiate from chatbot)
echo "Uploading templates..."
aws s3 cp . s3://$BUCKET_NAME/doc-pipeline/ --recursive --exclude "*" --include "pipeline-*.yaml"

# Deploy Root Stack
echo "Deploying Pipeline Root Stack..."
aws cloudformation deploy \
    --template-file pipeline-root.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        Environment=dev \
        S3TemplateBucket=$BUCKET_NAME \
        ProjectId=034 \
        PortfolioId=020 \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
    --region $REGION

echo "Pipeline Deployment Complete!"
