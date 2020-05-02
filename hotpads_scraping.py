"""
@fileName: hotpads_scraping.py
@Author: 
Sai Manogna Pentyala - spentyal@andrew.cmu.edu
"""


# Python program to scrape
# hotpads site to fetch the top 5 houses
# This file imports beautiful soup module,
# numpy, pandas, request and urlopen.
# This file is imported and used by group_7_nestaway_project

  
# importing required modules 
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen
import numpy as np


# method that takes area, budgetRange (min and max), beds as input parameters
# based on these parameters, a list of houses sorted on rent is found and sent
def scrape_hotpads_for_houselist(area, minBudgetRange, maxBudgetRange, beds):

    # replaces the spaces with a hyphen sign
    area = area.replace(" ","-");
    
    # setup url to scrape the hotpads site
    url = 'https://hotpads.com/' + area + '-pittsburgh-pa/houses-for-rent?beds=' + str(beds) + '&price=' + str(minBudgetRange) + '-' + str(maxBudgetRange) + '&propertyTypes=house'
    
    # determine the response, and fetch the html content
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})    
    webpage = urlopen(req).read()
    bsyc = BeautifulSoup(webpage, "html.parser")
    
    # create a dataframe as mentioned below
    houselist_df = pd.DataFrame(columns=['HOUSE ADDRESS', 'BEDS', 'RENT($)', 'LINK TO VIEW THE HOUSE LISTING'])

    # extract information from the html content
    for element in bsyc.find_all('div', id= 'app-root'):
        elements = element.find_all('div', id= 'app-container')
        if(elements):
            for element_1 in elements:
                elements_1 = element_1.find_all('div', class_='SplitMapTemplate SplitMapTemplate-headerNav-mobile-padding')
                if(elements_1):
                    for element_2 in elements_1:
                        elements_2 = element_2.find_all('div', class_='SplitMapTemplate-right-sidebar')
                        if(elements_2):
                                for element_3 in elements_2:
                                    elements_3 = element_3.find_all('div', class_='AreaPage')
                                    if(elements_3):
                                        for element_4 in elements_3:
                                            elements_4 = element_4.find_all('div', class_='AreaListingsContainer')
                                            if(elements_4):
                                                for element_5 in elements_4:
                                                    elements_5 = element_5.find_all('div', class_='AreaListingsContainer-listings')
                                                    if(elements_5):
                                                        for element_6 in elements_5:
                                                            elements_6 = element_6.find_all('div', class_='ListingWrapper')
                                                            if(elements_6):
                                                                for element_7 in elements_6:
                                                                    elements_7 = element_7.find_all('div', class_='ListingCard')
                                                                    if(elements_7):
                                                                        for element_8 in elements_7:
                                                                            elements_8 = element_8.find_all('div', class_='ListingCard-container')
                                                                            if(elements_8):
                                                                                for element_9 in elements_8:
                                                                                    elements_9 = element_9.find_all('div', class_='ListingCard-content-container')
                                                                                    if(elements_9):
                                                                                        for element_10 in elements_9:
                                                                                            # tempList to store each row in the dataframe
                                                                                            templist=[]
                                                                                            # captures the rent amount
                                                                                            rent = element_10.find('div', class_='Utils-bold Utils-inline-block')
                                                                                            rent = str(rent)
                                                                                            fromIndex = rent.index("\">")
                                                                                            toIndex = rent.index("</div>")
                                                                                            rentAmt = rent[fromIndex+3:toIndex:]                                                                                            
                                                                                            # captures the link to view the house
                                                                                            link = element_10.find('a').get("href")
                                                                                            link = str(link)
                                                                                            # captures the address of the house
                                                                                            address = element_10.find('a').find("h3").text
                                                                                            templist.append(address)
                                                                                            templist.append(beds)
                                                                                            templist.append(rentAmt)
                                                                                            templist.append("https://hotpads.com"+link)                                                                                            
                                                                                            addRow = pd.DataFrame(templist, index=houselist_df.columns).T
                                                                                            houselist_df = houselist_df.append(addRow, ignore_index=True)                    
# return the list of houses sorted on the rent column
    houselist_df = houselist_df.sort_values(["RENT($)"], ascending = (True))                                                                                            
    houselist_df.index = np.arange(1, len(houselist_df)+1)    
    return houselist_df
