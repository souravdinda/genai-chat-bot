import json, boto3, os
s3 = boto3.client('s3')
kendra = boto3.client('kendra')
try:
    bedrock = boto3.client('bedrock-runtime')
except Exception:
    bedrock = None
def lambda_handler(event, context):
    try:
        s3.put_object(Bucket=os.environ['AUDIT_BUCKET'],
                    Key=f"audit-{context.aws_request_id}.json",
                    Body=json.dumps(event))
    except Exception as e:
        print("audit write failed:", e)
    if 'httpMethod' in event:
        body = json.loads(event.get('body') or '{}')
        if body.get('service') == 'kendra':
            resp = kendra.query(IndexId=os.environ.get('KENDRA_INDEX_ID'), QueryText=body.get('query',''))
            return {'statusCode': 200, 'body': json.dumps(resp)}
        if body.get('service') == 'bedrock' and bedrock:
            res = bedrock.invoke_model(modelId="amazon.titan", contentType="application/json", accept="application/json", body=json.dumps({"input": body.get('prompt','')}))
            if 'body' in res:
                try:
                    return {'statusCode': 200, 'body': res['body'].read().decode()}
                except:
                    return {'statusCode': 200, 'body': json.dumps(res)}
            return {'statusCode': 200, 'body': json.dumps(res)}
        return {'statusCode': 200, 'body': json.dumps({"msg":"logged"})}
    if 'sessionState' in event:
        user_text = event.get('inputTranscript','')
        kresp = kendra.query(IndexId=os.environ.get('KENDRA_INDEX_ID'), QueryText=user_text) if os.environ.get('KENDRA_INDEX_ID') else {}
        answer = None
        if isinstance(kresp, dict) and kresp.get('ResultItems'):
            top = kresp['ResultItems'][0]
            answer = top.get('DocumentExcerpt', {}).get('Text', 'I found something.')
        else:
            if bedrock:
                bed = bedrock.invoke_model(modelId="amazon.titan", contentType="application/json", accept="application/json", body=json.dumps({"input": user_text}))
                if 'body' in bed:
                    try:
                        answer = bed['body'].read().decode()
                    except:
                        answer = str(bed)
                else:
                    answer = str(bed)
            else:
                answer = "Sorry, no model available."
        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {"name": event['sessionState']['intent']['name'], "state": "Fulfilled"}
            },
            "messages": [{"contentType": "PlainText", "content": answer}]
        }
    return {'statusCode': 400, 'body': json.dumps({'error': 'Unknown event'})}