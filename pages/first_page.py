from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By


class FirstPage:

    sign_in = {
        "type": By.XPATH,
        "value": "//span[text()='Sign in']"
    }

    email_or_phone = {
        "type": By.ID,
        "value": "identifierId"
    }

    button_next = {
        'type': By.XPATH,
        'value': "//span[text()='Next']"
    }

    # def __init__(self, driver):
    #     self.driver = driver
    #     self.sign_in = self.driver.find_element(By.XPATH, "//span[text()='Sign in']")
    #     self.textbox = self.driver.find_element(By.CSS_SELECTOR, "#identifierId")



