import boto3
import datetime
import time
import json
import sys

def get_timestamps(time_str):
    try:
        # Parse the input time string
        input_time = datetime.datetime.strptime(time_str, "%m-%d-%Y %H:%M")
    except ValueError:
        print("Time needs to be in the format MM-DD-YYYY HH:MM")
        sys.exit(1)
    
    # Calculate 30 minutes before the input time
    end_time = int(input_time.timestamp())
    start_time = end_time - 1800  # 30 minutes in the past
    return start_time, end_time

def list_log_groups():
    client = boto3.client('logs')
    response = client.describe_log_groups()
    log_groups = [log_group['logGroupName'] for log_group in response['logGroups']]
    return log_groups

def start_log_query(log_group, log_filter, limit, time_str):
    start_time, end_time = get_timestamps(time_str)
    client = boto3.client('logs')
    query_string = f'fields @message | filter @message like {log_filter} | limit {limit}'
    
    response = client.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query_string
    )
    query_id = response['queryId']
    print(f"Query started (query id: {query_id}) for log group: {log_group} with filter: {log_filter}, please hold ...")
    
    time.sleep(5)  # Give it some time to query
    
    result = client.get_query_results(queryId=query_id)
    print(json.dumps(result, indent=2))

def query_multiple_log_groups(time_str):
    log_groups = list_log_groups()
    
    print("Available log groups:")
    for i, log_group in enumerate(log_groups):
        print(f"{i}: {log_group}")
    
    log_group_numbers = input("Enter the log group numbers separated by space: ").split()
    log_group_numbers = [int(num) for num in log_group_numbers]
    
    log_filter = input("Enter the log levels to filter (e.g., /ERROR/, /ERROR/WARN/, /ERROR/WARN/INFO/):\nYou can also add other query strings enclosed with '/' (e.g., /ERROR/ /requestId/): ")
    
    if not all([part.startswith('/') and part.endswith('/') for part in log_filter.split()]):
        print("Invalid format for log filter. Please follow the format (e.g., /ERROR/, /ERROR/WARN/, /ERROR/requestId/).")
        return
    
    limit = input("Enter the maximum number of log entries to retrieve (e.g., 20): ")
    
    for num in log_group_numbers:
        log_group = log_groups[num]
        start_log_query(log_group, log_filter, limit, time_str)

def describe_cloudformation_stack():
    client = boto3.client('cloudformation')
    stack_name = input("Enter the CloudFormation stack name: ")
    
    response = client.describe_stack_events(
        StackName=stack_name,
        MaxItems=15
    )
    
    reasons = [event['ResourceStatusReason'] for event in response['StackEvents']]
    print(reasons)

def display_help():
    help_text = """
AWS Log Checker Help
====================
This script allows you to check AWS CloudFormation and CloudWatch logs for errors.

Usage:
python main.py MM-DD-YYYY HH:MM

Menu Options:
1. CloudFormation Logs - Check the CloudFormation stack events for errors.
2. CloudWatch Logs - Query CloudWatch log groups for errors in the last 30 minutes.
3. Help - Display this help menu.

For CloudWatch Logs:
  - The script will list all available log groups.
  - You can enter the log group numbers separated by space to query multiple log groups.
  - You need to specify log levels to filter (e.g., /ERROR/, /ERROR/WARN/, /ERROR/WARN/INFO/).
  - You can also add other query strings enclosed with '/' (e.g., /ERROR/ /requestId/).
  - You can specify the maximum number of log entries to retrieve.

Example Workflow:
1. Run the script: python main.py MM-DD-YYYY HH:MM
2. Choose '2' for CloudWatch Logs.
3. The script will list available log groups.
4. Enter the log group numbers you want to query (e.g., '0 1').
5. Enter the log levels to filter (e.g., /ERROR/ /requestId/).
6. Enter the maximum number of log entries to retrieve (e.g., 20).
"""
    print(help_text)

def display_menu():
    print("Welcome to the AWS Log Checker!")
    print("===============================")
    print("1. CloudFormation Logs")
    print("2. CloudWatch Logs")
    print("3. Help")
    print("===============================")
    choice = input("Choose an option (1, 2, or 3): ")
    return choice

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py MM-DD-YYYY HH:MM")
        sys.exit(1)
    
    time_str = sys.argv[1]
    
    choice = display_menu()
    
    if choice == '1':
        print("You chose CloudFormation Logs")
        describe_cloudformation_stack()
    elif choice == '2':
        print("You chose CloudWatch Logs")
        query_multiple_log_groups(time_str)
    elif choice == '3':
        display_help()
    else:
        print("Invalid choice. Exiting.")
        exit(1)

if __name__ == '__main__':
    main()
