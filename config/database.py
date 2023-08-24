import pymysql
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def Db_Mysql():
    connection = pymysql.connect(
        host=os.getenv('DATABASE_HOST'),
        port=int(os.getenv('DATABASE_PORT')),
        user=os.getenv('DATABASE_USERNAME'),
        password=os.getenv('DATABASE_PASSWORD'),
        database=os.getenv('DATABASE_NAME')
    )
    return connection


def orm_sql():
    host = os.getenv('DATABASE_HOST')
    port = int(os.getenv('DATABASE_PORT'))
    user = os.getenv('DATABASE_USERNAME')
    password = os.getenv('DATABASE_PASSWORD')
    database = os.getenv('DATABASE_NAME')
    engine = create_engine(
        f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
