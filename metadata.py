import requests
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
import pandas as pd

load_dotenv()

API_KEY = os.getenv('api_key_google')

# move db_connect to grab_data and import it into main and metadata
def db_connect():
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

def bulk_troubleshoot():
    """Adds all books that haven't been logged in the volume id table to the troubleshoot table after all 
    the books in the raw_data table have been iterated through"""

    engine = db_connect()
    cnx = engine.connect()

    query3 = 'SELECT DISTINCT rd.author, rd.title\
    FROM raw_data AS rd\
        LEFT JOIN volumeid AS v\
            ON rd.author=v.author AND rd.title = v.title\
    WHERE v.author IS NULL \
    ORDER BY rd.author, rd.title ASC;'

    books = pd.read_sql(query3, cnx)

    df = {'author': books['author'],'title': books['title']}
    df = pd.DataFrame(data=df)

    df.to_sql('troubleshoot_id', con=engine, if_exists='append', index= False)

def troubleshoot_log():
    """Adds books that haven't been logged to the troubleshoot_id table."""
    engine = db_connect()
    cnx = engine.connect()

    query = 'SELECT author\
        FROM volumeid\
        ORDER BY author DESC\
        LIMIT 1'
    
    top_author = pd.read_sql(query, cnx)['author'][0] #the top name on the volumeid table
    print(top_author)

    # query the raw_data table for all the books that haven't been added to the volumeid table based on the top_author
    query2 = 'SELECT DISTINCT rd.author, rd.title\
        FROM raw_data AS rd\
            LEFT JOIN volumeid AS v\
                ON rd.author=v.author AND rd.title = v.title\
        WHERE v.author IS NULL AND rd.author<\'{author}\'\
        ORDER BY rd.author, rd.title ASC;'.format(author = top_author)
        
    books = pd.read_sql(query2, cnx)

    df = {'author': books['author'],'title': books['title']}
    df = pd.DataFrame(data=df)

    df.to_sql('troubleshoot_id', con=engine, if_exists='append', index= False)

def volumeid_entries():
    """Returns all the entries in the volume id table"""
    engine = db_connect
    cnx = engine.conntect()

    query = "SELECT "

def unlogged_books():
    """Return a list of books (titles and authors) whose volumeIDs have not been logged yet;
    books in the raw_data table or troubleshoot_id table but not in the volumeID table"""

    engine = db_connect()
    cnx = engine.connect()

    # query = 'WITH in_rd_but_not_vi AS(\
    #     SELECT DISTINCT rd.author, rd.title\
    #     FROM raw_data AS rd\
    #         LEFT JOIN volumeid  AS vi\
    #             ON rd.author = vi.author AND rd.title = vi.title\
    #     WHERE vi.author IS NULL\
    #     )\
    #     SELECT rdvi.author, rdvi.title\
    #     FROM in_rd_but_not_vi AS rdvi\
    #         LEFT JOIN troubleshoot_id AS t\
    #             ON rdvi.author = t.author\
    #     WHERE t.author IS NULL\
    #     ORDER BY rdvi.author, rdvi.title ASC;'
    query = 'SELECT DISTINCT r.author, r.title\
        FROM raw_data AS r\
            LEFT JOIN volumeid AS v\
                ON r.author = v.author AND r.title = v.title\
        WHERE v.author IS NULL AND r.author >\'Ted\'\
        ORDER BY r.author'
    
    books = pd.read_sql (query, con = cnx)
    authors = books['author']
    titles = books['title']

    return authors, titles

def get_volumeID(title: str, author: str):
    """Return the volume ID, title, and author (search result) of a book given its 
    title and author or None if the volume doesn't exist

    Args:
        title (str): name of the book
        author (str): name of the author
    
    """
    requestURL = 'https://www.googleapis.com/books/v1/volumes?q={book_name}+inauthor:{author_name}'.format(book_name = title, 
                                                                                                           author_name = author)
                                                                                                    
    # parameters = {'title': title, 'author': author}

    response = requests.get(url = requestURL).json()
    volumeID, author_rslt, title_rslt = None, None, None # initialize values in case no result is found

    # check the search returned at least one result
    if 'totalItems' in response and response['totalItems']> 0: # key exists and has at least 1 result
    # if response['totalItems']> 0:
        # print(response['items'][0])
        volume_info = response['items'][0]['volumeInfo']

        if 'authors' in volume_info and 'title' in volume_info: # check the volume has an author and title
            volumeID = response['items'][0]['id']
            author_rslt = response['items'][0]['volumeInfo']['authors'][0]
            title_rslt = response['items'][0]['volumeInfo']['title']

    # print('volume ID: {vol}, title: {name}, author: {auth}'.format(vol =volumeID,
    #                                                                 name = title_rslt, auth = author_rslt))

    return volumeID, author_rslt, title_rslt

def parse_name (full_name: str):
    """Return author's name parsed into first, middle and last names given their full_name
    
    Arg
        full_name: string containing authors full name
    
    """
    
    first_name = None
    middle_name = None
    last_name = None

    if full_name is not None:

        full_name = full_name.split(" ")

        if len(full_name) == 1:
            last_name = full_name[0]

        elif len(full_name) == 2:
            first_name = full_name[0]
            last_name = full_name[-1]

        elif len(full_name) >= 3:
            first_name =full_name[0]
            middle_name = full_name[1:-1]
            last_name = full_name[-1]

    return first_name, middle_name, last_name

def handle_middle_names(name: list):
    """Return string version of middle name given it as a list form
    
    Args
        name (list): either empty, or has an element or more of strings types
    """

    if name is None:
        return None
    else:
        middle_name = ' '.join(name)

    return middle_name

def populate_ids():
    """Iterate through list of unlogged books, grab the volumeID of each, log them into the volumeid table """

    engine = db_connect()
    authors, titles = unlogged_books()
    num_entries = len(authors)

    i = 0

    volume_ids = []
    title_rslt = []
    # list of authors and titles that had successful search results and returned a valid volumeID
    titles_searched = []
    authors_searched = []
    all_f_names = []
    all_m_names = []
    all_l_names = []

    while i <250 and i <num_entries:
        print(titles[i], authors[i])
        v,a,t = get_volumeID(titles[i], authors[i])
        # verify author last names match and append if so add to list
    
        first_name, middle_name, last_name = parse_name(a)
        middle_name = handle_middle_names(middle_name)

        if last_name != None:
            # check the last names match
            if last_name.lower() == authors[i].split(" ")[-1].lower():
                volume_ids.append(v)
                title_rslt.append(t)
                titles_searched.append(titles[i])
                authors_searched.append(authors[i])
                all_f_names.append(first_name)
                all_m_names.append(middle_name)
                all_l_names.append(last_name)
                print('num books:', i)

        i += 1

    df = {'volumeid': volume_ids, 'author': authors_searched,'title': titles_searched,'title_rslt': title_rslt,
           'first_name': all_f_names, 'middle_name': all_m_names, 'last_name': all_l_names}
    
    df = pd.DataFrame(data=df)
    print(df[['title', 'title_rslt', 'author', 'last_name']])

    val = 'z'

    while val != 'y' and val != 'n':
        val = input('Please confirm upload to table (y/n):')
    
    if val == 'y':
        df.to_sql('volumeid', con=engine, if_exists = 'append', index = False)

if __name__== '__main__':
#    get_volumeID('THE HOUSE OF SECRETS', 'Brad Meltzer and Tod Goldberg' )
#    unlogged_books()
    populate_ids()
    # f,m,l = parse_name('Tatiana de Rosnay')
    # print(f, " ",m, " ", l)
    # troubleshoot_log()
