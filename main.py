import requests
import pandas as pd
import json
from datetime import datetime

API_KEY = "hMLYbAaYHCcTUusSPdLwngxxiU3GLIgI"



def execute():

    # info to call get
    requestUrl = "https://api.nytimes.com/svc/books/v3/lists.json"
    requestHeaders = {
    "Accept": "application/json"
    }

    # generate a list of dates between a specified range
    dates = pd.date_range(start='01/01/2000',end=  datetime.today(), freq = 'W-THU')

    all_lists = requests.get(url=requestUrl, headers = requestHeaders, params = {'name': 'name'})


    parameters = {'date': '2024-01-01', 'list':'hardcover-fiction', 'api-key': API_KEY}

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


if __name__ == "__main__":
    execute()

