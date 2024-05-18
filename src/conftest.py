import pytest
from selenium import webdriver


@pytest.fixture(scope="module")
def launch_driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.google.com")
    request.cls.driver = driver
    yield
    driver.quit()