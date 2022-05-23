import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import NoResultFound
import pandas as pd
from db_handler.dbConnect import getEngine, sensitiveCensor

def showData(connection_data):
  print(connection_data)
  try:
    connection_string = getEngine(connection_data)
    alchemyEngine   = create_engine(connection_string, pool_recycle=3600)
    dbConnection    = alchemyEngine.connect()
    sql_script = "select * from " + connection_data[-2]
    dataFrame       = pd.read_sql(str(sql_script), dbConnection)
    pd.set_option('display.expand_frame_repr', False)
    if connection_data[-3] == True:
      df = sensitiveCensor(dataFrame)
    else:
      df = dataFrame
    dbConnection.close()
    return [df.head(10), getSchema(connection_data)]
  except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    return error

def getSchema(connection_data):
  try:
    connection_string = getEngine(connection_data)
    alchemyEngine   = create_engine(connection_string, pool_recycle=3600)
    dbConnection    = alchemyEngine.connect()
    md = sqlalchemy.MetaData()
    # print(connection_data)
    table = sqlalchemy.Table(connection_data[-2], md, autoload=True, autoload_with=dbConnection)
    # print(table)
    columns = table.c
    schema = dict()
    for c in columns:
      schema[c.name] = str(c.type)
    dbConnection.close()
    pd.set_option('display.expand_frame_repr', False)
    return schema
  except sqlalchemy.exc.SQLAlchemyError as e:
    return str(e)