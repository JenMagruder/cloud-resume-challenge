"""
Website Analytics Lambda Function
Queries CloudFront access logs via Athena and sends daily email reports via SNS

Environment Variables Required:
- ATHENA_OUTPUT_LOCATION: S3 path for query results (e.g., s3://your-bucket/athena-results/)
- SNS_TOPIC_ARN: ARN of SNS topic for notifications
- FILTERED_IPS: Comma-separated IPs to exclude (e.g., "1.2.3.4,5.6.7.8")
- DATABASE: Athena database name (default: cloudfront_logs_db)
- TABLE: Athena table name (default: cloudfront_logs)
"""

import boto3
import json
import os
from datetime import datetime, timedelta
import time

# Initialize AWS clients
athena_client = boto3.client('athena')
sns_client = boto3.client('sns')

# Configuration from environment variables
DATABASE = os.environ.get('DATABASE', 'cloudfront_logs_db')
TABLE = os.environ.get('TABLE', 'cloudfront_logs')
OUTPUT_LOCATION = os.environ['ATHENA_OUTPUT_LOCATION']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
FILTERED_IPS = os.environ['FILTERED_IPS'].split(',')

def lambda_handler(event, context):
    """Main Lambda handler - executes analytics queries and sends email report"""
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Build IP filter for SQL queries
    ip_filter = "(" + ", ".join([f"'{ip.strip()}'" for ip in FILTERED_IPS]) + ")"
    
    # Define analytics queries
    queries = {
        'overview': f"""
            SELECT 
                COUNT(*) as total_visits,
                COUNT(DISTINCT c_ip) as unique_visitors,
                COUNT(DISTINCT date) as days_tracked
            FROM {TABLE}
            WHERE c_ip NOT IN {ip_filter}
        """,
        'yesterday': f"""
            SELECT 
                COUNT(*) as visits_yesterday,
                COUNT(DISTINCT c_ip) as unique_yesterday
            FROM {TABLE}
            WHERE date = DATE '{yesterday}'
                AND c_ip NOT IN {ip_filter}
        """,
        'top_pages': f"""
            SELECT cs_uri_stem, COUNT(*) as visits
            FROM {TABLE}
            WHERE c_ip NOT IN {ip_filter}
            GROUP BY cs_uri_stem
            ORDER BY visits DESC
            LIMIT 5
        """,
        'geo_distribution': f"""
            SELECT x_edge_location, COUNT(*) as requests
            FROM {TABLE}
            WHERE c_ip NOT IN {ip_filter}
            GROUP BY x_edge_location
            ORDER BY requests DESC
            LIMIT 10
        """,
        'top_visitors': f"""
            SELECT c_ip, COUNT(*) as visits
            FROM {TABLE}
            WHERE c_ip NOT IN {ip_filter}
            GROUP BY c_ip
            ORDER BY visits DESC
            LIMIT 10
        """
    }
    
    # Execute all queries
    results = {}
    for query_name, query_sql in queries.items():
        results[query_name] = execute_athena_query(query_sql)
    
    # Format and send email
    email_body = format_email(yesterday, results)
    
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f'📊 Website Analytics - {today}',
        Message=email_body
    )
    
    return {'statusCode': 200, 'body': 'Analytics report sent successfully'}

def execute_athena_query(query):
    """Execute Athena query and return results"""
    # Start query execution
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT_LOCATION}
    )
    
    query_execution_id = response['QueryExecutionId']
    
    # Wait for query to complete (max 30 seconds)
    for i in range(30):
        status_response = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )
        status = status_response['QueryExecution']['Status']['State']
        
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
    
    # Return results if successful
    if status == 'SUCCEEDED':
        results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        return results['ResultSet']['Rows']
    else:
        return []

def format_email(yesterday, results):
    """Format analytics data into readable email report"""
    email = f"""
Website Analytics Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

═══════════════════════════════════════
📊 ALL-TIME OVERVIEW
═══════════════════════════════════════
"""
    
    # All-time overview
    if len(results['overview']) > 1:
        total_visits = results['overview'][1]['Data'][0]['VarCharValue']
        unique_visitors = results['overview'][1]['Data'][1]['VarCharValue']
        days_tracked = results['overview'][1]['Data'][2]['VarCharValue']
        email += f"Total Visits: {total_visits}\n"
        email += f"Unique Visitors: {unique_visitors}\n"
        email += f"Days Tracked: {days_tracked}\n"
    else:
        email += "No traffic data available.\n"
    
    # Yesterday's traffic
    email += f"\n═══════════════════════════════════════\n📅 YESTERDAY ({yesterday})\n═══════════════════════════════════════\n"
    if len(results['yesterday']) > 1:
        visits = results['yesterday'][1]['Data'][0]['VarCharValue']
        unique = results['yesterday'][1]['Data'][1]['VarCharValue']
        email += f"Visits: {visits}\n"
        email += f"Unique Visitors: {unique}\n"
    else:
        email += "No traffic yesterday.\n"
    
    # Top pages
    email += "\n═══════════════════════════════════════\n📄 TOP PAGES (All Time)\n═══════════════════════════════════════\n"
    if len(results['top_pages']) > 1:
        for row in results['top_pages'][1:]:
            uri = row['Data'][0].get('VarCharValue', 'N/A')
            visits = row['Data'][1].get('VarCharValue', '0')
            email += f"{uri}: {visits} visits\n"
    else:
        email += "No page data.\n"
    
    # Geographic distribution
    email += "\n═══════════════════════════════════════\n🌍 GEOGRAPHIC DISTRIBUTION\n═══════════════════════════════════════\n"
    if len(results['geo_distribution']) > 1:
        for row in results['geo_distribution'][1:]:
            location = row['Data'][0].get('VarCharValue', 'N/A')
            requests = row['Data'][1].get('VarCharValue', '0')
            email += f"{location}: {requests} requests\n"
    else:
        email += "No geographic data.\n"
    
    # Top visitors
    email += "\n═══════════════════════════════════════\n👥 TOP VISITORS\n═══════════════════════════════════════\n"
    if len(results['top_visitors']) > 1:
        for row in results['top_visitors'][1:]:
            ip = row['Data'][0].get('VarCharValue', 'N/A')
            visits = row['Data'][1].get('VarCharValue', '0')
            email += f"{ip}: {visits} visits\n"
    else:
        email += "No visitor data.\n"
    
    email += f"\n═══════════════════════════════════════\n🚫 Filtered IPs: {len(FILTERED_IPS)} IP(s) excluded from stats\n"
    
    return email