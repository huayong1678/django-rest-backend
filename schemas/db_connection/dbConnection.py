from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

def getEngine(connection_data):
  if connection_data[0] == "PG":
    connection_string = f'postgresql+psycopg2://{connection_data[1]}:{connection_data[2]}@{connection_data[3]}/{connection_data[4]}'
    return connection_string
  else:
    pass

def testConnection(connection_data):
  connection_string = getEngine(connection_data)
  try:
    alchemyEngine   = create_engine(connection_string, pool_recycle=3600)
    dbConnection    = alchemyEngine.connect()
    dbConnection.close()
    return True
  except:
    return False

def sensitiveCensor(df):
  import hashlib
  df_hashed = pd.DataFrame()
  for column in df:
    df[column] = df[column].astype(str)
    df_hashed[column] = df[column].apply(
      lambda x: 
        hashlib.md5(x.encode()).hexdigest()
    )
  return df_hashed

def showData(connection_data):
  try:
    connection_string = getEngine(connection_data)
    alchemyEngine   = create_engine(connection_string, pool_recycle=3600)
    dbConnection    = alchemyEngine.connect()
    # dataFrame       = pd.read_sql(f"select * from \"contacts\"", dbConnection)
    # dataFrame       = pd.read_sql(f"select * from contacts", dbConnection)
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