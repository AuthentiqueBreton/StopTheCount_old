#!/usr/bin/env python3

"""
TO DO
"""

import logging
import tweepy as tw

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGGER = logging.getLogger(__name__)

def get_tweets(client, user_name, tweet_id):
    """
    TO DO
    """
    authors = []
    contents = []
    ignored_tweets = 0

    search = client.search_recent_tweets
    query = f"to:{user_name} in_reply_to_status_id:{tweet_id}"
    for result in tw.Paginator(search, query, expansions='author_id', max_results=100).flatten(500):

        author_id = int(result.data['author_id'])
        tweet_content = result.data['text']

        if author_id not in authors:
            authors.append(author_id)
            contents.append(tweet_content)
        else:
            ignored_tweets += 1
            LOGGER.debug('%s already found in authors', author_id)

    return contents, ignored_tweets

def get_tweets_by_url(url):
    """
    TO DO
    """
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument("--user-data-dir=C:/Users/Nicolas/AppData/Local/Google/Chrome/User Data")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--window-size=2560,1440")
    driver = webdriver.Chrome(options=options)

    driver.get(url=url)

    wait = WebDriverWait(driver, 10)
    #xpath = "//div[@class='css-901oao css-cens5h r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']/span[@class='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0']"
    xpath = "//div[@class='css-175oi2r r-18u37iz r-1udh08x r-i023vh r-1qhn6m8 r-o7ynqc r-6416eg r-1ny4l3l r-1loqt21']"

    propositions_text = []
    old_len = 0
    new_len = 1

    down_y = 0
    down_prop = None

    while old_len != new_len:

        old_len = len(propositions_text)
        # Wait for the elements to be present
        wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

        # Get the image elements and retrieve their URLs
        #propositions = driver.find_elements(By.CSS_SELECTOR, css_selector)
        propositions_obj = driver.find_elements(By.XPATH, xpath)
        propositions_text = list(dict.fromkeys(propositions_text + [new_p.text for new_p in propositions_obj]))
        new_len = len(propositions_text)

        actual_y = 0
        for p in propositions_obj:
            try:
                actual_y = p.location['y']
            finally:
                if actual_y > down_y:
                    down_y = actual_y
                    down_prop = p

        driver.execute_script("arguments[0].scrollIntoView()", down_prop)
        time.sleep(2)

    return propositions_text
