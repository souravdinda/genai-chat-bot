import boto3

textract = boto3.client("textract")

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}},
        NotificationChannel={
            "SNSTopicArn": "<your-sns-topic-arn>",
            "RoleArn": "<iam-role-that-textract-uses>"
        }
    )
    job_id = response["JobId"]
    return {
        "statusCode": 200,
        "jobId": job_id,
        "message": "Textract job started successfully"
    }
    # Save job_id + metadata in DynamoDB
