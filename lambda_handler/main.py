import boto3

dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'http-crud-tutorial-items' 

def lambda_handler(event, context):
    print(event)
    try: 
        route_key = event['routeKey']
        http_method, resource_path = route_key.split(' ')

        if http_method == 'GET':
            if resource_path.startswith('/items/'):
                # Extract id from the resource path
                _, _, id_value = resource_path.split('/')
                return get_item(id_value)
            elif resource_path == '/items':
                return scan_items()
        elif http_method == 'PUT':
            if resource_path.startswith('/items/'):
                # Extract id from the resource path
                _, _, id_value = resource_path.split('/')
                return put_item(id_value, event)
        elif http_method == 'DELETE':
            if resource_path.startswith('/items/'):
                # Extract id from the resource path
                _, _, id_value = resource_path.split('/')
                return delete_item(id_value)
    
    except:
    # If the routeKey doesn't match any supported operation
        return {
            'statusCode': 400,
            'body': 'Unsupported operation'
        }

def get_item(id_value):
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            'partitionKey': {'S': id_value}
        }
    )
    item = response.get('Item')
    if item:
        return {
            'statusCode': 200,
            'body': item
        }
    else:
        return {
            'statusCode': 404,
            'body': 'Item not found'
        }

def scan_items():
    try:
        response = dynamodb.scan(
            TableName=TABLE_NAME
        )
        items = response.get('Items')
        return {
            'statusCode': 200,
            'body': items
        }
    except:
        return {
            'statusCode': 500,
            'body': 'Unexpected '
        }

def put_item(id_value, event):
    # Extract item data from the event body, assuming it's a JSON object
    item_data = event['body']
    if not item_data:
        return {
            'statusCode': 400,
            'body': 'Missing item data'
        }
    
    try:
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'partitionKey': {'S': id_value},
                **item_data
            }
        )
        return {
            'statusCode': 200,
            'body': id_value + ' added'
        }
    except:
        return {
            'statusCode': 404,
            'body': id_value + ' not added'
        }      

def delete_item(id_value):
    try:
        dynamodb.delete_item(
            TableName=TABLE_NAME,
            Key={
                'partitionKey': {'S': id_value}
            }
        )
        return {
            'statusCode': 200,
            'body': id_value + ' deleted'
        }
    except:
        return {
            'statusCode': 404,
            'body': id_value + ' not deleted'
        }
