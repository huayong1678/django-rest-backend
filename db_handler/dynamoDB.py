import boto3
from botocore.config import Config
import json
import uuid
import shortuuid
from botocore.exceptions import ClientError

config = Config(
    connect_timeout=3, read_timeout=3,
    retries={'max_attempts': 3})
dynamodb = boto3.client(
    'dynamodb', endpoint_url='http://localhost:8007', config=config)
TABLE_NAME = "Transforms"


def dynamoCheck():
    try:
        response = dynamodb.describe_table(TableName=TABLE_NAME)
        return {"TableStatus": response['Table']['TableStatus']}
    except ClientError as ce:
        print(ce.response)
        if ce.response['Error']['Code'] == 'ResourceNotFoundException':
            # print("Table " + TABLE_NAME + " does not exist. Create the table first and try again.")
            dynamoCreateTable(TABLE_NAME)
            return dynamoCheck()
        else:
            # print("Unknown exception occurred while querying for the " + TABLE_NAME + " table. Printing full error:")
            # pprint.pprint(ce.response)
            return ce.response['Error']['Code']


def dynamoCreateTable(TABLE_NAME):
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'UUID',
                'KeyType': 'HASH'
            },
            # {
            #     'AttributeName': 'OWNER_ID',
            #     'KeyType': 'RANGE'
            # },
            # {
            #     'AttributeName': 'TAG',
            #     'KeyType': 'RANGE'
            # }
        ],
        AttributeDefinitions=[
            # {
            #     'AttributeName': 'OWNER_ID',
            #     'AttributeType': 'N'
            # },
            {
                'AttributeName': 'UUID',
                'AttributeType': 'S'
            },
            # {
            #     'AttributeName': 'TAGS',
            #     'AttributeType': 'SS'
            # }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.wait_until_exists()
    dynamoCheck()


def dynamoCreateTransform(data, payload):
    response = dynamoCheck()
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    TAGS, SCRIPTS, SCHEMAS = [], [], {}
    TAGS.append(data['tags'])
    if len(data['scripts']) != 0:
        for item in data['scripts']:
            SCRIPTS.append(item)
    else:
        SCRIPTS = [""]
    # for item in data['schemas'].items():
    #     # SCHEMAS.append(item)
    #     print(item)
    # SCHEMAS = data['schemas']
    # print(data['schemas'])
    for k, v in data['schemas'].items():
        # print(k, v)
        SCHEMAS[k] = {'S': v}
        # print(SCHEMAS)
    OWNER_ID = str(payload['id'])
    try:
        response = dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'OWNER_ID': {'N': OWNER_ID},
                'UUID': {'S': s},
                'TAGS': {'SS': TAGS},
                'SCRIPTS': {'SS': SCRIPTS},
                'SCHEMAS': {'M': SCHEMAS}
            }
        )
        return {"HTTPStatusCode": response['ResponseMetadata']['HTTPStatusCode'], "UUID": s}
    except ClientError as ce:
        return {ce.response['Error']['Code']: ce.response['Error']['Message']}


def dynamoGetTransform(data):
    response = dynamoCheck()
    dynamodb = boto3.resource(
        'dynamodb', endpoint_url='http://localhost:8007', config=config)
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(Key={'UUID': data['uuid'], 'OWNER_ID': data['owner']})
    response['id'] = data['id']
    return response
