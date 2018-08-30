from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import requests
import logging
import sys
import os
import argparse

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_cookies(username, password):
    # Setup chromedriver
    logging.info("starting chromedriver...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=options)

    # Log in to DN 
    logging.info("logging in via 'https://kund.dn.se/'...")
    driver.get('https://kund.dn.se/')
    driver.find_element_by_link_text('Logga in').click()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'login-button-dn'))
    )
    driver.find_element_by_id('form_username').send_keys(args.username)
    driver.find_element_by_id('form_password').send_keys(args.password)
    driver.find_element_by_id('login-button-dn').click()
    cookies = driver.get_cookies()
    logging.info("stopping driver...")
    driver.quit()
    return cookies

def save_pdf(cookies, datestring, path):
    logging.info("copying cookies to request session...")
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = "https://kund.dn.se/service/download/{}/DN.pdf".format(datestring)
    logging.info("accessing '{}'...".format(url))
    r = session.get(url, stream=True)
    chunk_size = 512
    logging.info("writing data to '{}'...".format(path))
    with open(path, 'wb') as file:
        for chunk in r.iter_content(chunk_size):
            file.write(chunk)
    logging.info("done!")

if __name__ == "__main__":
    # handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='/downloads', help="Path to download directory with or without a filename. Defaults to '/downloads'.")
    parser.add_argument('-d', '--date', type=str, default=date.today().strftime("%Y%m%d"), help="The date of the issue in the format 'YYYYMMDD'")
    parser.add_argument('-u', '--username', type=str, required=True, help="Username (registered e-mail address) on dn.se")
    parser.add_argument('-p', '--password', type=str, required=True, help="Password on dn.se")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        args.path = "{}/{}.pdf".format(args.path, args.date)

    cookies = get_cookies(args.username, args.password)
    save_pdf(cookies, args.date, args.path)






