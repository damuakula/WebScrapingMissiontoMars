from splinter import Browser
from bs4 import BeautifulSoup
import requests
import cssutils
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    nasa_listings = []
    
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'

    browser.visit(url)
    html = browser.html
    # Create BeautifulSoup object; parse html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.title.text.strip()
    news_p = soup.body.p.text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')   
    background_image = soup.find('article', class_='carousel_item')['style']

    style = cssutils.parseStyle(background_image)
    url = style['background-image']

    image_url = url.replace('url(', '').replace(')', '')
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    # URL of page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    browser.visit(twitter_url)
    html = browser.html
    # Create BeautifulSoup object; parse html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.title.text.strip()
    mars_weather = soup.find_all('p')[4].text

    #Visit the Mars Facts webpage https://space-facts.com/mars/ and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html('https://space-facts.com/mars/')

    nasa_listings = [
        {"title": "Cerberus Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere Enhanced", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title": "Valles Marineris Hemisphere", "img_url": "http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"news_title": news_title},
        {"news_p": news_p},
        {"mars_weather": mars_weather},
        {"feature_img_url": featured_image_url}
    ]

    return nasa_listings, tables
