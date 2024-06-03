from behave import *
from pages.first_page import FirstPage
from utils.selenium.selenium_helper import SeleniumHelper


@given('I am on login page')
def land_on_login_page(context):
    SeleniumHelper.click_on_element(context.driver, FirstPage.SIGN_IN)
    SeleniumHelper.enter_text_in_lower_case(context.driver, FirstPage.EMAIL_OR_PHONE, "HELLO")
    SeleniumHelper.do_right_click_on_element(context.driver, FirstPage.BUTTON_TEXT)
    print(context.text, "\n")
    assert True


@when('I logged in application as admin')
def login(context):
    print(context.text, "\n")
    assert True


@when('I map a table here')
def table(context):
    for row in context.table:
        print(row['name'], ' ', row['desc'], '\n')
