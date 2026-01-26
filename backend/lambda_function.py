import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume-visitor-counter')

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