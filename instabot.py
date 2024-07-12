import logging
import os
import time
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import load_comments, load_credentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InstaBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome()
        self.comments = load_comments()
        self.registered_users = []
        self.broken_accounts = []
        self.comment_ban_control = []
        self.working_accounts = []
        self.published = []
        self.published_control = 0
        self.login_error = 0
        self.count = 0
        self.error_control = 0
        self.previous_account = ""
        self.status = 0

    def sign_in(self):
        logging.info(f"Signing in with {self.username}")
        self.browser.get('https://www.instagram.com')
        try:
            email_input = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input"))
            )
            password_input = self.browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
            email_input.send_keys(self.username)
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(10)

            if self.browser.find_elements(By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input"):
                logging.error(f"Login failed for {self.username}")
                self.status = 0
            else:
                self.status = 1
                logging.info(f"Login successful for {self.username}")
        except Exception as e:
            logging.error(f"Exception during sign in: {str(e)}")
            self.login_error += 1
            if self.login_error < 5:
                self.sign_in()
            else:
                self.browser.delete_all_cookies()
                self.registered_users.clear()
                self.login_error = 0
                time.sleep(10)
                self.sign_in()

    def get_followers_and_comment(self):
        while True:
            self.browser.get("https://www.instagram.com/?variant=following")
            time.sleep(10)
            try:
                post_box = WebDriverWait(self.browser, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abc0._abcm'))
                )
                posts = post_box.find_elements(By.TAG_NAME, "article")
                for post in posts:
                    self.comment_on_post(post)
            except Exception as e:
                logging.error(f"Error fetching posts: {str(e)}")
            time.sleep(120)
            self.count += 1
            if self.count == 30:
                self.cleanup()
                self.sign_in()

    def comment_on_post(self, post):
        try:
            get_time = post.find_element(By.TAG_NAME, "time").text
            get_link = post.find_element(By.CSS_SELECTOR, "._aaqd._a6hd").get_attribute("href")
            if ("MINUTES" in get_time or "SECONDS" in get_time) and get_link not in self.published:
                post.find_element(By.CSS_SELECTOR, "._ablz").click()
                time.sleep(1)
                send_comment = post.find_element(By.CSS_SELECTOR, "._ablz")
                send_comment.send_keys(self.comments[randint(0, len(self.comments) - 1)])
                send_comment.send_keys(Keys.ENTER)
                self.published.append(get_link)
                time.sleep(20)
                logging.info(f"Commented on post: {get_link}")
        except Exception as e:
            logging.error(f"Error commenting on post: {str(e)}")

    def cleanup(self):
        try:
            os.system("rm -rf /tmp/* /tmp/.*")
            self.published.clear()
            logging.info("Cleaned up temporary files.")
        except Exception as e:
            logging.error(f"Cleanup error: {str(e)}")

if __name__ == "__main__":
    credentials = load_credentials()
    for user in credentials["users"]:
        bot = InstaBot(user["username"], user["password"])
        bot.sign_in()
        bot.get_followers_and_comment()
