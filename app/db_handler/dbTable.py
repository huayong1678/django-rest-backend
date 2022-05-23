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
            dbConnection, connection_data[-2])
        # print(connection_string)
        # print(connection_data)
        # print(status)
        return {"status": status}
    # except:
    #     connection_string = getEngine(connection_data)
    #     alchemyEngine = create_engine(connection_string, pool_recycle=3600)
    #     dbConnection = alchemyEngine.connect()
    #     status = dbConnection.dialect.has_table(
    #         dbConnection, connection_data[-1])
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return {"status": 0, "detail": error}
    dbConnection.close()


def createTable(connection_data, schemas, pk):
    try:
        sql_script = scriptGenerate(connection_data[-2], schemas, pk, "create")
        # print(sql_script)
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
        for i in schemas:
            for k, v in i.items():
                if k == pk:
                    # script += f"{k} {v} PRIMARY KEY, "
                    script += f"{k} SERIAL PRIMARY KEY, "
                elif i == schemas[-1]:
                    script += f"{k} {v});"
                else:
                    script += f"{k} {v} ,"
    return script
    # print(table)
    # print(schemas)
    # print(pk)
