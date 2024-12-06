import pandas as pd
from datetime import datetime
import mysql.connector
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os
from grab_data import grab_books, grab_list_names

load_dotenv()
API_KEY = os.getenv('api_key')

# def execute():


def execute():

    # generate a list of dates between a specified range
    dates = pd.date_range(start='01/01/2000',end=  datetime.today(), freq = 'W-THU')

    # grab names of all bestseller lists
    all_lists = grab_list_names(API_KEY)

    best_sellers = grab_books('2024-10-24', 'hardcover-fiction', API_KEY)

    # # initialize best sellers dataframe
    # best_sellers = pd.DataFrame({"title": [], "rank": [], "prev rank": [], "num weeks": [],
    #       "author": [], "publisher": [], "description": [], "dagger": [], "amazon url": []})
    
    # create connection to MySQL database
    mydb = mysql.connector.connect(
        host = os.getenv('host'),
        user = 'admin',
        password = os.getenv('password'),
        database ='nytBestSellers'
    )

    # for day in dates[::-1]:
    #     print(day.strftime('%Y-%m-%d'))
    #     books = grab_books(day.strftime('%Y-%m-%d'),'hardcover-fiction', API_KEY)
    #     best_sellers._append(books)

    print(best_sellers)
   
if __name__ == "__main__":
    execute()

