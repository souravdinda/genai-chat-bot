def lambda_handler(event, context):
    print("Received event:", event)
    return {
        "statusCode": 200,
        "message": "Receipt processed successfully"
    }