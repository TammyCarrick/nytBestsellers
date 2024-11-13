import requests
import pandas as pd
import json
from datetime import datetime

API_KEY = "hMLYbAaYHCcTUusSPdLwngxxiU3GLIgI"

requestHeaders = {
    "Accept": "application/json"
}

def grab_books (date: str, list_name: str): 
    """Return the list of books on the NYT Bestsellers list specified by the list name and date
    
    Args:
        date (str): Date of the list to pull data from. Format yyyy-mm-dd
        list_name (str): Name of the NYT Bestseller list to pull data from.  
    """

    requestUrl = "https://api.nytimes.com/svc/books/v3/lists.json"
    parameters = {'date': date, 'list': list_name, 'api-key': API_KEY}

    # tells the API that the format it's expecting to recieve is a json file. If the server supports this
    # it'll return a json, if not it may return an error or a different content type

    response = requests.get(url=requestUrl, headers=requestHeaders, params= parameters)
    # saves files to a json
    # with open("data.json", 'w') as file:
    #     json.dump(response.json(), file)

    num_books = response.json()["num_results"]
    books = response.json()["results"]

    titles = []
    desc = []
    author = []
    publisher = []
    published_date = []
    bestsellers_date = []
    curr_rank = []
    prev_rank = []
    num_weeks = []
    dagger = []
    amazon_url = []

    # iterate through each element in the books list and grab its details
    for i in range(num_books):

        rank_details = books[i]
        published_date.append(rank_details["published_date"])
        bestsellers_date.append(rank_details["bestsellers_date"])
        curr_rank.append(rank_details["rank"])
        prev_rank.append(rank_details["rank_last_week"])
        num_weeks.append(rank_details["weeks_on_list"])
        dagger.append(rank_details["dagger"])
        amazon_url.append(rank_details["amazon_product_url"])

        book_details = books[i]["book_details"][0]
        titles.append(book_details["title"])
        desc.append(book_details["description"])
        author.append(book_details["author"])
        publisher.append(book_details["publisher"])

        # print(books[i]["book_details"][0]["title"])
        #print(response.json()["results"][i]["book_details"])

    # create dataframe from data

    d = {"title": titles, "rank": curr_rank, "prev rank": prev_rank, "num weeks": num_weeks, "author": author, "publisher": publisher, "description": desc, "dagger": dagger, "amazon url": amazon_url}

    best_sellers = pd.DataFrame(data=d)

    pd.set_option('display.max_columns', 5)
    print(best_sellers.head(n=5))

def grab_list_names():
    requestURL = "https://api.nytimes.com/svc/books/v3/lists/names.json"
    all_list_details = requests.get(url=requestURL, headers = requestHeaders, params = {'api-key': API_KEY})

    all_list_details = all_list_details.json()
    num_lists = all_list_details["num_results"]

    names_of_lists = []

    # iterate through dict and get book names only for lists last updated in 2024
    for i in range(num_lists):
        list_details = all_list_details["results"][i]

        year = list_details["newest_published_date"][:4]

        # only want book lists last updated in 2024 
        if year == "2024":
            names_of_lists.append(list_details["list_name_encoded"])
    print(names_of_lists)

   