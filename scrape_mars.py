#################################################
# Conversion of Jupyter Notebook to Python script
#################################################

# Dependencies
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
import splinter
import requests
from splinter import Browser
from selenium import webdriver
import time

def init_browser():
# Set Executable Path & Initialize Chrome Browser
    executable_path = {'executable_path': '/Users/17324/Downloads/chromedriver'}
    _browser = Browser('chrome', **executable_path, headless=False)

_browser = init_browser()
mars = {}

###################################################
# NASA Mars News
###################################################
def mars_news(browser):
    
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Get first list item and wait half a second if not immediately present
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    html = browser.html
    news_soup = bs(html, "html.parser")

    # Retrieve page with the requests module
    response = requests.get(url)
    response
    response.url
    response.status_code

    # news_soup
    print(news_soup.prettify())

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph text. Assign the text to variables that can
    #be referenced later.
    
    try:
       slide_elem = news_soup.select_one("ul.item_list li.slide")
       latest_title = slide_elem.find("div", class_="content_title").get_text()
       latest_text = slide_elem.find(
           "div", class_="article_teaser_body").get_text()

    #return latest_title, latest_text
    except AttributeError:
        return None, None
    return latest_title, latest_text
           
###################################################
# JPL Mars Space Images - Featured Image
###################################################
def featured_image(browser):
    #Access/visit the url
    
    # Visit the JPL Mars Space site and find the image url for the current Featured Mars Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

        # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    time.sleep(2)

    # Find the more info button and click that
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    time.sleep(2)

    # Parse the resulting html with soup
    html = browser.html
    image_soup = bs(html, 'html.parser')

    # find the relative image url
    img_url_rel = image_soup.find('figure', class_='lede').find('img')['src']

    # Set featured_image
    current_image_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return current_image_url
    
###################################################
# Mars Weather
###################################################
def weather_twitter(browser):
    # Visit the Mars Weather twitter account.
    #Access/visit the url
   
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    weather_soup = bs(html, "html.parser")

    # Scrape the latest Mars weather tweet from the page.
    try:
        mars_weather = weather_soup.find('div', attrs={"class":"js-tweet-text-container"})
        
        mars_weather.find('p').text

    # Save the tweet text for the weather report as a variable called mars_weather.
        mars_weather_text = mars_weather.find('p').text
           
    except AttributeError:
        return None, None
    return mars_weather_text

###################################################
# Mars Facts
###################################################

def mars_facts(browser):    

    # Visit the Mars Facts webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    try:
        tables = pd.read_html(url)
        tables
        type(tables)

        df1 = tables[0]
        df1.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
        df1
        df1.drop(["Earth"], axis = 1, inplace = True)
        df1
        df1.rename(columns={'Mars - Earth Comparison':'Fact Category'}, inplace=True)
        df1
        df1.rename(columns={'Mars':'Mars Value'}, inplace=True)
        df1

        df2 = tables[1]
        df2.columns = ['0', '1']
        df2
        df2.rename(columns={'0':'Fact Category'}, inplace=True)
        df2
        df2.rename(columns={'1':'Mars Value'}, inplace=True)
        df2

        df = df1.append(df2, ignore_index=True)
        df

    #Use Pandas to convert the data to a HTML table string.
        data = df
        mars_html_table = data.to_html(classes="table table-striped")

    except AttributeError:
        return None, None
    return mars_html_table
   
###################################################
# Mars Hemispheres
###################################################
def hemisphere(browser):
    #mars = {}
    # Retrieve Mars Hemisphere Data
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
   
    # List for hemisphere image links
    hemisphere_full_image_urls = []

    # First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for item in range(len(links)):
        hemisphere = {}

        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[item].click()

        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_elem["href"]

        # Get Hemisphere title
        hemisphere["title"] = browser.find_by_css("h2.title").text

        # Append hemisphere object to list
        hemisphere_full_image_urls.append(hemisphere)

        # Navigate backwards
        browser.back()
        
    return hemisphere_full_image_urls

###################################################
# Scrape Function
###################################################
def scrape_all():
    executable_path = {'executable_path': '/Users/17324/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    latest_title, latest_text = mars_news(browser)
    current_image_url = featured_image(browser)
    mars_weather_text = weather_twitter(browser)
    mars_html_table = mars_facts(browser)
    hemisphere_full_image_urls = hemisphere(browser)
    
    data = {
        "news_title": latest_title,
        "news_text": latest_text,
        "featured_image": current_image_url,
        "weather": mars_weather_text,
        "facts": mars_html_table,
        "hemispheres": hemisphere_full_image_urls,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())
