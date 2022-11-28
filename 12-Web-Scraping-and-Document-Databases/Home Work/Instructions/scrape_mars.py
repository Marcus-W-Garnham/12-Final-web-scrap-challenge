from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time
import selenium
from selenium import webdriver
import numpy as np
from flask import Flask 
from flask_pymongo import PyMongo
import requests as rqst


def scrape_info():

    # scrape the featured image

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    URL = "https://spaceimages-mars.com"
    browser.visit(URL)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information

    featured_image = soup.find_all('img', class_='headerimage')
    featured_image_url2 = URL + '/' + featured_image[0]['src']


    # now its time to scrape the mars comparison data

    URL2 = "https://galaxyfacts-mars.com"
    browser.visit(URL2)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information

    facts_mars = soup.find_all('tr', class_='table table-striped')

    facts_mars2 = rqst.get(URL2)
    soup_mars = bs(facts_mars2.content, "html.parser")

    tablehead = soup_mars.tbody

    Mars_Headers = []
    for x in tablehead.find_all('tr'):
        for y in x.find_all('th'):
            Mars_Headers.append(y.text)
    Mars_Headers

    numbers = tablehead.find_all("td")

    rows = tablehead.find_all('tr', class_="data-row")

    dfm = pd.read_html(URL2)

    earth_mars = dfm[0]

    earth_mars.columns = earth_mars.iloc[0]
    earth_mars = earth_mars[1:]

    earth_mars2 = earth_mars.to_html(classes= 'table table-striped').strip('"')
    #earth_mars2 = earth_mars.to_json(orient="table")
    print(type(earth_mars2))

    # end of facts mars and earth


    mars_data = {
    "Featured_img": featured_image_url2,
    "Earth_Mars_facts": earth_mars2,
    }

    browser.quit()

    return mars_data
#print(scrape_info())
