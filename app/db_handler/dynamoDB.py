import boto3
from botocore.config import Config
import json
import uuid
import shortuuid
from botocore.exceptions import ClientError
import os

config = Config(
    connect_timeout=3, read_timeout=3,
    retries={'max_attempts': 3})
if 'IS_DYNAMO_EXIST' in os.environ:
    dynamodb = boto3.client('dynamodb', config=config)
else:
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
            dynamoTransformTable()
            dynamoLogTable()
            return dynamoCheck()
        else:
            # print("Unknown exception occurred while querying for the " + TABLE_NAME + " table. Printing full error:")
            # pprint.pprint(ce.response)
            return ce.response['Error']['Code']


def dynamoTransformsTable():
    table = dynamodb.create_table(
        TableName="Transforms",
        KeySchema=[
            {
                'AttributeName': 'UUID',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'UUID',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.wait_until_exists()
    dynamoCheck()


# def dynamoLogTable():
#     dynamo_config = Config(
#         connect_timeout=3, read_timeout=3, retries={'max_attempts': 3})
#     if 'IS_DYNAMO_EXIST' in os.environ:
#         dynamodb_client = boto3.client('dynamodb', config=dynamo_config)
#     else:
#         dynamodb_client = boto3.client('dynamodb', endpoint_url='http://localhost:8007', config=dynamo_config)
#     existing_tables = dynamodb_client.list_tables()['TableNames']
#     # print(existing_tables)
#     try:
#         table = dynamodb_client.create_table(
#             TableName='MigrationLogs',
#             KeySchema=[
#                 {
#                     'AttributeName': 'MID',
#                     'KeyType': 'HASH'
#                 }
#             ],
#             AttributeDefinitions=[
#                 {
#                     'AttributeName': 'MID',
#                     'AttributeType': 'S'
#                 }
#             ],
#             ProvisionedThroughput={
#                 'ReadCapacityUnits': 1,
#                 'WriteCapacityUnits': 1
#             }
#         )
#         table.wait_until_exists()
#     except ClientError as ce:
#         print(ce.response)


def dynamoCreateTransform(data, payload):
    response = dynamoCheck()
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    TAGS, SCRIPTS, SCHEMAS, pk, test = [], [], {}, data['pk'], []
    TAGS.append(data['tags'])
    if len(data['scripts']) != 0:
        for item in data['scripts']:
            SCRIPTS.append(item)
    else:
        SCRIPTS = [""]
    # for item in data['schemas'].items():
    #     # SCHEMAS.append(item)
    # SCHEMAS = data['schemas']
    for k, v in data['schemas'].items():
        # SCHEMAS[k] = {'S': v}
        test.append({'M': {k: {'S': v}}})
    # print(test)
    # print(SCHEMAS)
    # for i in test:
    #     for k, v in i.items():
    #         for kk, vv in v.items():
    #             print(kk, vv)
    OWNER_ID = str(payload['id'])
    try:
        response = dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'OWNER_ID': {'N': OWNER_ID},
                'UUID': {'S': s},
                'TAGS': {'SS': TAGS},
                # 'SCRIPTS': {'SS': SCRIPTS}, 
                # 'SCHEMAS': {'M': SCHEMAS},
                'SCHEMAS': {'L': test},
                'PK': {'S': pk},
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
    # response = table.get_item(
    #     Key={'UUID': data['uuid'], 'OWNER_ID': data['owner']})
    response = table.get_item(
        Key={'UUID': data['uuid']})
    response['id'] = data['id']
    return response


def dynamoUpdateTransform(data, payload, uuid, id):
    response = dynamoCheck()
    # u = uuid.uuid4()
    # s = shortuuid.encode(u)
    TAGS, SCRIPTS, SCHEMAS, PK = [], [], [], data['pk']
    TAGS.append(data['tags'])
    if len(data['scripts']) != 0:
        for item in data['scripts']:
            SCRIPTS.append(item)
    else:
        SCRIPTS = [""]
    for k, v in data['schemas'].items():
        # SCHEMAS[k] = {'S': v}
        SCHEMAS.append({'M': {k: {'S': v}}})
    OWNER_ID = str(payload['id'])
    try:
        dynamodb = boto3.resource(
            'dynamodb', endpoint_url='http://localhost:8007', config=config)
        table = dynamodb.Table('Transforms')
        table.update_item(
            Key={
                'UUID': str(uuid),
                # 'OWNER_ID': payload['id']
            },
            UpdateExpression="SET TAGS=:val1, SCHEMAS=:val2, PK=:val3, SCRIPTS=:val4",
            ExpressionAttributeValues={
                ':val1': TAGS,
                ':val2': SCHEMAS,
                ':val3': PK,
                ':val4': SCRIPTS,
            },
        )
        data = {'uuid': uuid, 'owner': payload['id'], 'id': id}
        response = dynamoGetTransform(data)
        return response
    except ClientError as ce:
        return {ce.response['Error']['Code']: ce.response['Error']['Message']}
