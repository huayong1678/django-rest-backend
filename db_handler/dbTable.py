import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from db_handler.dbConnect import getEngine
import boto3


def createSchemaPattern(connection_data):
    connection_string = getEngine(connection_data)
    alchemyEngine = create_engine(connection_string, pool_recycle=3600)
    dbConnection = alchemyEngine.connect()
    dbConnection.close()
    pass


def createTable():
    pass
