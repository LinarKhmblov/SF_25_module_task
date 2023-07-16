import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(autouse=True)
def driver():
    """Открытие сайта для тестирования"""

    test_site = 'https://petfriends.skillfactory.ru/login'
    driver = webdriver.Chrome()

    # Увеличиваем окно браузера
    driver.maximize_window()

    # Переходим на страницу авторизации
    driver.get(test_site)

    yield driver

    driver.quit()


