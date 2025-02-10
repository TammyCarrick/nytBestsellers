import requests
import pandas as pd
from datetime import datetime

requestHeaders = {
    "Accept": "application/json"
}

def grab_books (date: str, list_name: str, api_key: str): 
    """Return the a dataframe of books on the NYT Bestsellers list specified by the list name and date
    
    Args:
        date (str): Date of the list to pull data from. Format yyyy-mm-dd
        list_name (str): Name of the NYT Bestseller list to pull data from
        api_key (str): API key for NYT Bestsellers
    """
    requestUrl = "https://api.nytimes.com/svc/books/v3/lists.json"
    parameters = {'date': date, 'list': list_name, 'api-key': api_key}

    # tells the API that the format it's expecting to recieve is a json file. If the server supports this
    # it'll return a json, if not it may return an error or a different content type

    response = requests.get(url=requestUrl, headers=requestHeaders, params= parameters)
    # saves files to a json
    # with open("data.json", 'w') as file:
    #     json.dump(response.json(), file)

    #num_books = response.json()["num_results"]
    books = response.json()["results"]
    num_books = len(books)

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

    d = {"title": titles, "rank_": curr_rank, "prev_rank": prev_rank, "num_weeks": num_weeks,
          "author": author, "publisher": publisher, "description_": desc, "dagger": dagger, "amazon_url": amazon_url}

    best_sellers = pd.DataFrame(data=d)

    return best_sellers, num_books

    # pd.set_option('display.max_columns', 5)
    # print(best_sellers.head(n=5))

def grab_list_details(api_key: str):
    """Return a name of all the categories of the NYT Bestsellers 

    Arg:
        api_key (str): API key to acces NYT Bestsellers
    """
    requestURL = "https://api.nytimes.com/svc/books/v3/lists/names.json"
    all_list_details = requests.get(url=requestURL, headers = requestHeaders, params = {'api-key': api_key})

    all_list_details = all_list_details.json()
    num_lists = all_list_details["num_results"]

    type_ = []
    oldest_published_date = []
    newest_published_date = []
    updated = []

    # iterate through dict and get book names only for lists last updated in 2024
    for i in range(num_lists):
        list_details = all_list_details["results"][i]

        year = list_details["newest_published_date"][:4]

        # only want the details of book lists last updated in 2024 
        if year == "2024":
            type_.append(list_details["list_name_encoded"])
            oldest_published_date.append(list_details["oldest_published_date"])
            newest_published_date.append(list_details["newest_published_date"])
            updated.append(list_details["updated"])
    # print(names_of_lists)

    # convert data to a dataframe and return
    list_details = {"type_": type_, "oldest_published_date":  oldest_published_date,
                    "newest_published_date": newest_published_date, "updated": updated}
    
    return pd.DataFrame(data = list_details)
   
