import pandas as pd
from datetime import datetime
# import mysql.connector
from sqlalchemy import create_engine, text

from dotenv import load_dotenv
import os
from grab_data import grab_books, grab_list_details

load_dotenv()
API_KEY = os.getenv('api_key')

def connect():
    """Connect to MySQL database"""

    username = 'root'
    password = os.getenv('password')
    host = os.getenv('host')
    database= 'nyt_best_sellers'

    engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(user = username, pw = password,
                           host = host, db = database))

    # df = pd.DataFrame({"col1":[1,2], "col2": [3,4]})

    # df.to_sql('tablel1', engine, if_exists = 'replace', index =False)

    return engine


def store_lists_info():
    engine = connect()

    # using api key to access nyt data
    list_details = grab_list_details(API_KEY)

    # storing list_details in a table called lists_info
    list_details.to_sql('lists_info', con=engine, if_exists='append', index=False)

def execute():

    # connect to database
    engine = connect()
    cnx = engine.connect()

    # generate a list of dates between a specified range
    dates = pd.date_range(start='01/01/2000',end=  datetime.today(), freq = 'W-THU')

    # grab names of all bestseller lists
    query = "SELECT type_ from lists_info"
    type_ = pd.read_sql(query, con = cnx)
    list = type_["type_"].tolist()

    print(list)

    # best_sellers = grab_books('2024-10-24', 'hardcover-fiction', API_KEY)

    # # initialize best sellers dataframe
    best_sellers = pd.DataFrame({"title": [], "rank": [], "prev rank": [], "num weeks": [],
          "author": [], "publisher": [], "description": [], "dagger": [], "amazon url": []})
    

    # for day in dates[::-1]:
    #     print(day.strftime('%Y-%m-%d'))
    #     books = grab_books(day.strftime('%Y-%m-%d'),'hardcover-fiction', API_KEY)
    #     best_sellers._append(books)

    print(best_sellers)
   
if __name__ == "__main__":
    execute()