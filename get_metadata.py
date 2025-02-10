import pandas as pd
import requests
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from main import db_connect
import json
import numpy as np
import time


load_dotenv()
API_KEY = os.getenv('api_key_google')


def retrieve_volume(vol_id: str, t = False):
    """Return infromation about a specific volume using the Google Books API

    Args
        vol_id(str): contains the volume id of a book to search
        t(boolean): specifies if we're troubleshooting data or not
    """
    data = ""
    # requestURL = "https://www.googleapis.com/books/v1/volumes/{id}?projection=lite&key={api_key}".format(id = vol_id, api_key = API_KEY)
    requestURL = "https://www.googleapis.com/books/v1/volumes/{id}".format(id = vol_id)

    response = requests.get(requestURL).json()
    if "volumeInfo" in response:
        data = response['volumeInfo']
    
    if t:
        print(json.dumps(data, indent = 2))

    return data

def get_verified_ids():
    """Return a list of ids from the verified ids table that haven't been logged in the metadata table
    
    """

    engine = db_connect()
    cnx = engine.connect()

    # all volume ids in the verified table not in the metadata table
    query = "SELECT ver.volumeid\
        FROM verified_ids AS ver\
        LEFT JOIN metadata AS met\
            ON ver.volumeid = met.volumeid\
        WHERE met.volumeid IS NULL\
        ORDER BY ver.volumeid DESC"
    
    vol_ids = pd.read_sql(query, con= cnx)

    # print(vol_ids)

    return vol_ids['volumeid']

def parse_categories(categories):
    """Return a formatted list of categories/genres of a book given its categories in list format
    
    Arg
        categories(list): elements are string type. 
        Example format: 
            categories = [
            "Fiction / Thrillers / Crime",
            "Fiction / Mystery & Detective / Police Procedural",
            "Fiction / Thrillers / Suspense"
            ]
    """

    all_genres = []
    max_len = 7
    i = 0
    l = 0 
    # iterate through each line
    while i < max_len and  l < len(categories):
        parsed = categories[l].split("/")

        j = 0
        # iterate through each genre in a line and add that genre to all_genres if it hasn't been added already
        while i < max_len and j < len(parsed):
            genre = parsed[j].strip()
            j += 1 #book count
            if genre not in all_genres:
                all_genres.append(genre)
                i+=1
        l+=1 # line count

    #populate remaining columns with ''
    while i < max_len:
        all_genres.append('')
        i +=1

    # print(all_genres)
    return all_genres

def handle_img_url(image_links):
    """Given a dictionary of url links, return a string containing a url referencing an image
    
    Arg
        image_links(dict): keys are image size, values are the image urls
    
    """

    if "small" in image_links:
        return image_links['small']
    elif "medium" in image_links:
        return image_links['medium']
    elif "large" in image_links:
        return image_links['large']
    elif "extralarge" in image_links:
        return image_links['extralarge']
    elif "smallThumbnail" in image_links:
        return image_links["smallThumbnail"]
    elif "thumbnail" in image_links:
        return image_links["thumbnail"]
    else:
        ""


def handle_maturity(rating:str):
    """Return 1 if rating is MATURE and 0 if rating is NOT_MATURE

    Arg
        rating(str): string containing the maturity rating of a book
    
    """

    if rating == "MATURE":
        return 1
    elif rating == "NOT_MATURE":
        return 0
    else:
        return


def populate_metadata(nrows = 50):

    """Populate the metadata table with google books info

    Arg
        nrows(int): number of volumeids to iterate through
    
    """
    engine = db_connect()
    
    vol_ids = get_verified_ids()
    num_vol = len(vol_ids)
    i = 0

    searched_ids = []
    author = []
    title = []
    publisher = []
    published_date = []
    desc = []
    pg_count = []
    print_pg_count = []
    all_genres = []
    img_link = []
    maturity_rating = []
    isbn10 = []
    isbn13=[]

    # key_names = ['title', 'publisher', 'publishedDate', 'description', 'pageCount',' printedPageCount']
    
    while i < nrows and i < num_vol:
        data = retrieve_volume(vol_ids[i])
        if data != "": # check the searched vol_id returned something
            # data = retrieve_volume('_HxlCgAAQBAJ')                
            print(vol_ids[i], data['title'])
            print("num books: ", i)
            searched_ids.append(vol_ids[i])

            if 'authors' in data:
                author.append(data['authors'][0])
            else:
                author.append(None)

            if 'title' in data:
                title.append(data['title'])
            else:
                title.append(None)

            if 'publisher' in data:
                publisher.append(data['publisher'])
            else:
                publisher.append(None)

            if 'publishedDate' in data:
                published_date.append(data['publishedDate'])
            else:
                published_date.append(None)

            if 'description' in data:
                desc.append(data['description'][:2999])
            else:
                desc.append(None)

            if 'pageCount' in data:
                pg_count.append(data['pageCount'])
            else:
                pg_count.append(None)

            if 'printedPageCount' in data:
                print_pg_count.append(data['printedPageCount'])
            else:
                print_pg_count.append(None)

            if 'imageLinks' in data:
                img_link.append(handle_img_url(data['imageLinks']))
            else:
                img_link.append(None)

            if 'maturityRating' in data:
                maturity_rating.append(handle_maturity(data['maturityRating']))
            else:
                maturity_rating.append(None)

            if 'industryIdentifiers' in data:
                isbn10.append(data['industryIdentifiers'][0]['identifier'])
            else:
                isbn10.append(None)

            if 'industryIdentifiers' in data and len(data['industryIdentifiers']) > 1:
                isbn13.append(data['industryIdentifiers'][1]['identifier'])
            else:
                isbn13.append(None)
        
            # get the genres
            if 'categories' in data:
                all_genres.append(parse_categories(data['categories']))
            else:
                all_genres.append(['','','','','','',''])
            

            # every 20 entries break for 10 sec
            if i % 20 == 0 and i != 0:
                time.sleep(10)

        i +=1
    
    # transposing all_genres list so I can index it in the correct way (eg the first row corresponds to the first
    # genre for all books instead of all the genres for one book)

    all_genres_t = np.array(all_genres).T

    data = {'volumeid': searched_ids, 'author': author, 'title': title, 'publisher': publisher, 'published_date': published_date,
            'description_': desc, 'pg_count' : pg_count, 'printed_pg_count' : print_pg_count, 'img_url' : img_link,
            'maturity_rating': maturity_rating, 'ISBN10': isbn10, 'ISBN13': isbn13, 'genre1': all_genres_t[0],
            'genre2': all_genres_t[1], 'genre3': all_genres_t[2], 'genre3': all_genres_t[2], 'genre4': all_genres_t[3],
            'genre5': all_genres_t[4], 'genre6': all_genres_t[5], 'genre7': all_genres_t[6]}
    
    df = pd.DataFrame(data)

    print(df)

    val = 'z'

    while val != 'y' and val != 'n':
        val = input('Please confirm upload to table (y/n):')
    
    if val == 'y':
        df.to_sql('metadata', con=engine, if_exists = 'append', index = False)


if __name__ == "__main__":
    retrieve_volume('_C5jxQEACAAJ', True )
    # get_verified_ids()
    # parse_categories([
    #   "Fiction / Thrillers / Crime",
    #   "Fiction / Mystery & Detective / Police Procedural",
    #   "Fiction / Thrillers / Suspense"])
    # handle_maturity('d')
    # populate_metadata(200)
    # parse_categories( ["Fiction / Family Life / General", "Fiction / Animals"])
# 