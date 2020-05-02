"""
@fileName: grocery_restaurant_scraping.py
@Author:
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""

# It performs scraping of a website - yellow pages
# to determine the restaurants and grocery stores
# It imports beautifulSoup, requests, pandas, and numpy
# It is imported by project_7_nestaway_project

# imports for webscraping and dataframes
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def scrape_groceries_restaurants(type, area, distance=1):

    """
    This method get The various groceries
    and restaurants in that are from yellowpage.
    """

    # setup url
    base_url = 'https://www.yellowpages.com/search?search_terms='

    # check whether the input type is grocery or restaurants.
    # and build the url to scrape information.
    if type == 'grocery':
        base_url += 'grocery+stores&geo_location_terms='

    if type == 'restaurant':
        base_url += 'restaurants&geo_location_terms='

    base_url += (area + '%2C%20Pittsburgh%2C%20PA&s=distance')

    # scrape information
    res = requests.get(base_url)
    bsyc = BeautifulSoup(res.content, "html.parser")

    list_df = pd.DataFrame(columns=['NAME', 'DISTANCE(miles)', 'LINK TO MORE INFORMATION ON GROCERY STORE'])

    # extract information
    for element in bsyc.find_all('div', {'class': 'info'}):
        distance_element = element.find('div', {'class': 'distance'})
        if distance_element is not None:

            # if scraped distance is smaller than the distance that we defined
            if float(distance_element.text.split(" ")[0]) <= distance:
                templist = []
                name = element.find('span').text
                mile = distance_element.text.split(" ")[0]
                link = 'https://www.yellowpages.com' + element.find('a').get("href")
                templist.append(name)
                templist.append(mile)
                templist.append(link)
                addRow = pd.DataFrame(templist, index=list_df.columns).T
                list_df = list_df.append(addRow, ignore_index=True)


    list_df.index = np.arange(1, len(list_df)+1)

    # return the number of restaurants or groceries
    return list_df
