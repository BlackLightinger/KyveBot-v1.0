from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyautogui
from time import sleep
import json


def popup_windows(driver, main_page):
    for handle in driver.window_handles:
        if handle != main_page:
            approve_page = handle
    return approve_page


def keplr_import(driver, mnemonic):
    driver.get("chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/popup.html#/register")
    sleep(1)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Import existing account')]").click()
    driver.find_element(by=By.NAME, value='words').send_keys(mnemonic)
    driver.find_element(by=By.NAME, value='name').send_keys('hueta')
    try:
        driver.find_element(by=By.NAME, value='password').send_keys('redahbdrsztg')
        driver.find_element(by=By.NAME, value='confirmPassword').send_keys('redahbdrsztg')
        driver.find_element(by=By.NAME, value='confirmPassword').submit()
    except:
        driver.find_element(by=By.NAME, value='name').submit()


def keplr_connect(driver):
    driver.get("https://app.kyve.network/#/faucet")
    sleep(3)
    driver.find_element(by=By.XPATH, value="//*[name()='svg' and @class='q-checkbox__svg fit absolute-full']").click()
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Save selection')]").click()
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Connect wallet')]").click()

    sleep(1)
    main_page = driver.current_window_handle
    driver.switch_to.window(popup_windows(driver, main_page))
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Approve')]").click()
    driver.switch_to.window(main_page)
    sleep(1)
    driver.switch_to.window(popup_windows(driver, main_page))
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Approve')]").click()
    driver.switch_to.window(main_page)


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


def enter_proxy_auth(proxy_username, proxy_password):
    pyautogui.typewrite(proxy_username)
    pyautogui.press('tab')
    pyautogui.typewrite(proxy_password)
    pyautogui.press('enter')

options = Options()
options.add_argument("start-maximized")
options.add_extension('extension_0_10_4_0.crx')
options.add_extension('anticaptcha-plugin_v0.62.crx')
options.add_extension('proxy.zip')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.google.ru/")
sleep(1)

acp_api_send_request(
    driver,
    'setOptions',
    {'options': {'antiCaptchaApiKey': ''}}
)
sleep(3)

main_page = driver.current_window_handle

# кошелек на который надо сливать
wallet = "kyve157kywn8mme8glgyc53wtn5m7s9zmqa4ts5axxe"

with open("mnemonics.txt", "r") as file:
    for mnemonic in file:
        if mnemonic.strip() == "":
            continue
        print(mnemonic.strip())
        driver.execute_script('''window.open("https://www.google.ru/", "tab2");''')
        driver.switch_to.window('tab2')
        keplr_import(driver, mnemonic.strip())
        sleep(3)
        try:
            keplr_connect(driver)
        except:
            pass

        sleep(3)
        driver.get("chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/popup.html#/")
        driver.find_element(by=By.CLASS_NAME, value="title-icon-25e1WHW2QCVx0gKPqEq2KM").click()
        sleep(2)
        driver.find_element(by=By.CLASS_NAME, value="chain-list-container-2O1kmXQgj2e1mD5MUOrGU8").find_element(by=By.XPATH, value="//*[contains(text(), 'Korellia')]").click()
        sleep(5)
        try:
            driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Send')]").click()
            sleep(2)
            driver.find_element(by=By.CLASS_NAME, value="input-group").find_element(by=By.XPATH, value="//*[name()='input' and @class='form-control-alternative input-2hAJgmbJ5GujqDYmHt7IH5 form-control']").send_keys(wallet)
            driver.find_elements(by=By.CLASS_NAME, value="form-group")[2].find_element(by=By.XPATH, value="//*[contains(text(), 'Balance: ')]").click()
            sleep(1)
            driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Send')]").click()
            sleep(1)
            driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Approve')]").click()
        except:
            pass
        sleep(5)
        driver.find_element(by=By.CLASS_NAME, value="header-menu-right").find_element(by=By.XPATH, value="//*[name()='i' and @class='fas fa-user']").click()
        sleep(1)
        driver.find_element(by=By.XPATH, value="//*[name()='i' and @class='fas fa-ellipsis-h']").click()
        sleep(1)
        driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Delete Account')]").click()
        sleep(1)
        driver.find_element(by=By.NAME, value="password").send_keys('redahbdrsztg')
        driver.find_element(by=By.NAME, value="password").submit()
        driver.close()
        driver.switch_to.window(main_page)
        sleep(3)
sleep(100)
