from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep, time
from twitter_creation import twc
from tweet_and_copy import tac
from kepr_connect import keplr_connect
import json


def acp_api_send_request(driver, message_type, data={}):
    message = {
        # всегда указывается именно этот получатель API сообщения
        'receiver': 'antiCaptchaPlugin',
        # тип запроса, например setOptions
        'type': message_type,
        # мерджим с дополнительными данными
        **data
    }
    # выполняем JS код на странице
    # а именно отправляем сообщение стандартным методом window.postMessage
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))


def popup_windows(driver, main_page):
    for handle in driver.window_handles:
        if handle != main_page:
            approve_page = handle
    return approve_page


options = Options()
options.add_argument("start-maximized")
options.add_extension('extension_0_10_4_0.crx')
options.add_extension('anticaptcha-plugin_v0.62.crx')
options.add_extension('proxy.zip')

while True:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.google.ru/")
    sleep(1)

    acp_api_send_request(
        driver,
        'setOptions',
        {'options': {'antiCaptchaApiKey': ''}}
    )
    sleep(3)

    start = time()

    keplr_connect(driver)
    sleep(1)
    main_page = driver.current_window_handle

    twc(driver)

    driver.switch_to.window(main_page)

    tweet_url = tac(driver)

    sleep(1)
    driver.find_element(by=By.XPATH, value="//*[name()='input' and @class='q-field__native q-placeholder']").send_keys(tweet_url)
    sleep(1)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Claim your tokens')]").click()

    WebDriverWait(driver, 180).until(lambda x: x.find_element(by=By.CSS_SELECTOR, value=".antigate_solver.solved"))
    sleep(5)
    print(time() - start)
