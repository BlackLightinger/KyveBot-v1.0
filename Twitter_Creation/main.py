from twitter_creation import twc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("start-maximized")
options.add_extension('proxy.zip')

while True:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    twc(driver)