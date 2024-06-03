from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By


class FirstPage:

    SIGN_IN = (By.XPATH, "//span[text()='Sign in']")
    EMAIL_OR_PHONE = (By.ID, "identifierId")
    BUTTON_TEXT = (By.XPATH, "//span[text()='Next']")



