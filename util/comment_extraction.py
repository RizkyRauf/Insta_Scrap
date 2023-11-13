# Import libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from config.logings import initialize_logging
import logging
import time


class CommentExtractor:
    def __init__(self, driver, log_level=logging.INFO):
        self.driver = driver
        self.log_level = log_level
        self.logger = initialize_logging("logs/comments.log", self.log_level)

    # Function to scroll and load comments on an Instagram post
    def scroll_to_load_comments(self):
        comment_section_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='x5yr21d xw2csxc x1odjw0f x1n2onr6']")
            )
        )
        previous_height = self.driver.execute_script(
            "return arguments[0].scrollHeight", comment_section_element
        )
        while True:
            self.driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight);",
                comment_section_element,
            )
            time.sleep(10)
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", comment_section_element
            )
            if new_height == previous_height:
                break
            previous_height = new_height
    #
    # def _extract_comment(self) -> None:
    #     comment_list: list = []
    #     try:
    #         comment_elements = self.driver.find_elements(
    #             By.XPATH, "//div[@class='...']/div[@class='...']/span"
    #         )
    #         for comment in comment_elements:
    #             comment_list.append(comment.text)
    #     except NoSuchElementException as error_element:
    #         self.logger.error("error blablalb {}".fomat(error_element))

    # Function to extract comments, usernames, likes, dates, and links from an Instagram post
    def extract_comments(self, post_id):
        post_link = f"https://www.instagram.com/p/{post_id}"
        self.logger.info(f"Extracting comments from post: {post_link}")

        self.driver.get(post_link)
        time.sleep(5)

        self.scroll_to_load_comments()
        time.sleep(20)

        comments_list = []
        usernames = []
        likes = []
        dates = []
        links = []

        # Extract comments
        try:
            comment_elements = self.driver.find_elements(
                By.XPATH,
                "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1']/span",
            )
            for comment in comment_elements:
                comments = comment.text
                comments_list.append(comments)
        except NoSuchElementException:
            comments_list = []
            self.logger.error("Error extracting comments")

        # Extract usernames
        try:
            user_elements = self.driver.find_elements(
                By.XPATH,
                f"{}",
            )
            for user in user_elements:
                username = user.text
                usernames.append(username)
        except NoSuchElementException:
            usernames = []
            self.logger.error("Error extracting usernames")

        # Extract likes
        try:
            like_elements = self.driver.find_elements(
                By.XPATH,
                "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1']/div[1]/span/span",
            )
            for like in like_elements:
                liks = like.text

                if "likes" in liks:
                    liks = liks.replace("likes", "")
                elif "like" in liks:
                    liks = liks.replace("like", "")
                else:
                    liks = "0"

                likes.append(liks)
        except NoSuchElementException:
            likes = []
            self.logger.error("Error extracting likes")

        # Extract date
        try:
            date_elements = self.driver.find_elements(
                By.XPATH,
                "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div/span/a/time[@class='x1ejq31n xd10rxx x1sy0etr x17r0tee x1roi4f4 xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6']",
            )
            for date in date_elements:
                date_text = date.get_attribute("datetime")
                date_text = str(date_text)  # Convert
                date_text = date_text.replace("T", " ").replace(".000Z", "")
                formatted_date = date_text
                dates.append(formatted_date)
        except NoSuchElementException:
            dates = []
            self.logger.error("Error extracting dates")

        # Extract links
        try:
            link_elements = self.driver.find_elements(
                By.XPATH,
                "//div[@class='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/div/span/a",
            )
            for link in link_elements:
                link_text = link.get_attribute("href")

                if "/p/" in link_text:
                    links.append(link_text)
        except NoSuchElementException:
            links = []
            self.logger.error("Error extracting links")

        # Check the lengths of comments and usernames lists
        if (
            len(comments_list) != len(usernames)
            or len(comments_list) != len(likes)
            or len(comments_list) != len(dates) != len(links)
        ):
            # Log or handle this mismatch
            self.logger.warning(
                f"Warning: Mismatch between comments ({len(comments_list)}), usernames ({len(usernames)}), likes ({len(likes)}), dates ({len(dates)}) and links ({len(links)})"
            )

        # Ensure that all lists have the same length by padding the shorter ones
        min_length = min(
            len(comments_list), len(usernames), len(likes), len(dates), len(links)
        )
        comments_list = comments_list[:min_length] if comments_list else []
        usernames = usernames[:min_length] if usernames else []
        likes = likes[:min_length] if likes else []
        dates = dates[:min_length] if dates else []
        links = links[:min_length] if links else []

        data = {
            "usernames": usernames,
            "dates": dates,
            "comments": comments_list,
            "likes": likes,
            "links": links,
            "type": ["comment"] * len(usernames),
        }

        return data
