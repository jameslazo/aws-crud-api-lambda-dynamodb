import unittest
from unittest.mock import patch
from moto import mock_aws
import boto3
import os
import json



@mock_aws
class TestLambdaHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up variables
        cls.table_name = 'http-crud-tutorial-items'
        cls.region = os.environ["AWS_DEFAULT_REGION"]

        # Create a dummy session with dummy credentials
        # cls.session = boto3.Session(aws_access_key_id='testing', aws_secret_access_key='testing')
        from botocore.config import Config
        cls.config = Config(proxies={"https": "http://localhost:5005"})
        # Create a mock DynamoDB table.
        # cls.dynamodb = cls.session.resource('dynamodb', region_name='us-east-1')
        cls.client = boto3.client("dynamodb", region_name=cls.region, config=cls.config, verify=False)
        cls.dynamodb = boto3.resource("dynamodb", region_name=cls.region, config=cls.config, verify=False)

        # Create the DynamoDB table
        cls.dynamodb.create_table(
            TableName=cls.table_name,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )

        # Initialize the visitor count value in DynamoDB to 0
        cls.table = cls.dynamodb.Table(cls.table_name)
        cls.table.put_item(Item={'id': '1', 'name': 'Test', 'price': 10})

        # Initialize event
        cls.event = {
            'routeKey': ""
        }

    def test_table_exists(self):
        # Check for table
        self.assertTrue(self.table)

    def test_table_name(self):
        # Check table name
        self.assertIn(self.table_name, self.table.name)

    def test_response_code_200(self):
        # update event key
        eventkey = "GET /items/1"
        self.event['routeKey'] = eventkey

        # import function within test after mock services are created
        from lambda_handler import main
        response = main.lambda_handler(self.event, None)

        # Check if the response code is 200
        self.assertEqual(response['statusCode'], 200)

    def test_delete_item(self):
        # update event key
        # event = {}
        # eventkey = "DELETE /items/{id}"
        # self.event['routeKey'] = eventkey

        # import function within test after mock services are created
        # from lambda_handler import main
        # main.lambda_handler(self.event, None)

        # Check delete item
        # self.assertIsNone()
        pass

    def test_get_item(self):
        # Check get item
        pass

    @mock_aws
    def test_scan_table(self):
        # update event key
        eventkey = "GET /items"
        self.event['routeKey'] = eventkey
        # table = self.dynamodb.Table(self.table_name)
        response = self.client.scan(TableName=self.table_name)
        self.assertTrue('Items' in response)
        print("Scanned items: ", response['Items'])

        # import function within test after mock services are created
        # from lambda_handler import main
        # response = main.lambda_handler(self.event, None)

        # Check scan table
        # print(response['body'])
        # self.assertEqual(response['body'], 200)

    def test_put_item(self):
        # Check put item
        pass

    def test_keyerror(self):
        # Check KeyError exception
        pass

if __name__ == '__main__':
    unittest.main()
