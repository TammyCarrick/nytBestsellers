import pandas as pd
from datetime import datetime
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

    best_sellers = grab_books('2024-01-01', 'hardcover-fiction', API_KEY)

    connection = create_connection

    sql.write_frame


   
if __name__ == "__main__":
    execute()

