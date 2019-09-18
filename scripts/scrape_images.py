from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

url_prefix = 'https://www.airbnb.com.au/rooms/'

with open('data/sydney.csv') as listings:
    next(listings)

    count = 0
    for listing in listings:
        if count == 2500:
            break

        id = listing.strip().split(',')[0]
        url = url_prefix + id

        driver = webdriver.Firefox()
        driver.get(url)

        # make sure dynamic content is all loaded
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()

        srcs = []
        # pull out img tags
        for img in soup.find_all('img'):
            src = img.get('src')
            if src.startswith('https://a0.muscache.com/im/pictures/') and src.endswith('large'):
                srcs.append(src)
        
        if len(srcs) == 5:
            # save each img url in file name given by listing id
            f = open('data/listing-images/sydney/' + id, 'w+')

            for src in srcs:
                f.write(src + '\n')

            f.close()
            count += 1

