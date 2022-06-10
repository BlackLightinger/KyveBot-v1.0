from selenium.webdriver.common.by import By
from time import sleep


def popup_windows(driver, main_page):
    for handle in driver.window_handles:
        if handle != main_page:
            approve_page = handle
    return approve_page


def tac(driver):

    main_page = driver.current_window_handle

    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Share on twitter')]").click()
    driver.switch_to.window(popup_windows(driver, main_page))

    sleep(15)


    driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Tweet')]").click()

    sleep(10)

    driver.find_element(by=By.XPATH, value="//*[name()='div' and @style='transform:"
                                           " translateY(0px); position: absolute; width: 100%; "
                                           "transition: opacity 0.3s ease-out 0s;']"
                        ).click()
    sleep(1)

    s = driver.current_url

    driver.close()
    driver.switch_to.window(main_page)
    return s