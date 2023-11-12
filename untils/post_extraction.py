# Import libraries
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from config.logings import initialize_logging
import logging

class PostExtractor:
    def __init__(self, driver, log_level=logging.INFO):
        self.driver = driver
        self.log_level = log_level
        self.logger = initialize_logging('logs/post.log', self.log_level)

    def extract_post(self, post_id):
        post_link = f"https://www.instagram.com/p/{post_id}"
        self.logger.info(f"Extracting post from link: {post_link}")

        self.driver.get(post_link)

        # Extract username of the post
        try:
            username_element = self.driver.find_element(By.XPATH, "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/span/div/a/div/div/span")
            username = username_element.text
        except NoSuchElementException:
            username = None
            self.logger.error("Error extracting username")

        # Extract post content
        try:
            post_content_element = self.driver.find_element(By.XPATH, "//div/span[@class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj']")
            post_content = post_content_element.text
        except NoSuchElementException:
            post_content = None
            self.logger.error("Error extracting post content")

        # Extract post date
        try:
            datetime_post_element = self.driver.find_element(By.XPATH, "//span[@class='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x1roi4f4 x10wh9bi x1wdrske x8viiok x18hxmgj']/time[@class='xsgj6o6']")
            date_post = datetime_post_element.get_attribute("datetime")
            date_post = date_post.replace("T", " ").replace(".000Z", "")
            formatted_date = date_post
        except NoSuchElementException:
            formatted_date = None
            self.logger.error("Error extracting post date")

        data = {
            "username": [username],
            "date": [formatted_date],
            "comments": [post_content],
            "likes": ["0"],
            "links": [post_link],
            "type": ["post"],
        }

        return data
