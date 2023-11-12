# utils/driver_setup.py

# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config.setting import USER_APP

# Function to set up the Chrome driver
def setup_driver():
    # user_dir = f'C:/Users/{USER_APP}/AppData/Local/Google/Chrome/User Data'
    option = webdriver.ChromeOptions()
    # option.add_argument(f'--user-data-dir={user_dir}')
    option.add_argument('--lang=en-US')
    option.add_argument('--window-size=1200,1000')

    s = Service('C:\Driver\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=option)
    driver.get("https://www.instagram.com/accounts/login")
    return driver
