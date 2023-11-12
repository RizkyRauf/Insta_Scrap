import os
from datetime import datetime
import pandas as pd
from get_cookies import InstagramLogin
from untils.comment_extraction import CommentExtractor
from untils.post_extraction import PostExtractor
from config.logings import initialize_logging
import logging

class InstagramScraper:
    def __init__(self, driver_path, log_level=logging.INFO):
        self.driver_path = driver_path
        self.log_level = log_level
        self.logger = initialize_logging('logs/instagram_scraper.log', self.log_level)

    def login(self):
        self.instagram_login = InstagramLogin(self.driver_path)
        self.instagram_login.login_with_cookies()

    def extract_data_from_posts(self, post_ids):
        df_combined = pd.DataFrame()

        if post_ids:
            post_extractor = PostExtractor(self.instagram_login.driver)
            comment_extractor = CommentExtractor(self.instagram_login.driver)

            for post_id in post_ids:
                data_post = post_extractor.extract_post(post_id)
                data_comments = comment_extractor.extract_comments(post_id)

                data_combined = {
                    "username": [data_post["username"][0]] + data_comments["usernames"],
                    "date": [data_post["date"][0]] + data_comments["dates"],
                    "comments": [data_post["comments"][0]] + data_comments["comments"],
                    "likes": ["0"] + data_comments["likes"],
                    "links": [data_post["links"][0]] + data_comments["links"],
                    "type": ["post"] + ["comment"] * len(data_comments["usernames"])
                }

                df_combined = pd.concat([df_combined, pd.DataFrame(data_combined)], ignore_index=True)

        return df_combined

    def save_data_to_excel(self, df_combined, output_folder="output_data"):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        current_datetime = datetime.now().strftime("%Y-%m-%d")
        xlsx_file_name = f"data_instagram_{current_datetime}.xlsx"
        xlsx_file_path = os.path.join(output_folder, xlsx_file_name)
        df_combined.to_excel(xlsx_file_path, index=False, engine='openpyxl')
        self.logger.info(f"Data has been saved in the folder {output_folder} with the file name {xlsx_file_name}")

    def run(self, post_ids):
        self.login()
        df_combined = self.extract_data_from_posts(post_ids)
        self.save_data_to_excel(df_combined)
        self.instagram_login.close()

if __name__ == "__main__":
    driver_path = 'C:\Driver\chromedriver.exe'
    post_ids = ["CytMIPJS6ch", "CyygMRpyhxi"]
    scraper = InstagramScraper(driver_path)
    scraper.run(post_ids)
