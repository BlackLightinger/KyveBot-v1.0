from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from time import sleep

def popup_windows(driver, main_page):
    for handle in driver.window_handles:
        if handle != main_page:
            approve_page = handle
    return approve_page


def decoding_mnemonic(mnemonic, driver):
    mnemonic = mnemonic.split(' ')
    for i in range(len(mnemonic)):
        driver.find_element(by=By.XPATH, value="//button[contains(text(), '"+mnemonic[i]+"')]").click()

def keplr_connect(driver):
    driver.get("chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/popup.html#/register")
    sleep(1)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Import existing account')]").click()
    driver.find_element(by=By.NAME, value='words').send_keys(
        'below shove outside direct poet cancel kit upgrade omit dwarf room portion')
    driver.find_element(by=By.NAME, value='name').send_keys('hueta')
    driver.find_element(by=By.NAME, value='password').send_keys('redahbdrsztg')
    driver.find_element(by=By.NAME, value='confirmPassword').send_keys('redahbdrsztg')
    driver.find_element(by=By.NAME, value='confirmPassword').submit()

    driver.get("chrome-extension://dmkamcknogkgcdfhhbddcghachkejeap/popup.html#/register")
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Create new account')]").click()
    mnemonic = driver.find_element(by=By.CLASS_NAME, value='new-mnemonic-3oR7GptCgeG2ZjPpA1EN1F').text
    driver.find_element(by=By.NAME, value='name').send_keys('123')
    driver.find_element(by=By.NAME, value='password').send_keys('srthbsrthb')
    driver.find_element(by=By.NAME, value='confirmPassword').send_keys('srthbsrthb')
    driver.find_element(by=By.NAME, value='confirmPassword').submit()
    decoding_mnemonic(mnemonic, driver)

    with open("mnemonics.txt", "a") as file:
        file.write(mnemonic)
        file.write("\n")

    try:
        alert = Alert(driver)
        alert.dismiss()
    except:
        print("no alert")

    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Register')]").click()

    sleep(3)
    driver.get("https://app.kyve.network/#/faucet")
    sleep(3)
    driver.find_element(by=By.XPATH, value="//*[name()='svg' and @class='q-checkbox__svg fit absolute-full']").click()
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Save selection')]").click()
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Connect wallet')]").click()

    sleep(2)
    main_page = driver.current_window_handle
    driver.switch_to.window(popup_windows(driver, main_page))
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Approve')]").click()
    driver.switch_to.window(main_page)
    sleep(2)
    driver.switch_to.window(popup_windows(driver, main_page))
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Approve')]").click()
    driver.switch_to.window(main_page)