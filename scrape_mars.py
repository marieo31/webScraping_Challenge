
# coding: utf-8
# Imports
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time


def init_browser():
    """
    Initialize the browser
    """
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_news():
    """
    # ## 1/ Scraping NASA Mars news
    Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    Assign the text to variables that you can reference later. -> news_title / news_p
    # Example:
    news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
    news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
    """
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'lxml')

    # Grabbing the slides of the NASA mars news page
    # results = soup.find_all('div', class_='slide')
    # we only want the first slide
    result = soup.find('div', class_='slide')
    news_title = result.find('div', class_="content_title").text.strip()
    news_p = result.find('div', class_="rollover_description_inner").text.strip()

    return news_title, news_p

def scrape_jpl_images():      
    """
    # ## 2/ JPL Mars Space Images
    Visit the url for JPL Featured Space Image.
    Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    Make sure to find the image url to the full size .jpg image.
    Make sure to save a complete url string for this image
    """
    browser = init_browser()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=featured&category=Mars#submit"
    browser.visit(url)
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    url_base = "https://www.jpl.nasa.gov"
    result = soup.find('a', class_='fancybox')
    featured_image_url = url_base+result["data-fancybox-href"]

    # Close the browser after scraping
    browser.quit()
    return featured_image_url

def scrape_weather():      
    """
    # ## 3/ Mars Weather
    Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the 
    planet including Diameter, Mass, etc.
    Use Pandas to convert the data to a HTML table string
    # Example:
    mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    """

    url = "https://twitter.com/marswxreport?lang=en"
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'lxml')

    result = soup.find('div', class_='js-tweet-text-container')
    mars_weather = result.find('p').text.strip()

    return mars_weather


def scrape_mars_facts():
    """
    # ## 4/ Mars Fact
    Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    Use Pandas to convert the data to a HTML table string.
    """
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)

    mars_fun_facts = tables[0]
    # Adding column names
    mars_fun_facts.columns = ['Description', 'Value']
    # Remove the ":" at the end of the descriptions of the values
    mars_fun_facts['Description'] = mars_fun_facts['Description'].str[:-1]

    return mars_fun_facts.to_html()

def scrape_hemispheres():
    """
    # ## 5/ Mars Hemispheres
    Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    You will need to click each of the links to the hemispheres in order to find the image url to the full 
    resolution image.
    Save both the image url string for the full resolution hemisphere image, and the Hemisphere
    title containing the hemisphere name. 
    Use a Python dictionary to store the data using the keys img_url and title.
    Append the dictionary with the image url string and the hemisphere title to a list. 
    This list will contain one dictionary for each hemisphere
    """
    url_base = "https://astrogeology.usgs.gov"
    url = url_base+"/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = init_browser()

    browser.visit(url)
    time.sleep(3)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # we look for the div describing the images
    results = soup.find_all('div', class_='description')
#     hemisphere_image_urls = []
    hemi_dico = {}
    ii = 1
    for rr in results:
        # grab the tile of the picture
        title = rr.find('h3').text    
        # url to visit to get the full size imge
        url_for_pict = url_base + rr.find('a')['href']
        # go to the page where we can find the full size pict
        browser.visit(url_for_pict)
        # sleep a little bit
        time.sleep(3)
        # Scrape into soup
        html_pic = browser.html
        soup_pic = bs(html_pic, 'html.parser')
        # look for the link
        res_pic = soup_pic.find('img',  class_="wide-image")
        url_img = url_base+res_pic['src']
#         # Append a dict with the scraped variable in the list
#         hemisphere_image_urls.append({"title":title,
#                                     "img_url": url_img})
        # I found easier to manage in the html to have a dictionnary
        hemi_dico['title'+str(ii)] = title
        hemi_dico['img_url'+str(ii)] = url_img
        ii += 1        
#         break    
        
    browser.quit()
#     print(hemisphere_image_urls)
    


    return hemi_dico


def scrape_mars():
    """
    Scrape everything and return a dictionnary with all the data
    """
    (news_title, news_p) = scrape_news()


    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
#         "jpl_url": scrape_jpl_images(),
#         "facts_tbl": scrape_mars_facts(),
#         "weather": scrape_weather(),
        "hemi_pct": scrape_hemispheres(),
    }


    return mars_data
        

