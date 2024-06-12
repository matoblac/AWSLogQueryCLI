# tests/test_main.py

import unittest
from unittest.mock import patch
from moto import mock_logs, mock_cloudformation
import boto3
from main import list_log_groups, get_timestamps, describe_cloudformation_stack

class TestAWSLogChecker(unittest.TestCase):

    @mock_logs
    def test_list_log_groups(self):
        client = boto3.client('logs', region_name='us-east-1')
        client.create_log_group(logGroupName='test-log-group')
        
        log_groups = list_log_groups()
        self.assertIn('test-log-group', log_groups)

    def test_get_timestamps(self):
        # Test with a valid date
        time_str = "12-15-2023 14:30"
        start_time, end_time = get_timestamps(time_str)
        
        self.assertIsInstance(start_time, int)
        self.assertIsInstance(end_time, int)
        self.assertEqual(end_time - start_time, 1800)  # 30 minutes difference

    def test_invalid_time_format(self):
        # Test with an invalid date
        with self.assertRaises(SystemExit):
            get_timestamps("invalid-date")

    @mock_cloudformation
    @patch('builtins.input', return_value='test-stack')
    def test_describe_cloudformation_stack(self, mock_input):
        client = boto3.client('cloudformation', region_name='us-east-1')
        client.create_stack(
            StackName='test-stack',
            TemplateBody='{"Resources": {}}'
        )
        response = client.describe_stack_events(StackName='test-stack')

        with patch('main.boto3.client', return_value=client):
            describe_cloudformation_stack()

        reasons = [event['ResourceStatusReason'] for event in response['StackEvents']]
        self.assertIsInstance(reasons, list)

if __name__ == '__main__':
    unittest.main()
