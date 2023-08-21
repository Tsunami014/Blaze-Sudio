from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
import time
from selenium.webdriver.common.by import By
from math import inf
from webdriver_manager.chrome import ChromeDriverManager

def signin(driver, url, wait_for_by, wait_for_value, cookie_name):
    driver.maximize_window()
    driver.get(url)

    WebDriverWait(driver, inf).until(lambda x: x.find_element(wait_for_by, wait_for_value))
    all_cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie['name']] = cookie['value']
    return

options = webdriver.ChromeOptions()
#options.add_argument("--user-data-dir=C:/Users/{userName}/AppData/Local/Google/Chrome/User Data/Profile {#}/")
options.add_argument('--disable-web-security')
options.add_argument('--allow-running-insecure-content')

# chrome, get bard
print('Sign in to bard, google\'s AI.')
d = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
res = signin(d, "https://bard.google.com/", By.CLASS_NAME, "input-area-container ng-tns-c1494065745-1", " __Secure-1PSID")
