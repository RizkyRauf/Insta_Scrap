import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.setting import USERNAME_IG, PASSWORD_IG

class InstagramLogin:
    def __init__(self, chrome_driver_path):
        self.chrome_driver_path = chrome_driver_path
        self.cookies_dir = "Cookies"
        self.cookies_file = os.path.join(self.cookies_dir, "cookies.pkl")
        os.makedirs(self.cookies_dir, exist_ok=True)
        self.driver = None

    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=en-US')
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--log-level=3')

        self.driver = webdriver.Chrome(service=Service(self.chrome_driver_path), options=options)

    def login_with_cookies(self):
        self.initialize_driver()
        self.driver.get("https://www.instagram.com")

        try:
            if os.path.exists(self.cookies_file):
                self.load_cookies()
                self.driver.refresh()
                time.sleep(3)
                print("Login dengan cookies berhasil!")

            else:
                print("Cookies tidak ditemukan. \nMencoba login manual")
                self.login_manually()

                if os.path.exists(self.cookies_file):
                    print("Cookies ditemukan. Login dengan cookies.")
                    self.load_cookies()
                    self.driver.refresh()

        except Exception as e:
            print("Login dengan cookies gagal:", e)

    def load_cookies(self):
        with open(self.cookies_file, 'rb') as cookie_file:
            cookies = pickle.load(cookie_file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def login_manually(self):
        self.initialize_driver()
        self.driver.get("https://www.instagram.com/accounts/login")

        try:
            username_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "username")))
            password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.NAME, "password")))
            login_button = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']")))

            username_field.send_keys(USERNAME_IG)
            time.sleep(3)
            password_field.send_keys(PASSWORD_IG)
            time.sleep(3)
            login_button.click()

            time.sleep(5)
            self.handle_not_now_buttons()
            print("Login manual berhasil!")
            self.save_cookies()

        except Exception as e:
            print("Login manual gagal:", e)
            self.driver.quit()

    def handle_not_now_buttons(self):
        try:
            not_now_1 = WebDriverWait(self.driver, timeout=10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='_ac8f']//div[contains(@class, 'x1i10hfl') and contains(@class, 'xa49m3k') and contains(@class, 'xqeqjp1') and contains(@class, 'x2hbi6w') and contains(@class, 'xdl72j9') and contains(@class, 'x2lah0s') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x2lwn1j') and contains(@class, 'xeuugli') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1ja2u2z') and contains(@class, 'x1t137rt') and contains(@class, 'x1q0g3np') and contains(@class, 'x1lku1pv') and contains(@class, 'x1a2a7pz')]")))
            time.sleep(5)
            not_now_1.click()
            time.sleep(5)
            not_now = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
            not_now.click()
        except TimeoutError:
            print("Not Now button not found")

    def save_cookies(self):
        if os.path.exists(self.cookies_file):
            os.remove(self.cookies_file)

        cookies = self.driver.get_cookies()

        with open(self.cookies_file, "wb") as cookie_file:
            pickle.dump(cookies, cookie_file)

        print("Cookies telah disimpan di direktori:", self.cookies_dir)

    def close(self):
        if self.driver:
            self.driver.quit()
            print("Driver ditutup.")

if __name__ == "__main__":
    instagram_login = InstagramLogin('C:\Driver\chromedriver.exe')
    instagram_login.login_with_cookies()
