import unittest
from unittest.mock import patch
from moto import mock_aws
import boto3
import json

# Set up variables
table_name = 'http-crud-tutorial-items'

@mock_aws
class TestLambdaHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

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
            'routeKey': 'GET /items'
        }

    def test_table_exists(self):
        # Check for table
        self.assertTrue(self.dynamodb.Table(table_name))

    def test_table_name(self):
        # Check table name
        self.assertIn(table_name, self.dynamodb.Table(table_name).name)

    def test_response_code_200(self):
        # Call the Lambda handler
        # from moto.core import patch_resource
        # patch_resource(dynamodb)
        from lambda_handler import main
        response = main.lambda_handler(self.event, None)

        # Check if the response code is 200
        self.assertEqual(response['statusCode'], 200)

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

    def test_keyerror(self):
        # Check KeyError exception
        pass

if __name__ == '__main__':
    unittest.main()
