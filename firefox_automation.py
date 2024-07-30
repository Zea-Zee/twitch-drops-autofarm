import time
import random
from datetime import datetime, date
import os
import database
import email_service

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from fake_useragent import UserAgent

import pyautogui

STREAM_URL = "https://www.twitch.tv/tysead"


def human_type(element, text: str) -> None:
    element.click()
    time.sleep(random.uniform(0.1, 2))
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.075, 0.5))


def get_random_user_agent():
    user_agent = UserAgent(browsers='firefox', os='windows', platforms='pc')
    return user_agent.random


def create_webdriver(username: str):
    options = Options()
    options.add_argument("-private")  # Запуск в режиме инкогнито
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    options.set_preference("general.useragent.override",
                           get_random_user_agent())

    if username:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_directory = os.path.join(script_dir, 'users')
        user_directory = os.path.join(base_directory, username)
        options.set_preference("profile", user_directory)

    service = Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

    return driver


def register(username: str, password: str, birthday: str, email: str):
    driver = create_webdriver(username)
    driver.get("https://www.twitch.tv")
    wait = WebDriverWait(driver, 10)

    signup_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '[data-a-target="signup-button"]')))
    signup_button.click()
    print("signup")

    username_field = wait.until(
        EC.element_to_be_clickable((By.ID, 'signup-username')))
    password_field = wait.until(
        EC.element_to_be_clickable((By.ID, 'password-input')))
    print("fields")
    human_type(username_field, username)
    time.sleep(1)
    human_type(password_field, password)
    time.sleep(1)

    year, month, day = birthday.split('-')
    day, month = day.replace('0', '', 1), month.replace('0', '', 1)
    day_field = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[aria-label='Укажите день вашего рождения']")))
    human_type(day_field, day)

    month_field = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[aria-label='Укажите месяц своего рождения']")))
    select_month = Select(month_field)
    select_month.select_by_value(month)

    year_field = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[aria-label='Укажите год вашего рождения']")))
    human_type(year_field, year)

    email_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-a-target='signup-phone-email-toggle']")))
    email_button.click()
    email_field = wait.until(
        EC.element_to_be_clickable((By.ID, 'email-input')))
    human_type(email_field, email)

    user_data_submit_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-a-target='passport-signup-button']")))
    user_data_submit_button.click()
    database.update_user_status(username, 2)

    confirmation_code = email_service.get_confirmation_code(email)
    input_code_fields = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "[data-a-target='verification-code-input-component-input'] input")))
    for i, digit in enumerate(confirmation_code):
        human_type(input_code_fields[i], str(digit))
    confirmation_submit_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-a-target='verification-code-modal-component-primary-button']")))
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
        submit_18_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-a-target='content-classification-gate-overlay-start-watching-button']")))
        submit_18_button.click()
    except Exception as e:
        print(f"watch_strean func, 146 row {e}")

    database.update_user_status(username, 4)
    time.sleep(45000)
    database.update_user_status(username, 5)
    driver.quit()
