# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 15:33:03 2021

@author: Joey
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import html_header
import url_specific_site


# Get the Header required to get past the security of the Website
header = html_header.get_html_header()
# Get base URL of specific statistics Website that is scraped
base_url = url_specific_site.get_url()

# Postal codes we want to scrap from website
postal_codes = ['V5C', 'V5H', 'V5K', 'V5L', 'V5M', 'V5N', 'V5P', 'V5R', 'V5S',
                'V5T', 'V5V', 'V5W', 'V5X', 'V5Y', 'V5Z', 'V6A', 'V6B', 'V6C',
                'V6H', 'V6J', 'V6K', 'V6L', 'V6M', 'V6N', 'V6E', 'V6G', 'V6P', 
                'V6R', 'V6S', 'V6T', 'V6V', 'V6X', 'V6Z', 'V7B', 'V7J', 'V7P', 
                'V7R', 'V7S', 'V7T', 'V7V', 'V7X', 'V7Y', 'V8B']

# Name of the categories we want to scrap
attributes = ["Area of Postal Code", "Population", "Male Population",
           "Female Population", "Median Age", "Male Median Age",
           "Female Median Age"]

# Lower and add underscore to fit better into other columns style
columns = [x.lower().replace(" ", "_") for x in attributes]
columns.append("postal_code")


# Create a new empty DataFrame
df = pd.DataFrame(columns=columns)

# Better performance of the get request
session = requests.Session()

# Iterate over all postal codes
for index, code in enumerate(postal_codes):
    
    # Combine HTML with prefix 
    page = requests.get(base_url + code, headers=header)
    # Parse with BeautifulSoup
    soup = BeautifulSoup(page.text, 'html.parser')
    # "tr" tags contain the data we want
    values = soup.find_all("tr")
    # Only the first 17 "tr" tags are useful for us
    for attr in range(17):
        # "tr" tags contain two "td" tags (tag[0] = Category, tag[1] = Value) 
        tags = values[attr].find_all("td")
        category = tags[0].text
        # One of the categories name is dynamic with the postal code we want
        # to generalize
        if category == (attributes[0] + " " + code):
            category = category[:-4]
        if category in attributes:
            column = category.lower().replace(" ", "_")
            df.loc[index, column] = tags[1].text
    # Add Postal Code to DataFrame
    df.loc[index, "postal_code"] = code
    # Sleep so website doesnt block our requests
    time.sleep(10)


# Save as CSV File
df.to_csv("population_data_vancouver.csv")