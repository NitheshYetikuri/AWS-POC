import json
import boto3

print('loading function')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CompanyRecords')  # Update with the new table name

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            message_body = json.loads(record['body'])
            print(f'Message Body: {message_body}')
            
            table.put_item(Item=message_body)
            
        return {
            'statusCode': 200,
            'body': json.dumps('Messages processed successfully')
        }
    except Exception as e:
        print(f'Error processing SQS message: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing messages')
        }
