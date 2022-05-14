from db_handler.dbConnect import *
import argparse
import logging
import subprocess
from subprocess import PIPE,Popen
import os
import sys
import uuid
import shortuuid
import tempfile
from pathlib import Path
from tempfile import mkstemp
import threading
import configparser
import gzip
import boto3
from botocore.config import Config
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import NoCredentialsError, ClientError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
from shutil import move
from db_handler.dbConnect import getEngine
from django.http import HttpResponse
import time
import psutil
import pandas as pd

if 'S3_BUCKET' in os.environ:
    AWS_BUCKET_NAME = os.environ['S3_BUCKET']
else:
    AWS_BUCKET_NAME = 'etl-dump-bucket-d56550'
dt_string = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
file_name = f'{dt_string}'
if 'IS_EFS_EXIST' in os.environ:
    file_path = f"/usr/share/tmp/{file_name}"
else:
    file_path = f"{os.getcwd()}/tmp/{file_name}"

def exportData(connection_data, owner_id, dynamo_data):
    AWS_BUCKET_PATH = f'{owner_id}/'
    # print(connection_data)
    os.environ["PGPASSWORD"] = str(connection_data[2])
    # connection_string = f'postgresql+psycopg2://{connection_data[1]}:{connection_data[2]}@{connection_data[3]}:{connection_data[-1]}/{connection_data[4]}'
    # tmp = [connection_data[0], connection_data[1], connection_data[2],
    #        connection_data[3], connection_data[4], False, connection_data[-1]]
    connection_string = getEngine(connection_data)
    # print("BF Strip: " +connection_string)
    connection_string = connection_string[:10:] + connection_string[19:]
    # print("AF Strip: " +connection_string)
    try:
        print("Start Exporting...")
        start = time.time()
        schemas, pk = list(), dynamo_data['Item']['PK']
        # print(dynamo_data['Item']['SCHEMAS'])
        # schemas.append(pk)
        for i in dynamo_data['Item']['SCHEMAS']:
            for k,v in i.items():
                if k == dynamo_data['Item']['PK']:
                    pass
                else:
                    schemas.append(k)
        # for k,v in dynamo_data['Item']['SCHEMAS'].items():
        #     schemas.append(k)
        schemas = ', '.join(schemas)
        # print(schemas)
        process = subprocess.Popen(['psql', connection_string, '--echo-all', '-c',
                                    f'\\copy (SELECT {schemas} FROM {connection_data[-2]}) to  \'{file_path}.csv\' csv header;'], stdout=subprocess.PIPE)
        process.communicate()[0]
        # get output from process "Something to print"
        # one_line_output = process.stdout.readline()
        # print(one_line_output)
        end = time.time()
        print("Execution Time: " + str(end-start) + " second(s)")
        if os.path.getsize(f'{file_path}.csv')/1000000 >= 1000:
            file_size = str(os.path.getsize(f'{file_path}.csv')/1000000000) + " GB(s)"
        else:
            file_size = str(os.path.getsize(f'{file_path}.csv')/1000000) + " MB(s)"
        print(file_size)
        print("Start Uploading...")
        multi_part_upload_with_s3(
            file_path + ".csv", file_name, AWS_BUCKET_PATH)
        # psutil.cpu_percent()
        # psutil.virtual_memory()
        # dict(psutil.virtual_memory()._asdict())
        # print("\nMemory Usage: " +
        #       str((psutil.virtual_memory().used/1000000)/1000) + " GB(s)")
        # print("Memory Usage: " + str(psutil.virtual_memory().percent) + " %")
        # return [connection_string, (file_path + '.csv'), connection_data[-1]]
        df = pd.read_csv(f'{file_path}.csv')
        return [0, str(file_path + '.csv'), {"rows": (str(len(df.index)) + ' row(s)'), "size": file_size, "time": (str(end-start) + " second(s)")}]
    except sqlalchemy.exc.SQLAlchemyError as e:
        return str(e)


def importData(export_data, path, dynamo_data):
    connection_string = getEngine(export_data)
    # print("BF Strip: " +connection_string)
    connection_string = connection_string[:10:] + connection_string[19:]
    # print("AF Strip: " +connection_string)
    start = time.time()
    schemas = []
    print("Start Importing...")
    # print(export_data)
    # print(path)
    for i in dynamo_data['Item']['SCHEMAS']:
        for k,v in i.items():
            if k == dynamo_data['Item']['PK']:
                pass
            else:
                schemas.append(k)
    # for k,v in dynamo_data['Item']['SCHEMAS'].items():
    #     schemas.append(k)
    schemas = ', '.join(schemas)
    try:
        # print(export_data[-2])
        df = pd.read_csv(path)
        process = subprocess.Popen(['psql', connection_string, '--echo-all', '-c',
                                f'\\copy {export_data[-2]}({schemas}) FROM \'{path}\' DELIMITER \',\' CSV HEADER;'], stdout=PIPE)
        process.communicate("n\n")[0]
        process = subprocess.Popen(['psql', connection_string, '--echo-all', '-c', f'SELECT reltuples::bigint AS estimate FROM   pg_class WHERE  oid = \'{export_data[-2]}\'::regclass;'])
        process.communicate("n\n")[0]
        try:
            if os.path.getsize(f'{file_path}.csv')/1000000 >= 1000:
                file_size = str(os.path.getsize(path)/1000000000) + " GB(s)"
            else:
                file_size = str(os.path.getsize(path)/1000000) + " MB(s)"
        except:
            file_size = 0
        end = time.time()
        return {"rows": (str(len(df.index)) + ' row(s)'), "size": file_size, "time": (str(end-start) + " second(s)")}
    except sqlalchemy.exc.SQLAlchemyError as e:
        return str(e)
    del os.environ["PGPASSWORD"]
    print("Execution Time: " + str(end-start) + " second(s)")


def removeLocalData(file_path):
    try:
        os.remove(file_path)
        return "success"
    except:
        return "The file does not exist."


def migrate_log():
    pass


def multi_part_upload_with_s3(file_path, file_name, bucket_path):
    start = time.time()
    s3 = boto3.resource('s3')
    s3_config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                               multipart_chunksize=1024 * 25, use_threads=True)
    s3.meta.client.upload_file(file_path, AWS_BUCKET_NAME, bucket_path+file_name+".csv", ExtraArgs={
                               'ACL': 'private', 'ContentType': 'text/plain', 'ServerSideEncryption': 'AES256'}, Config=s3_config, Callback=ProgressPercentage(file_path))
    end = time.time()
    print("\nExecution Time: " + str(end-start) + " second(s)")


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            # sys.stdout.write(
            #     "\r%s  %s / %s  (%.2f%%)" % (
            #         self._filename, self._seen_so_far, self._size,
            #         percentage))
            sys.stdout.write(
                "\r%s / %s  (%.2f%%)" % (
                    self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
