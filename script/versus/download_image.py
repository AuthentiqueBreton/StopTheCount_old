#!/usr/bin/env python3

"""
TO DO
"""
import time
from io import BytesIO
from tqdm import tqdm
from PIL import Image
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def get_images(list_looking_for, hint=None):
    """
    TO DO
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--user-data-dir=C:/Users/Nicolas/AppData/Local/Google/Chrome/User Data")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--window-size=2560,1440")
    driver = webdriver.Chrome(options=options)

    progress_bar = tqdm(list_looking_for, desc="Progression")

    for looking_for in list_looking_for:
        progress_bar.set_postfix({"Élément": looking_for})
        pinterest_url = generate_url(looking_for, hint)
        response = get_link(driver, pinterest_url)
        download_file(response, looking_for, hint)
        progress_bar.update(1)

    driver.quit()

def generate_url(looking_for, hint):
    """
    TO DO
    """
    looking_for = looking_for.replace(' ', '%20')

    if hint is not None:
        hint = '%20' + hint.replace(' ', '%20')
    else:
        hint = ''

    url = (f'https://www.pinterest.fr/search/pins/?q={looking_for}{hint}'
            '&rs=typo_auto_original&auto_correction_disabled=true')
    return url

def get_link(driver, url, num_results=20):
    """
    TO DO
    """
    driver.get(url=url)
    time.sleep(5)
    wait = WebDriverWait(driver, 10)
    css_selector = "img.hCL.kVc.L4E.MIw"

    image_urls = []
    while len(image_urls) < num_results:
        try:
            # Wait for the elements to be present
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))

            # Get the image elements and retrieve their URLs
            images = driver.find_elements(By.CSS_SELECTOR, css_selector)
            sorted_images = sorted(images, key=lambda img: (img.location['y'], img.location['x']))
            for image in sorted_images:
                try:
                    image_urls.append(image.get_attribute("src"))
                    if len(image_urls) == num_results:
                        break
                except StaleElementReferenceException:
                    continue
        except StaleElementReferenceException:
            continue

    urls_originals = []
    for image_url in image_urls:
        urls_originals.append(image_url.replace('236x', 'originals'))

    return link_and_file_verification(urls_originals)


def link_and_file_verification(urls):
    """
    TO DO
    """
    for url in urls:
        response = requests.get(url, stream=True, timeout=5)
        if response.status_code == 200:
            image_data = response.content
            with Image.open(BytesIO(image_data)) as img:
                width, height = img.size
                if 0.55 < width/height < 0.75:
                    return response

    url = 'https://i.pinimg.com/564x/6e/bf/a6/6ebfa6babb801c4981571b5636764a5d.jpg'
    return requests.get(url, stream=True, timeout=5)

def download_file(response, looking_for, hint):
    """
    TO DO
    """
    file_location = 'data/raw_images/'
    file_name = looking_for.replace(' ', '_')
    if hint is not None:
        file_name = file_name + '_' + hint.replace(' ', '_')
    file_name = file_name + '.jpg'

    with open(file_location + file_name, 'wb') as fichier:
        for chunk in response.iter_content(1024):
            fichier.write(chunk)
