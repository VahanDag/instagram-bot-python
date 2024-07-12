import csv
import json
import os
import time
from gettext import find
from random import randint

import selenium.common.exceptions as d
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InstaBot():
    count = 0
    published = []
    publishedControl = 0
    loginError = 0
    status = 0
    registeredUsers = []
    workingAccounts = [
        "charlsiealcombright6", "demet.sarisin123", "jonathonwalston7", "simge.saskin12"]
    errorControl = 0
    previousAccount = ""
    brokenAccounts = []
    f = open("comments.csv")
    data = csv.reader(f)
    comments = list([i[0] for i in data])
    loginControl = 0
    commentBanControl = []

    def __init__(self, username, password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        self.previousAccount = username
        self.sign()

    def sign(self):
        self.browser.get('https://www.instagram.com')
        try:
            try:

                self.emailInput = WebDriverWait(self.browser, 20). until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input")))

                self.passwordInput = self.browser.find_element(
                    By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')

                self.emailInput.send_keys(self.username)
                self.passwordInput.send_keys(self.password)
                self.passwordInput.send_keys(Keys.ENTER)
            except:
                pass
            time.sleep(10)
            try:
                self.browser.find_element(
                    By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input")
                self.status = 0
            except:
                self.status = 1

            if self.status == 0:
                print(f"Grirs Hatasi: {self.username}")
                f = open("users.json")
                data = json.load(f)
                for x in data["users"]:
                    if x["username"] != self.username and x["username"] in self.workingAccounts:
                        self.workingAccounts.remove(self.username)
                        self.brokenAccounts.append(self.username)
                        self.username = x["username"]
                        self.password = x["password"]
                        f.close()
                        self.sign()
            else:
                while True:
                    try:
                        WebDriverWait(self.browser, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '._acan._acap._acas'))).click()
                        time.sleep(3)
                    except:
                        print("save user error")

                    self.browser.get(
                        "https://www.instagram.com/?variant=following")
                    try:
                        WebDriverWait(self.browser, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '._a9--._a9_1'))).click()
                    except:
                        print("Bildirim Goster Butonu EXCEPT")

                    time.sleep(2)
                    try:
                        clickNavbar = self.browser.find_element(By.CSS_SELECTOR, "._acus").find_elements(
                            By.CSS_SELECTOR, "._acut")[-1].click()
                    except:
                        clickNavbar = self.browser.find_element(By.CSS_SELECTOR, ".xhuyl8g.xl5mz7h").find_element(
                            By.TAG_NAME, "a").click()
                    time.sleep(2)
                    changeAccount = self.browser.find_elements(
                        By.CSS_SELECTOR, "._abm4")[-2].click()
                    time.sleep(3)
                    try:
                        getUsers = self.browser.find_element(
                            By.CSS_SELECTOR, "._ab9o._ab9w._abcm").find_elements(By.CSS_SELECTOR, "._aacl._aaco._aacw._aacx._aad6")
                        for i in getUsers:
                            print(i.text)
                            if i.text not in self.registeredUsers and i.text != "" and i.text not in self.brokenAccounts:
                                self.registeredUsers.append(i.text)

                        print(self.registeredUsers)
                        print(len(getUsers))
                        print(self.brokenAccounts)
                        if len(self.registeredUsers) == len(self.workingAccounts):
                            print("Kullanıcılar Tamamlanndı..")
                            clickNavbar
                            self.getFollowersAndComment()

                        else:
                            # click "login to another account" for adding another user
                            # self.browser.find_element(By.CSS_SELECTOR, ".f0dnt3l3").find_elements(
                            #     By.TAG_NAME, "div")[-1].find_element(By.TAG_NAME, "button").click()
                            self.browser.find_elements(By.CSS_SELECTOR, "._ab8w._ab94._ab97._ab9h")[
                                -1].find_element(By.TAG_NAME, "button").click()
                    except:
                        print("getUsers HATA")

                    inputEmail = WebDriverWait(self.browser, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input')))
                    inputPassword = self.browser.find_element(
                        By.XPATH, '//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
                    saveUser = self.browser.find_element(
                        By.CSS_SELECTOR, "._aahg").click()
                    time.sleep(3)
                    f = open("users.json")
                    data = json.load(f)
                    for x in data["users"]:
                        print((x["username"] not in self.registeredUsers), (self.username !=
                              x["username"]), (x["username"] in self.workingAccounts))
                        if (x["username"] not in self.registeredUsers) and (self.username != x["username"]) and (x["username"] in self.workingAccounts):
                            print("ife girdi")
                            self.username = x["username"]
                            self.password = x["password"]
                            inputEmail.send_keys(self.username)
                            inputPassword.send_keys(self.password)
                            inputPassword.send_keys(Keys.ENTER)
                            print(f"{self.username} kullanicisi eklendi.")
                            self.registeredUsers.clear()
                            time.sleep(10)
                            break

                    try:
                        while True:
                            print("while is gone")
                            WebDriverWait(self.browser, 5).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[1]/div/label/input')))
                            self.workingAccounts.remove(self.username)
                            self.brokenAccounts.append(self.username)
                            print(f"hata var {self.username}")
                            for i in data["users"]:
                                if (i["username"] not in self.registeredUsers) and (self.username != i["username"]) and (i["username"] in self.workingAccounts):
                                    self.username = i["username"]
                                    self.password = i["password"]
                                    inputEmail.click()
                                    time.sleep(0.5)
                                    inputEmail.send_keys(Keys.chord(
                                        Keys.CONTROL, "a", Keys.DELETE))
                                    time.sleep(0.5)
                                    inputPassword.click()
                                    time.sleep(0.5)
                                    inputPassword.send_keys(Keys.chord(
                                        Keys.CONTROL, "a", Keys.DELETE))
                                    time.sleep(1)
                                    inputEmail.send_keys(self.username)
                                    inputPassword.send_keys(self.password)
                                    inputPassword.send_keys(Keys.ENTER)
                                    self.registeredUsers.clear()
                                    time.sleep(20)
                    except:
                        print(f"burda hata yok {self.username}")
                    f.close()

                    try:
                        for x in self.browser.find_element(By.CSS_SELECTOR, ".lAPmk").find_elements(By.CSS_SELECTOR, ".MHDUK"):
                            if x.find_element(By.CSS_SELECTOR, ".l9hKg").text != self.username:
                                x.click()
                                time.sleep(10)
                                break
                            else:
                                pass
                    except:
                        print("kullanici secme hata!")

        except:
            self.loginError += 1
            print(f"Login Except Calisti: {self.username}")
            if self.loginError == 5:
                self.browser.delete_all_cookies()
                self.registeredUsers.clear()
                self.loginError = 0
            time.sleep(10)
            self.sign()

    def getFollowersAndComment(self):
        while True:
            self.browser.get(
                "https://www.instagram.com/?variant=following")
            # self.browser.find_element(By.CSS_SELECTOR,"._a9--._a9_1").click()
            time.sleep(10)
            try:
                postBox = WebDriverWait(self.browser, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abc0._abcm')))

                # self.browser.execute_script(
                #     "window.scrollTo(0, document.body.scrollHeight);")

                posts = postBox.find_elements(By.TAG_NAME, "article")

                for post in posts:
                    getTime = post.find_element(By.TAG_NAME, "time").text
                    getLink = post.find_element(
                        By.CSS_SELECTOR, "._aaqd._a6hd").get_attribute("href")
                    getLink = getLink + self.username

                    if (("MINUTES" in getTime) or ("DAKIKA" in getTime) or ("SANIYE" in getTime) or ("SECONDS" in getTime)) and (getLink not in self.published):
                        try:
                            WebDriverWait(self.browser, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "._ablz")))
                            textarea = post.find_element(
                                By.CSS_SELECTOR, "._ablz")
                            textarea.click()
                            time.sleep(1)
                            sendComment = post.find_element(
                                By.CSS_SELECTOR, "._ablz")

                            sendComment.send_keys(
                                self.comments[randint(0, 21)])

                            time.sleep(2)
                            sendComment.send_keys(Keys.ENTER)
                            time.sleep(20)
                            self.browser.execute_script(
                                "window.scrollTo(0, 774);")
                            self.published.append(getLink)

                        except:
                            print("yorum atmadi")
                            try:
                                self.browser.find_element(
                                    By.CSS_SELECTOR, "._a9--._a9_1").click()
                                print(
                                    f"{self.username} Hesabı Yorum Engeli Yedi..")
                                time.sleep(1)
                                self.commentBanControl.append(self.username)
                            except:
                                pass

                            self.browser.execute_script(
                                "window.scrollTo(0, 774);")
                    else:
                        self.publishedControl += 1
                        print("else calisti")
            except:
                print("PostBox EXCEPT")
            time.sleep(120)
            self.count += 1
            if self.count == 30:
                try:
                    print("OS CALISTI")
                    os.system("rm -rf /tmp/* /tmp/.*")
                    self.published.clear()
                    time.sleep(60)
                    self.sign()
                except:
                    print("OS EXCEPT")
                    self.published.clear()
                    time.sleep(60)
            hour = str(time.gmtime())
            # if int(hour[62]) > 23 and int(hour[62]) < 5:
            #     print("Bekliyor..")
            #     self.browser.delete_all_cookies()
            #     # self.browser.quit()
            #     time.sleep((int(hour[62]) - 6) * 3600)
            try:
                self.browser.find_element(
                    By.CSS_SELECTOR, "._a9--._a9_1").click()
                print(
                    f"{self.username} Hesabı Yorum Engeli Yedi..")
                time.sleep(1)
            except:
                pass
            
            if self.publishedControl >= 50:
                time.sleep(200)
                self.publishedControl = 0

            if self.count == 40:
                self.published.clear()
                self.count = 0
            try:
                banControl = self.browser.find_element(
                    By.XPATH, "/html/body/div[1]/section/main/div[2]/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/span").text
                print(f"{self.username} hesabında hata: {banControl}")
                self.workingAccounts.remove(self.brokenAccounts)
                self.brokenAccounts.append(self.username)
                self.browser.delete_all_cookies()
                time.sleep(10)
                self.sign()
            except:
                pass

            try:
                clickNavbar = self.browser.find_element(By.CSS_SELECTOR, "._acus").find_elements(
                    By.CSS_SELECTOR, "._acut")[-1].click()
            except:
                clickNavbar = self.browser.find_element(By.CSS_SELECTOR, ".xhuyl8g.xl5mz7h").find_element(
                    By.TAG_NAME, "a").click()
            time.sleep(5)
            self.changeAccount = self.browser.find_elements(
                By.CSS_SELECTOR, "._abm4")[-2].click()
            time.sleep(5)
            self.getUsers = self.browser.find_elements(
                By.CSS_SELECTOR, "._aacl._aaco._aacu._aacx._aada")
            print(len(self.getUsers), "Get users")
            if len(self.getUsers) <= 5:
                self.getUsers = self.browser.find_elements(
                    By.CSS_SELECTOR, "._aacl._aaco._aacu._aacx._aada")
            else:
                self.getUsers = self.browser.find_element(
                    By.CSS_SELECTOR, "._ab9o._ab9w._abcm").find_elements(By.CSS_SELECTOR, "._aacl._aaco._aacw._aacx._aad6")

            while True:

                randomNumber = randint(1, len(self.workingAccounts)-1)
                self.username = self.getUsers[randomNumber].text
                if (self.username in self.workingAccounts) and (self.username != self.previousAccount) and (self.username not in self.commentBanControl):
                    # randomNumber = randint(1, len(self.workingAccounts)-1)
                    # self.username = self.getUsers[randomNumber].find_element(
                    #     By.TAG_NAME, "div").text
                    self.previousAccount = self.username
                    self.getUsers[randomNumber].click()
                    break
                # else:
                #     self.getUsers[randomNumber].click()

            time.sleep(15)
            self.browser.refresh()
            time.sleep(10)

            try:
                self.browser.find_element(By.CSS_SELECTOR, ".iNy2T")
                self.errorControl = 0
            except:
                self.errorControl = 1

            if self.errorControl == 0:
                self.workingAccounts.remove(self.username)
                self.brokenAccounts.append(self.username)
                print(f"{self.username} Hesabına Girmiyor..")
                try:
                    for x in self.browser.find_element(By.CSS_SELECTOR, ".lAPmk").find_elements(By.CSS_SELECTOR, ".MHDUK"):
                        nameUser =x.find_element(By.CSS_SELECTOR, ".l9hKg").text
                        if (nameUser != self.username) and (nameUser not in self.brokenAccounts) and (nameUser not in self.commentBanControl):
                            x.click()
                            time.sleep(15)
                            break
                        else:
                            pass
                except:
                    f = open("users.json")
                    data = json.load(f)

                    for x in data["users"]:
                        if (self.username != x["username"]) and (x["userrname"] not in self.brokenAccounts):
                            self.emailInput
                            self.passwordInput

                            self.emailInput.send_keys(x["username"])
                            self.passwordInput.send_keys(x["password"])
                            self.passwordInput.send_keys(Keys.ENTER)
                            print(
                                f"{x['username']} Hesabına Giriş Yapılıyor..")
                            time.sleep(15)
                    f.close()


insta = InstaBot("simge.saskin12", "password")
