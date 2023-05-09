#!/usr/bin/env python3

"""
TO DO
"""

import time
import re
from selenium import webdriver

def get_image(search, hint=None):
    """
    TO DO
    """
    search = search.replace(' ', '%20')
    if hint is not None:
        hint = '%20' + hint.replace(' ', '%20')
    else:
        hint = ''
    url = f'https://www.pinterest.fr/search/pins/?q={search}{hint}'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url=url)

    regex = r"https://i\.[A-Za-z]+\.([A-Za-z0-9]+(/[A-Za-z0-9]+)+)\.jpg"
    image_link = None
    while image_link is None:
        image_link = re.search(regex, str(driver.page_source))
        time.sleep(0.1)
    image_link = image_link.group().replace('236x', 'originals')

    return image_link
