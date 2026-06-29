import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'cloud-resume-visitor-counter'))

def get_cors_headers():
    """Return CORS headers for API responses."""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }

def lambda_handler(event, context):
    # Handle OPTIONS preflight request
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': ''
        }

    # Handle POST request - increment counter
    try:
        response = table.update_item(
            Key={'id': 'visitor-count'},
            UpdateExpression='SET #count = if_not_exists(#count, :start) + :inc',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':start': 0, ':inc': 1},
            ReturnValues='UPDATED_NEW'
        )

        count = int(response['Attributes']['count'])

        return {
            'statusCode': 200,
            'headers': get_cors_headers(),
            'body': json.dumps({'count': count})
        }

    except ClientError as e:
        print(f"DynamoDB error: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Failed to update visitor count'})
        }

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': get_cors_headers(),
            'body': json.dumps({'error': 'Internal server error'})
        }