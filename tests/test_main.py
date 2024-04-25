import unittest
from unittest.mock import patch
from moto import mock_aws
import boto3
import json
from lambda_handler import main

class TestLambdaHandler(unittest.TestCase):
    @classmethod
    @mock_aws
    def setUpClass(cls):
        # Set up variables
        table_name = 'http-crud-tutorial-items'

        # Create a dummy session with dummy credentials
        session = boto3.Session(aws_access_key_id='testing', aws_secret_access_key='testing')

        # Create a mock DynamoDB table.
        cls.dynamodb = session.resource('dynamodb', region_name='us-east-1')

        # Create the DynamoDB table
        cls.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # Initialize the visitor count value in DynamoDB to 0
        table = cls.dynamodb.Table(table_name)
        table.put_item(Item={'id': '1', 'name': 'Test', 'price': 10})

        # Create event only if same for all tests. Define in each test if variable.
        cls.event = {
            'routeKey': 'DELETE /items/{id}',
            'pathParameters': {'id': '1'}
        }

    def test_table_exists(self):
        # Check for table
        pass

    def test_table_name(self):
        # Check table name
        pass

    def test_response_code_200(self):
        # Check response code
        pass

    def test_delete_item(self):
        # Check delete item
        pass

    def test_get_item(self):
        # Check get item
        pass

    def test_scan_table(self):
        # Check scan table
        pass

    def test_put_item(self):
        # Check put item
        pass

if __name__ == '__main__':
    unittest.main()
