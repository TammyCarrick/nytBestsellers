import requests
import pandas as pd
import json
from datetime import datetime
from grab_data import grab_books, grab_list_names


def execute():

    # generate a list of dates between a specified range
    dates = pd.date_range(start='01/01/2000',end=  datetime.today(), freq = 'W-THU')

    # grab names of all bestseller lists
    grab_list_names()
    
    grab_books('2024-01-01', 'hardcover-fiction')
   
if __name__ == "__main__":
    execute()

