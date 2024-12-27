
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient
import datetime
import uuid
import requests

# ProxyMesh Configuration
PROXY_URL = "add your proxy mesh url here¸"

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/trends")
db = client.twitter_trends
collection = db.trends

# Selenium Options
options = Options()
options.add_argument(f'--proxy-server={PROXY_URL}')

def fetch_trends():
    driver = webdriver.Chrome(options=options)
    driver.get("https://x.com/login")

    # Login to Twitter
    username = driver.find_element(By.NAME, "text")
    username.send_keys("your_twitter_username")
    username.send_keys(Keys.RETURN)
    time.sleep(2)

    password = driver.find_element(By.NAME, "password")
    password.send_keys("your_twitter_password")
    password.send_keys(Keys.RETURN)
    time.sleep(5)

    # Fetch Trending Topics
    trends = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")[:5]
    trend_names = [trend.text for trend in trends]

    # Get Proxy IP
    ip_response = requests.get("http://ipinfo.io/json")
    ip_address = ip_response.json()["ip"]

    # Store Results in MongoDB
    unique_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now()
    record = {
        "_id": unique_id,
        "trend1": trend_names[0],
        "trend2": trend_names[1],
        "trend3": trend_names[2],
        "trend4": trend_names[3],
        "trend5": trend_names[4],
        "datetime": timestamp,
        "ip_address": ip_address,
    }
    collection.insert_one(record)

    driver.quit()
    return record
