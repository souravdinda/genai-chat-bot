import json
import time
import urllib.request
import boto3

kendra = boto3.client('kendra')

def send_response(event, context, status, reason=None, physical_resource_id=None, data=None):
    response_body = json.dumps({
        'Status': status,
        'Reason': reason or f'See the details in CloudWatch Log Stream: {context.log_stream_name}',
        'PhysicalResourceId': physical_resource_id or context.log_stream_name,
        'StackId': event.get('StackId'),
        'RequestId': event.get('RequestId'),
        'LogicalResourceId': event.get('LogicalResourceId'),
        'Data': data or {}
    }).encode('utf-8')

    req = urllib.request.Request(event['ResponseURL'], data=response_body, method='PUT')
    req.add_header('Content-Type', '')
    req.add_header('Content-Length', str(len(response_body)))
    try:
        with urllib.request.urlopen(req) as f:
            pass
    except Exception as e:
        print("Failed sending response:", e)

def wait_for_active(index_id, timeout_seconds=600, poll_interval=5):
    start = time.time()
    while True:
        resp = kendra.describe_index(Id=index_id)
        status = resp.get('Status')
        if status == 'ACTIVE':
            return True, resp
        if status == 'FAILED':
            # Kendra may return an ErrorMessage or ErrorCode
            return False, resp.get('ErrorMessage', 'Index creation failed')
        if time.time() - start > timeout_seconds:
            return False, f"Timeout waiting for index {index_id} to become ACTIVE"
        time.sleep(poll_interval)

def handler(event, context):
    request_type = event.get('RequestType')
    props = event.get('ResourceProperties', {})
    index_id = props.get('IndexId')
    timeout = int(props.get('TimeoutSeconds', 600))
    try:
        if request_type in ('Create', 'Update'):
            ok, info = wait_for_active(index_id, timeout_seconds=timeout)
            if ok:
                send_response(event, context, 'SUCCESS', data={'IndexStatus': 'ACTIVE'})
            else:
                send_response(event, context, 'FAILED', reason=str(info))
        elif request_type == 'Delete':
            send_response(event, context, 'SUCCESS')
        else:
            send_response(event, context, 'FAILED', reason='Unknown RequestType')
    except Exception as e:
        send_response(event, context, 'FAILED', reason=str(e))