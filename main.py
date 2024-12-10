import pandas as pd
from datetime import datetime
# import mysql.connector
from sqlalchemy import create_engine, URL

from dotenv import load_dotenv
import os
from grab_data import grab_books, grab_list_details

load_dotenv()
API_KEY = os.getenv('api_key')

def connect():
    """Connect to MySQL database"""

    # # create connection to MySQL database using mysql.connector
    # mydb = mysql.connector.connect(
    #     host = os.getenv('host'),
    #     user = 'admin',
    #     password = os.getenv('password'),
    #     database ='nytBestSellers'
    # )

    username = 'root'
    password = os.getenv('password')
    host = os.getenv('host')
    database= 'nyt_best_sellers'

    engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(user = username, pw = password,
                           host = host, db = database))

    df = pd.DataFrame({"col1":[1,2], "col2": [3,4]})

    df.to_sql('tablel1', engine, if_exists = 'replace', index =False)

    return engine


def store_lists_info():
    engine = connect()

    list_details = grab_list_details(API_KEY)
    print(list_details)

    list_details.to_sql(name='lists_info', con=engine, if_exists='append', index=False)

def execute():

    # generate a list of dates between a specified range
    dates = pd.date_range(start='01/01/2000',end=  datetime.today(), freq = 'W-THU')

    # grab names of all bestseller lists

    best_sellers = grab_books('2024-10-24', 'hardcover-fiction', API_KEY)

    # # initialize best sellers dataframe
    # best_sellers = pd.DataFrame({"title": [], "rank": [], "prev rank": [], "num weeks": [],
    #       "author": [], "publisher": [], "description": [], "dagger": [], "amazon url": []})
    

    # for day in dates[::-1]:
    #     print(day.strftime('%Y-%m-%d'))
    #     books = grab_books(day.strftime('%Y-%m-%d'),'hardcover-fiction', API_KEY)
    #     best_sellers._append(books)

    print(best_sellers)
   
if __name__ == "__main__":
    connect()

