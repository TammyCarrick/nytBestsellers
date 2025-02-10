import pandas as pd
from datetime import datetime, timedelta
# import mysql.connector
import time
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os
from get_list_info import grab_books, grab_list_details

from main import db_connect

load_dotenv()
API_KEYS = (os.getenv('api_key1'), os.getenv('api_key2'))

def store_lists_info():
    engine = db_connect()

    # using api key to access nyt data
    list_details = grab_list_details(API_KEYS[0])

    # storing list_details in a table called lists_info
    list_details.to_sql('lists_info', con=engine, if_exists='append', index=False)

def oldest_date(list_name: str):
    """Return all the unique dates in the raw data table
    
    Arg:
        list_name: a string containing the name of the list you want to check eg: 'hardcover-fiction'
    """

    engine = db_connect()
    cnx = engine.connect()

    query = "SELECT DISTINCT date_on_list FROM raw_data WHERE type_ = '{}' ORDER BY date_on_list LIMIT 1".format(list_name)
    result = pd.read_sql(query, con = cnx)

    print(result.empty)
    #print((result['date_on_list'])[0])

    # return result['date_on_list'][0]

def check_if_new(given_date: str, list_name: str)-> bool:
    """Return true if the combination of date and book list type will result in 
    new entries into the raw_data table.

    Arg:
        given_date: a string containing a date in YYYY-MM-DD format
        list_name: a string containing the name of the list you want to check eg: 'hardcover-fiction'
    
    """

    engine = db_connect()
    cnx = engine.connect()
    
    given_date = datetime.strptime(given_date, '%Y-%m-%d').date()

    # determining the day of the week and the difference between date and most recent Thursday
    day_of_week = given_date.weekday()
    
    if day_of_week >= 3:
        diff = day_of_week - 3
    else:
        diff = day_of_week + 4

    closest_thurs = given_date - timedelta(days = diff)
    #print(closest_thurs)

    query = "SELECT DISTINCT date_on_list FROM raw_data WHERE type_ = '{}' AND date_on_list = '{}'".format(list_name, closest_thurs)

    result = pd.read_sql(query, cnx)

    return result['date_on_list'].empty

def date_range(list_name: str, end_date = datetime.today()):
    """Return a list of dates given a list name and an end_date. List of dates is based on the 
      oldest and newest published date of the list name

    Arg:
        list_name: a string containing the name of the list you want to check eg: 'hardcover-fiction'

        end_date: a string containing the end of the date range to be generated. set to today's date.
      
      """
    
    engine = db_connect()
    cnx = engine.connect()

    query = "SELECT oldest_published_date FROM lists_info WHERE type_ = '{}'".format(list_name)
    start_date = pd.read_sql(query, con = cnx)

    start_date = start_date['oldest_published_date'][0]
    dates = pd.date_range(start = start_date, end = end_date, freq = 'W-THU')

    return dates

def execute(list_name: str):

    # connect to database
    engine = db_connect()
    cnx = engine.connect()

    # generate a list of dates between a specified range
    start_date = oldest_date(list_name)
    dates = date_range(list_name, start_date)
    
    # grab names of all bestseller lists
    query = "SELECT type_ FROM lists_info ORDER BY priority"
    type_ = pd.read_sql(query, con = cnx)
    list_ = type_["type_"].tolist()

    # print(list)

    # best_sellers = grab_books('2024-10-24', 'hardcover-fiction', API_KEYS[0])

    # # initialize best sellers dataframe, date series, and count
    best_sellers = pd.DataFrame({"title": [], "rank_": [], "prev_rank": [], "num_weeks": [],
           "author": [], "publisher": [], "description_": [], "dagger": [], "amazon_url": []})

    count = 0
    dates_ = []
    type_ = []

    while count <50: 
        day1 = dates[-1 - 2*count]
        day1 = (day1.strftime('%Y-%m-%d'))

        day2 = dates[-2 - 2*count]
        day2 = (day2.strftime('%Y-%m-%d'))

        if check_if_new(day1, list_[0]):
            # grabbing the list details day1 using apikey 1
            books, num_books = grab_books(day1, list_[0], API_KEYS[0])
            best_sellers = best_sellers._append(books)

            # populating date column
            dates_.extend([day1 for i in range(num_books)])
            type_.extend(list_[0] for i in range(num_books))

        if check_if_new(day2, list_[0]):
            # grabbing the list details day2 using apikey 2
            books, num_books = grab_books(day2, list_[0], API_KEYS[1])
            best_sellers = best_sellers._append(books)

            # populating date column
            dates_.extend([day2 for i in range(num_books)])
            type_.extend(list_[0] for i in range(num_books))

        time.sleep(12)

        count += 1
        print("num days:", count)

    # appending dates column to df and appending df to db
    best_sellers['date_on_list'] = dates_
    best_sellers['type_'] = type_

    print(best_sellers['date_on_list'].unique())
    val = input("Please confirm upload to sql database (y/n): ")
    if val == 'y':
        best_sellers.to_sql('raw_data', con=engine, if_exists='append', index=False)

    print("done")
   
if __name__ == "__main__":
    #date_range("hardcover-fiction")
    #check_if_new("2024-12-01", 'combined-print-and-e-book-fiction')
    oldest_date('combined-print-and-e-book-nonfiction')
    # execute("combined-print-and-e-book-nonfiction")
