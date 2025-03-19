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
    browser.add_cookie({"name": "MUSIC_U", "value": "00076D96C7531C6AB2BAF545D52BC0CE3110C2171A6F1560F8165B86BEFD5087A06F86BB9B9D389C2788E83EC2322C8DFA2B4D7BBB0B990433F983B73512BCC76CCBAD85778C635F84C386A3A63F545C4987D1CD6AD050689BB610887180CE7A55E70F8173210C6EC1B1FEE2A352CDCE4B70AB92D986EBDEA01FD7CA112E6F0C4DF6914232A13C17FA5659E0846B1E92DD0EE3C3FAD62C32B0E381FB7720EB51777D33B16620F54C4B3E80E1230D79F7A1B489C6B2DC7068839AC9E2483425C3410F2819EEEA9B59F144727CED7059FB6C6F5F443FEFB34B9CE1D71F8F16BD326983572B6DE6ADDA30468F9250840E1877D9E2BD6B5B4F93D7B27CAF3FCDEFE3AB480E6186D9584866E9D4419C7603BC12137CD76995BCEB1AF15E6E4F59C52D861C82A4730A39D414BF54F93D0D92F9FD473F5A8F97FAEA7F05D24C92AD51F175A7131FED20A706CA3BFE5D3C2C133B77B5D73DB29E474411753D556A7B7B561B"})
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
