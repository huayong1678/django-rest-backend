import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from db_handler.dbConnect import getEngine, sensitiveCensor

def showData(connection_data):
  try:
    connection_string = getEngine(connection_data)
    alchemyEngine   = create_engine(connection_string, pool_recycle=3600)
    dbConnection    = alchemyEngine.connect()
    sql_script = "select * from " + connection_data[-1]
    dataFrame       = pd.read_sql(str(sql_script), dbConnection)
    pd.set_option('display.expand_frame_repr', False)
    if connection_data[-2] == True:
      df = sensitiveCensor(dataFrame)
    else:
      df = dataFrame
    dbConnection.close()
    return df.head(10)
  except SQLAlchemyError as e:
    error = str(e.__dict__['orig'])
    return error

def getSchema(connection_data):
  try:
    connection_string = getEngine(connection_data)
    alchemyEngine   = create_engine(connection_string, pool_recycle=3600)
    dbConnection    = alchemyEngine.connect()
    md = sqlalchemy.MetaData()
    table = sqlalchemy.Table(connection_data[-1], md, autoload=True, autoload_with=dbConnection)
    columns = table.c
    schema = dict()
    for c in columns:
      schema[c.name] = str(c.type)
    dbConnection.close()
    pd.set_option('display.expand_frame_repr', False)
    return schema
  except SQLAlchemyError as e:
    error = str("sqlalchemy.exc.NoSuchTableError")
    return error