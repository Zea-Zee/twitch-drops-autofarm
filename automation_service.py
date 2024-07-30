import time
import random
from datetime import datetime, date
import os
import database
import email_service

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyautogui
from selenium_stealth import stealth
from fake_useragent import UserAgent


STREAM_URL = "https://www.twitch.tv/tysead"

def human_type(element, text: str) -> None:
    element.click()
    time.sleep(random.uniform(0.1, 2))
    for char in text:
        # pyautogui.typewrite(char)
        element.send_keys(char)
        time.sleep(random.uniform(0.075, 0.5))


def get_random_user_agent():
    user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
    return user_agent.random


def create_webdriver(username: str):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    if username:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_directory = os.path.join(script_dir, 'users')
        user_directory = os.path.join(base_directory, username)
        options.add_argument(f'user-data-dir={user_directory}')
    # options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    service = Service(executable_path="C:/Users/kuzga/OneDrive/Рабочий стол/twitch-drops-autofarm/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    user_agent = get_random_user_agent()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.73 Safari/537.36"
    stealth(driver=driver,
            user_agent=user_agent,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True
    )

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return driver


def register(username: str, password: str, birthday: str, email: str):
    driver = create_webdriver(username)
    # time.sleep(200)
    driver.get("https://www.twitch.tv")
    wait = WebDriverWait(driver, 10)

    # cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="consent-banner-accept"]')))
    # cookie_button.click()
    # time.sleep(1)
    # cookie_button.click()
    # print("cookie")

    signup_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="signup-button"]')))
    signup_button.click()
    print("signup")
    # time.sleep(3)

    usename_field = wait.until(EC.element_to_be_clickable((By.ID, 'signup-username')))
    password_field = wait.until(EC.element_to_be_clickable((By.ID, 'password-input')))
    print("fields")
    human_type(usename_field, username)
    time.sleep(1)
    human_type(password_field, password)
    time.sleep(1)


    year, month, day = birthday.split('-')
    day, month = day.replace('0', '', 1), month.replace('0', '', 1)
    day_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Укажите день вашего рождения']")))
    human_type(day_field, day)

    month_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Укажите месяц своего рождения']")))
    select_month = Select(month_field)
    select_month.select_by_value(month)

    year_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Укажите год вашего рождения']")))
    human_type(year_field, year)


    email_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-a-target='signup-phone-email-toggle']")))
    email_button.click()
    email_field = wait.until(EC.element_to_be_clickable((By.ID, 'email-input')))
    human_type(email_field, email)
    # # driver.find_elements_by_css_selector("[aria-label='']")

    user_data_submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-a-target='passport-signup-button']")))
    user_data_submit_button.click()
    database.update_user_status(username, 2)

    confirmation_code = email_service.get_confirmation_code(email)
    input_code_fields = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-a-target='verification-code-input-component-input'] input")))
    for i, digit in enumerate(confirmation_code):
        human_type(input_code_fields[i], str(digit))
    confirmation_submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-a-target='verification-code-modal-component-primary-button']")))
    confirmation_submit_button.click()

    database.update_user_status(username, 3)
    driver.quit()


def authenticate_user(username, password):
    user = database.get_user(username)
    if user and user[2] == password and user[3]:
        return True
    return False


def watch_stream(username: str, url: str) -> None:
    driver = create_webdriver(username)
    driver.get(STREAM_URL)
    wait = WebDriverWait(driver, 10)

    try:
        submit_18_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-a-target='content-classification-gate-overlay-start-watching-button']")))
        submit_18_button.click()
    except Exception as e:
        print(f"watch_strean func, 146 row {e}")

    database.update_user_status(username, 4)
    time.sleep(45000)
    database.update_user_status(username, 5)
    driver.quit()
