import random
import string
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from time import sleep
from sms import get_sms, get_phone


def generate_random_name_or_password():
    length = 10
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def random_month():
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    return random.choice(months)


def twc(driver):
    driver.execute_script('''window.open("https://twitter.com/signup", "tab2");''')
    driver.switch_to.window('tab2')
    sleep(2)
    driver.find_element(by=By.XPATH,
                        value="//*[contains(text(), 'Зарегистрируйтесь с помощью номера телефона или адреса электронной почты')]").click()
    name = generate_random_name_or_password()
    driver.find_element(by=By.NAME, value="name").send_keys(name)

    phone, activation = get_phone()

    driver.find_element(by=By.NAME, value="phone_number").send_keys(phone)
    Select(driver.find_element(by=By.ID, value="SELECTOR_1")).select_by_visible_text(random_month())
    Select(driver.find_element(by=By.ID, value="SELECTOR_2")).select_by_visible_text(str(random.randint(1, 28)))
    Select(driver.find_element(by=By.ID, value="SELECTOR_3")).select_by_visible_text(str(random.randint(1975, 2003)))
    sleep(2)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Далее')]").click()
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Далее')]").click()
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Зарегистрироваться')]").click()
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'ОК')]").click()
    sleep(1)
    driver.find_element(by=By.NAME, value="verfication_code").send_keys(get_sms(activation))
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Далее')]").click()
    sleep(2)
    password = generate_random_name_or_password()
    driver.find_element(by=By.XPATH, value="//*[name()='input' and @type='password']").send_keys(password)
    sleep(2)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Далее')]").click()
    sleep(5)
    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Пропустить')]").click()

    with open("twitters.txt", "a") as file:
        file.write(f"{phone}:{password}:@{name}")
        file.write("\n")

    driver.close()