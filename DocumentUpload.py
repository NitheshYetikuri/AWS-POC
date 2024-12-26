import json
import boto3
from datetime import datetime
import uuid
import base64

print('loading function')

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

bucket_name = 'company-records-bucket'  # Updated with your S3 bucket name
queue_url = 'https://sqs.ap-southeast-2.amazonaws.com/529088289934/DocumentUpload'  # Your SQS queue URL

def upload_to_s3(document, company_name):
    try:
        document_content = base64.b64decode(document)
        s3_key = f'documents/{company_name}.pdf'
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=document_content)
        s3_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_key}'
        return s3_url
    except Exception as e:
        print(f'Error uploading to S3: {e}')
        raise

def generate_presigned_url(company_name):
    try:
        s3_key = f'documents/{company_name}.pdf'
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=3600
        )
        return presigned_url
    except Exception as e:
        print(f'Error generating presigned URL: {e}')
        raise

def send_message_to_sqs(message_body):
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body)
        )
        return response
    except Exception as e:
        print(f'Error sending message to SQS: {e}')
        raise

def lambda_handler(event, context):
    try:
        print(f'Event: {event}')
        body = json.loads(event['body'])
        print(f'Parsed body: {body}')
        
        unique_id = str(uuid.uuid4())
        companyName = body['companyName']
        prompt = body['prompt']
        document = body['document']
        timestamp = body.get('timestamp', datetime.utcnow().isoformat())
        
        print(f'ID={unique_id}, CompanyName={companyName}, Prompt={prompt}, Timestamp={timestamp}')
        
        s3_url = upload_to_s3(document, companyName)
        presigned_url = generate_presigned_url(companyName)
        
        message_body = {
            'unique_id': unique_id,
            'CompanyName': companyName,
            'Prompt': prompt,
            'SignedURL': presigned_url,
            'Timestamp': timestamp
        }
        
        send_message_to_sqs(message_body)
        
        transactionResponse = {
            'unique_id': unique_id,
            'CompanyName': companyName,
            'Prompt': prompt,
            'Timestamp': timestamp,
            'SignedURL': presigned_url,
            'msg': 'Transaction stored successfully'
        }
        
        responseObject = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(transactionResponse)
        }
    except KeyError as e:
        print(f'KeyError: {e}')
        responseObject = {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'msg': f'Bad Request: Missing {str(e)} in request body'})
        }
    except json.JSONDecodeError as e:
        print(f'JSONDecodeError: {e}')
        responseObject = {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'msg': 'Bad Request: Invalid JSON'})
        }
    return responseObject
