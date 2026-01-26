"""
Website Analytics Lambda Function
Queries CloudFront access logs via Athena and sends daily email reports via SNS

Environment Variables Required:
- ATHENA_OUTPUT_LOCATION: S3 path for query results
- SNS_TOPIC_ARN: ARN of SNS topic for notifications
- FILTERED_IPS: Comma-separated IPs to exclude
- DATABASE: Athena database name (default: cloudfront_logs_db)
- TABLE: Athena table name (default: cloudfront_logs)
"""

import boto3
import json
import os
from datetime import datetime, timedelta
import time

athena_client = boto3.client('athena')
sns_client = boto3.client('sns')

DATABASE = os.environ.get('DATABASE', 'cloudfront_logs_db')
TABLE = os.environ.get('TABLE', 'cloudfront_logs')
OUTPUT_LOCATION = os.environ['ATHENA_OUTPUT_LOCATION']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
FILTERED_IPS = os.environ['FILTERED_IPS'].split(',')


def lambda_handler(event, context):
    """Execute analytics queries and send email report."""
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    ip_filter = build_ip_filter()
    
    results = {
        'overview': execute_query(get_overview_query(ip_filter)),
        'yesterday': execute_query(get_yesterday_query(ip_filter, yesterday)),
        'top_pages': execute_query(get_top_pages_query(ip_filter)),
        'geo_distribution': execute_query(get_geo_query(ip_filter)),
        'top_visitors': execute_query(get_top_visitors_query(ip_filter))
    }
    
    email_body = format_email_report(yesterday, results)
    
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f'Website Analytics - {today}',
        Message=email_body
    )
    
    return {'statusCode': 200, 'body': 'Analytics report sent successfully'}


def build_ip_filter():
    """Build SQL IN clause for filtered IPs."""
    return "(" + ", ".join([f"'{ip.strip()}'" for ip in FILTERED_IPS]) + ")"


def get_overview_query(ip_filter):
    """Return query for all-time overview statistics."""
    return f"""
        SELECT 
            COUNT(*) as total_visits,
            COUNT(DISTINCT c_ip) as unique_visitors,
            COUNT(DISTINCT date) as days_tracked
        FROM {TABLE}
        WHERE c_ip NOT IN {ip_filter}
    """


def get_yesterday_query(ip_filter, yesterday):
    """Return query for yesterday's traffic statistics."""
    return f"""
        SELECT 
            COUNT(*) as visits_yesterday,
            COUNT(DISTINCT c_ip) as unique_yesterday
        FROM {TABLE}
        WHERE date = DATE '{yesterday}'
            AND c_ip NOT IN {ip_filter}
    """


def get_top_pages_query(ip_filter):
    """Return query for most visited pages."""
    return f"""
        SELECT cs_uri_stem, COUNT(*) as visits
        FROM {TABLE}
        WHERE c_ip NOT IN {ip_filter}
        GROUP BY cs_uri_stem
        ORDER BY visits DESC
        LIMIT 5
    """


def get_geo_query(ip_filter):
    """Return query for geographic distribution."""
    return f"""
        SELECT x_edge_location, COUNT(*) as requests
        FROM {TABLE}
        WHERE c_ip NOT IN {ip_filter}
        GROUP BY x_edge_location
        ORDER BY requests DESC
        LIMIT 10
    """


def get_top_visitors_query(ip_filter):
    """Return query for top visitor IPs."""
    return f"""
        SELECT c_ip, COUNT(*) as visits
        FROM {TABLE}
        WHERE c_ip NOT IN {ip_filter}
        GROUP BY c_ip
        ORDER BY visits DESC
        LIMIT 10
    """


def execute_query(query):
    """Execute Athena query and return results."""
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT_LOCATION}
    )
    
    query_execution_id = response['QueryExecutionId']
    
    for i in range(30):
        status_response = athena_client.get_query_execution(
            QueryExecutionId=query_execution_id
        )
        status = status_response['QueryExecution']['Status']['State']
        
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(1)
    
    if status == 'SUCCEEDED':
        results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        return results['ResultSet']['Rows']
    
    return []


def format_email_report(yesterday, results):
    """Format analytics data into email report."""
    sections = []
    
    sections.append(f"Website Analytics Report")
    sections.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    sections.append("\n" + "=" * 50)
    sections.append("ALL-TIME OVERVIEW")
    sections.append("=" * 50)
    sections.append(format_overview(results['overview']))
    
    sections.append("\n" + "=" * 50)
    sections.append(f"YESTERDAY ({yesterday})")
    sections.append("=" * 50)
    sections.append(format_yesterday(results['yesterday']))
    
    sections.append("\n" + "=" * 50)
    sections.append("TOP PAGES (All Time)")
    sections.append("=" * 50)
    sections.append(format_top_pages(results['top_pages']))
    
    sections.append("\n" + "=" * 50)
    sections.append("GEOGRAPHIC DISTRIBUTION")
    sections.append("=" * 50)
    sections.append(format_geo_distribution(results['geo_distribution']))
    
    sections.append("\n" + "=" * 50)
    sections.append("TOP VISITORS")
    sections.append("=" * 50)
    sections.append(format_top_visitors(results['top_visitors']))
    
    sections.append(f"\nFiltered IPs: {len(FILTERED_IPS)} IP(s) excluded from stats")
    
    return "\n".join(sections)


def format_overview(data):
    """Format overview statistics."""
    if len(data) > 1:
        total = data[1]['Data'][0]['VarCharValue']
        unique = data[1]['Data'][1]['VarCharValue']
        days = data[1]['Data'][2]['VarCharValue']
        return f"Total Visits: {total}\nUnique Visitors: {unique}\nDays Tracked: {days}"
    return "No traffic data available."


def format_yesterday(data):
    """Format yesterday's statistics."""
    if len(data) > 1:
        visits = data[1]['Data'][0]['VarCharValue']
        unique = data[1]['Data'][1]['VarCharValue']
        return f"Visits: {visits}\nUnique Visitors: {unique}"
    return "No traffic yesterday."


def format_top_pages(data):
    """Format top pages list."""
    if len(data) > 1:
        lines = []
        for row in data[1:]:
            uri = row['Data'][0].get('VarCharValue', 'N/A')
            visits = row['Data'][1].get('VarCharValue', '0')
            lines.append(f"{uri}: {visits} visits")
        return "\n".join(lines)
    return "No page data."


def format_geo_distribution(data):
    """Format geographic distribution list."""
    if len(data) > 1:
        lines = []
        for row in data[1:]:
            location = row['Data'][0].get('VarCharValue', 'N/A')
            requests = row['Data'][1].get('VarCharValue', '0')
            lines.append(f"{location}: {requests} requests")
        return "\n".join(lines)
    return "No geographic data."


def format_top_visitors(data):
    """Format top visitors list."""
    if len(data) > 1:
        lines = []
        for row in data[1:]:
            ip = row['Data'][0].get('VarCharValue', 'N/A')
            visits = row['Data'][1].get('VarCharValue', '0')
            lines.append(f"{ip}: {visits} visits")
        return "\n".join(lines)
    return "No visitor data."