# import mysql.connector
import time
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

def db_connect():
    """Connect to MySQL database"""

    username = os.getenv('user')
    password = os.getenv('password')
    host = os.getenv('host')
    database= 'nyt_best_sellers'

    engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(user = username, pw = password,
                           host = host, db = database))

    # df = pd.DataFrame({"col1":[1,2], "col2": [3,4]})

    # df.to_sql('tablel1', engine, if_exists = 'replace', index =False)

    return engine


