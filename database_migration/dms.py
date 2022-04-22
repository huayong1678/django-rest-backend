from db_handler.dbConnect import *
import argparse
import logging
import subprocess
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

AWS_BUCKET_NAME = 'etl-dump-bucket-df12f0'

def dumpDatabase(connection_data, owner_id):
    start = time.time()
    AWS_BUCKET_PATH = f'{owner_id}/'
    dt_string = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    # u = uuid.uuid4()
    # s = str(shortuuid.encode(u))
    file_name = f'{dt_string}.csv'
    file_path = f"{os.getcwd()}/tmp/{file_name}"
    os.environ["PGPASSWORD"] = str(connection_data[2])
    tmp = [connection_data[0], connection_data[1], connection_data[2],
           connection_data[3], connection_data[5], False, connection_data[-1]]
    connection_string = getEngine(tmp)
    connection_string = connection_string[:10:] + connection_string[19:]
    try:
        # prepareLogTable()
        process = subprocess.Popen(['psql', connection_string, '--echo-all', '-c',
                                    f'\\copy (SELECT * FROM contacts) to  \'{file_path}\' csv header;'], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        # print(output)
        del os.environ["PGPASSWORD"]
        multi_part_upload_with_s3(file_path, file_name, AWS_BUCKET_PATH)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print("The file does not exist")
        end = time.time()
        psutil.cpu_percent()
        psutil.virtual_memory()
        dict(psutil.virtual_memory()._asdict())
        print("\nMemory Usage: " + str(psutil.virtual_memory().used/1000000) + " MB(s).")
        # print("\nMemory Usage: " + str(psutil.virtual_memory().percent) + " %")
        # print("Memory Available :" + str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total) + " %")
        print("Execution Time: " + str(end-start) + " second(s)")
    except:
        return HttpResponse(status=500)


def migrate_log():
    pass


def multi_part_upload_with_s3(file_path, file_name, bucket_path):
    s3 = boto3.resource('s3')
    s3_config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10,
                               multipart_chunksize=1024 * 25, use_threads=True)
    s3.meta.client.upload_file(file_path, AWS_BUCKET_NAME, bucket_path+file_name, ExtraArgs={
                               'ACL': 'private', 'ContentType': 'text/plain', 'ServerSideEncryption': 'AES256'}, Config=s3_config, Callback=ProgressPercentage(file_path))


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
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
