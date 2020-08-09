from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep
from re import findall
from random import randint
import json
from urllib.request import urlretrieve

# Get webpage details
def get_resource(driver, url):
    driver.get(url)
    return driver

# Load the entire page
def load_fullpage(driver):
    for i in range(1, 10):
        sleep(0.4)
        height = 1080*i
        driver.execute_script("window.scrollTo("+ str(height - 1080)+ ","+ str(height)+");")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == height*(i-1):
            break

# Extract links to all the articles in a page
def extract_article_links(driver):
    xpath = '//*[@id="product-results-view"]/div/div[2]/div/section/div/article/h3/a'
    wait_for_page_to_load(driver, xpath)
    
    art_links = driver.find_elements_by_xpath(xpath)
    
    links = []
    for link in art_links:
        links.append(link.get_attribute('href'))
    return links

# Find total number of pages for a product
def get_total_pagecount(driver):
    xpath = '//*[@id="product-results-view"]/div/div[2]/div/section/footer/ul/li[1]/ul'
    wait_for_page_to_load(driver, xpath)
    
    nextpages = driver.find_element_by_xpath(xpath).find_elements_by_tag_name('a')
    
    lastpage_link = nextpages[-1].get_attribute('href')
    last_pagenum = findall(r'[^\d]+(\d+)', lastpage_link)[-1]
    
    return int(last_pagenum)

# Get title of an article
def get_title_of_article(driver):
    xpath = ('//*[@id="product-page-product-title-lockup"]/div/h1')
    wait_for_page_to_load(driver, xpath)
    
    title_elem = driver.find_element_by_xpath(xpath)
    
    return title_elem.text

# Get details of a product
def get_article_details(driver):
    details = []
    
    xpath_for_description = '//*[@id="layer-0"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div/*/div/div[2]/p'
    wait_for_page_to_load(driver, xpath_for_description)
    details.append(driver.find_element_by_xpath(xpath_for_description).text)
    
    xpath_for_details = '//*[@id="layer-0"]/div/div[1]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/ul/*/span'
    details_elem = driver.find_elements_by_xpath(xpath_for_details)
    
    for elem in details_elem:
        details.append(elem.text)
    
    return details

# Get rating of a product
def get_product_rating_div(driver):
    rating_div = {}
    
    xpath = '//*[@id="reviews"]/section/div[1]/header/div/div[2]/*/span[3]'
    wait_for_page_to_load(driver, xpath)
    rating_elem = driver.find_elements_by_xpath(xpath)
    
    rating = 5
    for elem in rating_elem :
        rating_div[rating] = int(elem.text[0:-1])
        rating -= 1
    
    return rating_div

# Get image-url
def get_image_url(driver):
    xpath1 = '//*[@id="product-page-main-gallery-image"]/picture/img'
    xpath2 = '//*[@id="product-page-main-gallery-image"]/img'
    try :
        url = driver.find_element_by_xpath(xpath1).get_attribute('src')
    except :
        url = driver.find_element_by_xpath(xpath2).get_attribute('src')
    return url

# Get total number of pages with comments
def get_total_comment_pages(driver):
    xpath = '//*[@id="reviews"]/section/ul/li[1]/ul/li/a'
    pages = driver.find_elements_by_xpath(xpath)
    return int(pages[-1].text)

# Get comments on a page
def get_comments(driver, comment_list):
    xpath_for_reviews = '//*[@id="reviews"]/section/div[3]/div'
    tag_for_comment_heading = 'strong'
    xpath_for_comment_body = './*/div[1]/div[1]'
    xpath_for_date = './*/div[2]/span'
    
    reviews_elem = driver.find_elements_by_xpath(xpath_for_reviews)
    
    for review in reviews_elem:
        new_comment = {}
        new_comment['heading'] = review.find_element_by_tag_name(tag_for_comment_heading).text
        new_comment['body'] = review.find_element_by_xpath(xpath_for_comment_body).text
        new_comment['date'] = review.find_element_by_xpath(xpath_for_date).text
        
        comment_list.append(new_comment)

# Wait for xpath of a page to load
def wait_for_page_to_load(driver, xpath):
    timeout = 2
    retries = 1
    while retries <= 7:
        try:
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(driver, timeout).until(element_present)
            break
        except:
            driver.refresh()
            retries += 1

#Constants
DRIVER_PATH = "/usr/bin/chromedriver"
PATH_FILE = "./"
BASE_URL = "https://www.nordstrom.com/sr?keyword="
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

product = "t-shirt"

# Open a json file
out_file = open(PATH_FILE + "stage_0.json", "wb")
out_file.write(str("[\n").encode('utf-8'))
URL = BASE_URL + product

# Get a driver for URL
driver = get_resource(driver, URL)
load_fullpage(driver)

# Get total number of pages for this product
totalpages = get_total_pagecount(driver)

# Keep track of id
id = 1

#Now for each page for a product
for page_no in range (1, totalpages+1):
    page_url = URL + "&page=" + str(page_no)
    
    driver = get_resource(driver, page_url)    
    article_links = extract_article_links(driver)
    
    # For each article link
    for link in article_links:
        try :
            driver = get_resource(driver, link)        
            new_article = {}
            
            new_article['id'] = id
            new_article['title'] = get_title_of_article(driver)
            
            load_fullpage(driver)
            
            new_article['details'] = get_article_details(driver)
            new_article['rating_div'] = get_product_rating_div(driver)

            new_article['image'] = get_image_url(driver)

            new_article['comments'] = []
            try:
                total_comment_page_count = get_total_comment_pages(driver)
                
                # read comments for each item
                for page_no in range(1, min(3, total_comment_page_count)):
                    load_fullpage(driver)            
                    get_comments(driver, new_article['comments'])
                    # Go to the comment path
                    xpath = '//*/a[@href="?page='+str(page_no+1) + '"]'
                    page_elem = driver.find_element_by_xpath(xpath)
                    page_elem.click()
            except:
                pass
            
            # Write the data maintaining json structure
            if id != 1 :
                out_file.seek(-1, 1)
                out_file.write(str(",\n").encode('utf-8'))
            to_write = json.dumps(new_article, indent = 4)
            to_write += "]"
            out_file.write(to_write.encode('utf-8'))
            id = id + 1
            print(str(id-1) + " finished")
            
            sleep(2)
        except :
            pass
