from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_HLISA():
    options = Options()
    # Укажите путь к бинарному файлу Firefox, если он нестандартный
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

    # Укажите путь к geckodriver
    service = FirefoxService(executable_path=r"C:\Users\kuzga\Downloads\geckodriver-v0.34.0-win32\geckodriver.exe")

    # Создание драйвера Firefox
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Открытие страницы DuckDuckGo
        driver.get("https://duckduckgo.com/")

        # Поиск поля ввода и ввод текста
        search_box = driver.find_element(By.CSS_SELECTOR, 'input[aria-autocomplete="both"]')
        search_box.click()
        search_box.send_keys("котики")

        # Ожидание появления результатов поиска
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results--main')))

        print("Тест успешно выполнен!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрываем браузер
        driver.quit()

if __name__ == "__main__":
    test_HLISA()
