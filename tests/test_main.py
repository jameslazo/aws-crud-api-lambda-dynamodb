import unittest
from moto import mock_aws
import boto3
from lambda_handler import main
import os



table_name = 'http-crud-tutorial-items'
region = os.environ["AWS_DEFAULT_REGION"]
context = {}

@mock_aws
def spinup_ddb(operation="exists"):
    # Create boto3 session
    boto3.setup_default_session()

    # Create DDB client
    client = boto3.client("dynamodb", region_name=region)

    # Create the DDB table
    client.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'partitionKey', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'partitionKey', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    # Branch test paths
    if operation == "exists":
        return client.describe_table(TableName=table_name)
    elif operation == "get/delete":
        client.put_item(
            TableName=table_name,
            Item={
                'partitionKey': {'S': 'id'},
                'name': {'S': 'Test'},
                'price': {'N': '10'}
            }
        )

@mock_aws
class TestLambdaHandler(unittest.TestCase):

    def test_table_exists(self):
        # mock table
        response = spinup_ddb()
        # Check for table
        self.assertTrue(response)

    def test_table_name(self):
        # mock table
        tablename = spinup_ddb()["Table"]["TableName"]
        # Check table name
        self.assertIn(tablename, table_name)

    def test_response_code_200(self):
        # initialize event
        event = {}
        eventkey = "GET /items/id"
        event['routeKey'] = eventkey

        # mock resources
        spinup_ddb("get/delete")

        # call function within test after mock services are created
        
        response = main.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)

    def test_delete_item(self):
        # initialize event
        event = {}
        eventkey = "DELETE /items/id"
        event['routeKey'] = eventkey

        # mock resources
        spinup_ddb("get/delete")

        # call function within test after mock services are created        
        response = main.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        # self.assertIsNone()

    def test_get_item(self):
        # initialize event
        event = {}
        eventkey = "GET /items/id"
        event['routeKey'] = eventkey

        # mock resources
        spinup_ddb("get/delete")

        # call function within test after mock services are created
        response = main.lambda_handler(event, context)
        self.assertEqual(response['body'], {'partitionKey': {'S': 'id'}, 'name': {'S': 'Test'}, 'price': {'N': '10'}})

    def test_scan_table(self):
        # initialize event
        event = {}
        eventkey = "GET /items"
        event['routeKey'] = eventkey

        # mock resources
        spinup_ddb("get/delete")

        # call function within test after mock services are created
        response = main.lambda_handler(event, context)
        self.assertEqual(response['body'], [{'partitionKey': {'S': 'id'}, 'name': {'S': 'Test'}, 'price': {'N': '10'}}])

    def test_put_item(self):
        # initialize event
        event = {}
        eventkey = "PUT /items/id"
        event['routeKey'] = eventkey
        event['body'] = {
            'name': {'S': 'PutTest'},
            'price': {'N': '50'}
        }

        # mock resources
        spinup_ddb("put")

        # call function within test after mock services are created
        response = main.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)

    def test_keyerror(self):
        event = {}
        # call function within test after mock services are created
        response = main.lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 400)

if __name__ == '__main__':
    unittest.main()
