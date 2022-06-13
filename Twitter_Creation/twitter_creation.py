import random
import string
from selenium.webdriver.common.by import By
from time import sleep
from sms import get_sms, get_phone
from os import getcwd


def generate_random_name_or_password():
    length = 10
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def twc(driver):
    code = False
    main_page = driver.current_window_handle
    while not code:
        driver.execute_script('''window.open("https://twitter.com/signup", "tab2");''')
        driver.switch_to.window('tab2')
        sleep(4)

        pageSource = driver.page_source
        fileToWrite = open("page_source.html", "w")
        fileToWrite.write(pageSource)
        fileToWrite.close()

        driver.find_elements(by=By.XPATH,value="//*[name()='a' and @data-testid='signup']//*[name()='span']")[1].click()
        name = generate_random_name_or_password()
        driver.find_element(by=By.NAME, value="name").send_keys(name)

        phone, activation = get_phone()

        driver.find_element(by=By.NAME, value="phone_number").send_keys(phone)
        driver.find_element(by=By.XPATH, value=f"//*[@value='{random.randint(1, 12)}']").click()
        driver.find_element(by=By.XPATH, value=f"//*[@aria-labelledby='SELECTOR_2_LABEL']//*[@value='{random.randint(1, 28)}']").click()
        driver.find_element(by=By.XPATH, value=f"//*[@value='{random.randint(1975, 2003)}']").click()
        sleep(2)
        driver.find_elements(by=By.XPATH, value="//*[@role='button']")[2].click()
        driver.find_elements(by=By.XPATH, value="//*[@role='button']")[1].click()
        driver.find_element(by=By.XPATH, value="//*[@role='button' and @data-testid='ocfSignupReviewNextLink']").click()
        sleep(1)
        driver.find_elements(by=By.XPATH, value="//*[@role='button']")[4].click()
        sleep(1)
        code = get_sms(activation)
        if not code:
            driver.close()
            driver.switch_to.window(main_page)

    driver.find_element(by=By.NAME, value="verfication_code").send_keys(code)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[2].click()
    sleep(2)
    password = generate_random_name_or_password()
    driver.find_element(by=By.XPATH, value="//*[name()='input' and @type='password']").send_keys(password)
    sleep(2)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[1].click()
    sleep(5)
    driver.find_element(by=By.XPATH, value="//*[name()='input']").send_keys(getcwd() + f"/pics/{random.randint(1, 20)}.jpg")
    sleep(3)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[4].click()
    sleep(1)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[2].click()
    sleep(1)
    # после загрузки картинки и нажатия далее
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[0].click()
    sleep(1)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[-1].click()
    sleep(1)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[1].click()
    sleep(1)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[1].click()
    sleep(1)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[-1].click()
    sleep(10)
    driver.find_elements(by=By.XPATH, value="//*[@dir='auto']")[8].click()
    sleep(1)
    driver.find_elements(by=By.XPATH, value="//*[@role='button']")[-1].click()
    sleep(1)
    
    with open("twitters.txt", "a") as file:
        file.write(f"{phone}:{password}:@{name}")
        file.write("\n")
    driver.close()