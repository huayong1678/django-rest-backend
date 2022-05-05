import sqlalchemy
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from db_handler.dbConnect import *
from db_handler.dbInfo import *
import boto3


def checkTable(connection_data):
    try:
        connection_string = getEngine(connection_data)
        alchemyEngine = create_engine(connection_string, pool_recycle=3600)
        dbConnection = alchemyEngine.connect()
        status = dbConnection.dialect.has_table(
            dbConnection, connection_data[-1])
    finally:
        dbConnection.close()
    return status


def createTable(connection_data, schemas, pk):
    try:
        sql_script = scriptGenerate(connection_data[-1], schemas, pk, "create")
        connection_string = getEngine(connection_data)
        alchemyEngine = create_engine(connection_string, pool_recycle=3600)
        dbConnection = alchemyEngine.connect()
        with dbConnection as connection:
            with connection.begin():
                result = connection.execute(text(sql_script))
            connection.close()
        alchemyEngine.dispose()
        return "created table"
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error

def scriptGenerate(table, schemas, pk, type):
    script = f"CREATE TABLE {table}("
    if type == "create":
        for k, v in schemas.items():
            if k == pk:
                script += f"{k} {v} PRIMARY KEY, "
            elif k == list(schemas.keys())[-1]:
                script += f"{k} {v});"
            else:
                script += f"{k} {v} ,"
    else:
        pass
    return script
    # print(table)
    # print(schemas)
    # print(pk)
