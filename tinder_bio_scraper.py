from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests


s = Service(ChromeDriverManager().install())
options = Options()
options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
driver = webdriver.Chrome(service=s, chrome_options=options)

class TinderBot:
    def __init__(self):
        self.name_path='//h1[@data-testid="recCard__name"]'
        self.age_path = '//span[@data-testid="recCard__age"]'
        self.city_path = '//div[@data-testid="info-city"]'
        self.bio_path = '//div[@data-testid="info-bio"]'
        self.interests_path = '//div[@data-testid="interest"]'
        self.descriptors_path = '//div[@data-testid="descriptor"]'
        self.like_path = '//button[@data-testid="gamepadLike"]'
        self.dislike_path = '//button[@data-testid="gamepadDislike"]'
        self.gender_path = '//div[@data-testid="info-genderAndOrientation"]'
        self.outoflikes_path = '//div[@data-testid="dialog-out-of-likes"]'

    def login(self,driver):
        driver.get('https://tinder.com/app/recs')
        main_page = driver.current_window_handle
        login = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//a[@data-testid="appLoginBtn"]')))
        # login = driver.find_element(By.XPATH, '//a[@data-testid="appLoginBtn"]')
        login.click()
        time.sleep(3)
        fb = driver.find_element(By.XPATH, '//button[@data-testid="login"]')
        fb.click()

        for handle in driver.window_handles:
            if handle != main_page:
                login_page = handle

        driver.switch_to.window(login_page)
        agg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//button[@data-testid="cookie-policy-manage-dialog-accept-button"]')))
        # agg = driver.find_element(By.XPATH, '//button[@data-testid="cookie-policy-manage-dialog-accept-button"]')
        agg.click()

        time.sleep(1)
        # enter the email
        driver.find_element(By.XPATH, '//*[@id ="email"]').send_keys("mail")
        time.sleep(1)
        # enter the password
        driver.find_element(By.XPATH, '//*[@id ="pass"]').send_keys("password")
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@name ="login"]').click()

        driver.switch_to.window(main_page)
        # driver.find_element(By.XPATH, '//button[@data-testid="allow"]').click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//button[@data-testid="allow"]'))).click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[@data-testid="decline"]').click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, '//button[@data-testid="privacyPreferencesAccept"]').click()
        time.sleep(5)
        self.random_time()

    def start(self,driver):
        driver.get('https://tinder.com/app/recs')
        time.sleep(5)
        self.random_time()

    def random_time(self):
        time=random.uniform(random.uniform(0.9,1.7), random.uniform(4.5,5.9))
        return time

    def action(self,driver):
        action = random.randint(0, 1)
        if action == 0:
            button = driver.find_element(By.XPATH,self.dislike_path)
        else:
            button = driver.find_element(By.XPATH, self.like_path)
        button.click()


        random_action_probability = random.randint(0, 3)
        if random_action_probability == 1: #25% chance
            random_action=random.randint(0, 2)
            if random_action ==0:
                body = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                body.send_keys(Keys.UP)
                time.sleep(0.3)
                body.send_keys(Keys.DOWN)
            elif random_action==1:
                body = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                body.send_keys(Keys.SPACE)
                time.sleep(1)
                body.send_keys(Keys.SPACE)

        self.random_time()

    def get_data(self,driver):
        time.sleep(random.uniform(random.uniform(0.4,0.7), random.uniform(1.5,1.9)))

        try:
            driver.find_element(By.XPATH,self.outoflikes_path)
            driver.close()
        except:
            pass
        body = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
        time.sleep(1)
        body.click()
        body.send_keys(Keys.UP)
        time.sleep(1)
        name = driver.find_element(By.XPATH, self.name_path).text
        # name = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, self.name_path))).text
        age = driver.find_element(By.XPATH, self.age_path).text


        try:
            city = driver.find_element(By.XPATH, self.city_path).text
        except:
            city = 'none'
        try:
            bio = driver.find_element(By.XPATH, self.bio_path).text.replace("\n", " ")

        except:
            bio = 'none'
        try:
            interests_list=[]
            interests = driver.find_elements(By.XPATH, self.interests_path)
            for interest in interests:
                interests_list.append(interest.text)
        except:
            interests_list="none"

        try:
            descriptors_list=[]
            descriptors = driver.find_elements(By.XPATH, self.descriptors_path)
            for descriptor in descriptors:
                descriptors_list.append(descriptor.text)
        except:
            descriptors_list="none"

        try:
            gender = driver.find_element(By.XPATH, self.gender_path).text
        except:
            gender = "not public"
        self.data_handler(name,age,city,bio,interests_list,descriptors_list,gender)



    def pause(self,scraped_users):
        if scraped_users > random.randint(20, 50):
            time.sleep(random.uniform(random.uniform(10, 20), random.uniform(30, 40)))
            scraped_users=0
        return scraped_users;

    def data_handler(self,name,age,city,bio,interests_list,descriptors_list,gender):

        possible_gender="tbd"
        bio = bio.lower()
        first_word_matches = ["insta:", "insta", "instagram:", "ig:", "instagram", "ig", "follow:", "follow"]
        containing_matches = ["@", "_", "."]
        possible_username = []

        for match in first_word_matches:
            if match in bio.split(" ") and bio.split(" ")[bio.split(" ").index(match) + 1] not in possible_username:
                possible_username.append(bio.split(" ")[bio.split(" ").index(match) + 1])
        for match in containing_matches:
            for element in bio.split(" "):
                if element.find(match) != -1 and element[-1] != "." and element not in possible_username:
                    possible_username.append(element)
        final_username = "none"
        for username in possible_username:
            if self.check_ig_username(username) is True:
                final_username = username



        with open("results.txt","a", encoding='utf-8') as f:
            f.write(str(name))
            f.write(';')
            f.write(str(age))
            f.write(';')
            f.write(str(city))
            f.write(';')
            f.write(str(bio))
            f.write(';')
            f.write(str(final_username))
            f.write(';')
            f.write(str(interests_list))
            f.write(';')
            f.write(str(descriptors_list))
            f.write(';')
            f.write(str(gender))
            f.write(';')
            f.write('\n')

    def check_ig_username(self,username):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'https://instausername.com',
            'Referer': 'https://instausername.com/availability',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        data = {
            'q': username,
        }

        response = requests.post('https://instausername.com/availability', headers=headers, data=data)

        if response.text.find("taken") == -1:
            response = False
        else:
            response = True
        return response;


bot=TinderBot()
bot.login(driver)
scraped_users=0
while True:
    scraped_users+=1
    try:
        bot.get_data(driver)
        bot.action(driver)
    except:
        bot.start(driver)
        bot.get_data(driver)
        bot.action(driver)
    scraped_users=bot.pause(scraped_users)