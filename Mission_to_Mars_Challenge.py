

# In[4]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


# In[7]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[8]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[9]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[10]:


slide_elem.find('div', class_='content_title')


# In[11]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[12]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[13]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[14]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[15]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[16]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[17]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[18]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[19]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[20]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[21]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)


# In[22]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []


# In[23]:


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


# In[24]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[25]:


# 5. Quit the browser
browser.quit()





