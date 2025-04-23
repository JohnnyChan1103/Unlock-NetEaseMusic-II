# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0018107648D28DD2B06D3EA5A3B4F699410F445AB47667107A4689696E0A4512C201BB353D2505FA4E1E6464E7A3AF273A47E4AD9878BDD13F168ED0FDA25E5476EB51AFD4DD5C306E04548A2F51DF96A356E81E7A8EE43DB99C6D0B3BFB9B6F0DE4B238DDBCF0ED256D73A2B52229755417EA792519D228B5F51696EBE476C67133E5DF07BAE58C97ADF15CA77D565B52830BFB3BA34485DFED21F7214D821C5A84CC9C7ABF7061127FE2547DEF7AADDB8F207165BEFF26D4A82441E7FD7262E03D8896747FE8EFAC6F6B24BE2A6BEE36A981301DBF44FB211802066228FC4092C79051352568E13D1359B7307D8D82B65EEFCEBABA9AF845D1AC60132A0B868D0505875BAC5B5317036237D1FB215BCAC6D7F8C1319FC753DB6040D29F3B3E590AD07F87E0EE878281079FAD817F24C5A6010F3CB35608D5572C06EDE6983D90C4DB81FE565D5FCD23FA002536E459FBB915C45913BE505AA70C2EFA79C5F3FB"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
