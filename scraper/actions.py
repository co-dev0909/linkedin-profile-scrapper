import getpass
import os
import pickle
import random
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from .constants import VERIFY_LOGIN_ID, COOKIE_FILE_NAME

BASE_URL = "https://www.linkedin.com/"


def __prompt_email_password():
    u = input("Email: ")
    p = getpass.getpass(prompt="Password: ")
    return u, p


def page_has_loaded(driver):
    page_state = driver.execute_script("return document.readyState;")
    return page_state == "complete"


def load_cookies(driver, path=""):
    driver.get(BASE_URL)
    if os.path.isfile(path or COOKIE_FILE_NAME):
        with open(path or COOKIE_FILE_NAME, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.get(f"{BASE_URL}feed/")
            sleep(2)


def action_click(driver, element):
    action = ActionChains(driver)
    action.click(element)
    action.perform()


def save_cookies(driver, file_name=""):
    if not os.path.exists("creds"):
        os.mkdir("creds")
    pickle.dump(
        driver.get_cookies(), open(f"creds/{file_name or COOKIE_FILE_NAME}.pkl", "wb")
    )


def linkedin_login(driver, email="", password="", timeout=10):
    driver.get(f"{BASE_URL}login")
    # if not email:
    #     email = input("Enter Email: ")
    # if not password:
    #     password = getpass.getpass(prompt="Enter Password: ")
    # try:
    #     email_elem = driver.find_element(By.ID, "username")
    #     email_elem.send_keys(email)
    # except NoSuchElementException:
    #     pass
    # except Exception as e:
    #     pass
    # password_elem = driver.find_element(By.ID, "password")
    # password_elem.send_keys(password)
    # password_elem.submit()
    # if driver.current_url == f'{BASE_URL}checkpoint/lg/login-submit':
    #     remember = driver.find_elements(By.ID, REMEMBER_PROMPT)
    #     if remember:
    #         remember[0].submit()
    # if "add-phone" in driver.current_url:
    #     skip = driver.find_elements(By.XPATH, '//button[@class="secondary-action"]')
    #     if skip:
    #         action_click(driver=driver, element=skip[0])\
    input("Please login manually and then hit enter here")
    counters = 0
    while counters < timeout:
        counters = counters + 1
        sleep(1)
        element = driver.find_elements(By.CLASS_NAME, VERIFY_LOGIN_ID)
        if len(element) == 0:
            pass
        else:
            break
    element = driver.find_elements(By.CLASS_NAME, VERIFY_LOGIN_ID)
    if element:
        save_cookies(driver, email)
        return True
    return False


def login(driver, timeout=10):
    paths = list(os.listdir("creds")) if os.path.exists("creds") else None
    if paths:
        path = "creds/" + random.choice(paths)
        load_cookies(driver=driver, path=path)
        counter = 0
        driver.get(f"{BASE_URL}feed/")
        while driver.current_url == f"{BASE_URL}feed/" and counter < 5:
            element = driver.find_elements(By.CLASS_NAME, VERIFY_LOGIN_ID)
            if len(element) > 0:
                return
            counter = counter + 1
            sleep(3)
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        return login(driver=driver, timeout=timeout)
    else:
        print("Please login")
    exit()
