# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd
import datetime as dt

def scrape_all():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
         "news_title": news_title,
         "news_paragraph": news_paragraph,
         "featured_image": featured_image(browser),
         "facts": mars_facts(),
         "last_modified": dt.datetime.now(),
         "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data    

def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # convert browser html to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None, None

    return news_title, news_p

# # ### Feat. Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try: 
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

# ### Scrape planet data and store in pandas df

def mars_facts():

    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    return df.to_html(classes="table table-dark")

### Scrape hemisphere data

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # counts how many hemisphere options available, could hard code to 4 since there are only 4 hemispheres, but keeping code flexible.
    html = browser.html
    item_count_soup = soup(html, 'html.parser')
    item_count = item_count_soup.find_all('div', class_='item')
    len(item_count)

    for x in range(len(item_count)):
        
        #select the item element
        product_element = item_count_soup.select('div.item')[x]
        #get the title
        product_title = product_element.find('h3').get_text()
        
        #print(product_title) #for debugging
        
        # get the image link
        # couldn't get click to work, but the goal was only to get the link so lets get the new link from href and tell browser to go there...
        img_url_rel= product_element.find('a',class_='itemLink product-item').get('href')
        full_img_page_url = f'{url}{img_url_rel}'

        #visit second page
        browser.visit(full_img_page_url)
        html = browser.html
        full_img_soup = soup(html, 'html.parser')
        full_img_element = full_img_soup.select('div.downloads')[0]
        full_img_rel = full_img_element.find('a', text='Sample').get('href')
        full_img_link = f'{url}{full_img_rel}'
        
        #print(full_img_link) #for debugging
        browser.back

        # append the list with new data
        hemispheres = {'img_url':full_img_link, 'title':product_title}
        hemisphere_image_urls.append(hemispheres)


    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls

    # 5. Quit the browser
    #browser.quit() #<- needs to be removed when converted to .py
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all()
