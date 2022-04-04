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
            {
                'AttributeName': 'OWNER_ID',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'OWNER_ID',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'UUID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    dynamoCheck()


def dynamoCreateTransform(data, payload):
    response = dynamoCheck()
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    # print(payload['id'], type(payload['id']))
    # print(s, type(s))
    OWNER_ID = str(payload['id'])
    try:
        response = dynamodb.put_item(
            TableName = TABLE_NAME,
            Item={
                'OWNER_ID': {'N': OWNER_ID},
                'UUID': {'S': s}
            }
        )
        return {"HTTPStatusCode": response['ResponseMetadata']['HTTPStatusCode']}
    except ClientError as ce:
        # return ce.response
        return {ce.response['Error']['Code']: ce.response['Error']['Message']}

def dynamoListTransform():
    pass
