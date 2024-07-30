import time
import os
import database
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from fake_useragent import UserAgent


def get_random_user_agent():
    user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
    return user_agent.random


def create_webdriver():
    options = Options()
    # options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_directory = os.path.join(script_dir, 'users')
    user_directory = os.path.join(base_directory, user_id)

    options.add_argument(f'user-data-dir={user_directory}')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    user_agent = get_random_user_agent()
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


def register(user):
    username, password, birthdate, phone_number, country, proxy = user[1:8]

    chrome_options = Options()
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument(f'--proxy-server={proxy}')

    webdriver_service = Service("path/to/chromedriver")
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    driver.get("https://www.twitch.tv")

    driver.find_element(By.ID, 'signup-username')
    driver.find_element(By.ID, 'password-input')

    #select
    driver.find_elements_by_css_selector("[aria-label='Select your birthday month']")
    #type
    driver.find_elements_by_css_selector("[aria-label='Enter the day of your birth']")
    driver.find_elements_by_css_selector("[aria-label='Enter the year of your birth']")

    #switch to email
    driver.find_elements_by_css_selector("[data-a-target='signup-phone-email-toggle']")
    # driver.find_elements_by_css_selector("[aria-label='']")

    driver.find_element(By.ID, 'email-input')
    driver.find_elements_by_css_selector("[data-a-target='passport-signup-button']")

    database.update_user_status(username)

    driver.quit()

def authenticate_user(username, password):
    user = database.get_user(username)
    if user and user[2] == password and user[3]:
        return True
    return False
