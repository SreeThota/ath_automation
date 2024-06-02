from behave import *
from pages.first_page import FirstPage
from utils.selenium.selenium_helper import SeleniumHelper


@given('I am on login page')
def land_on_login_page(context):
    # locator_info = FirstPage.sign_in
    # print(locator_info)
    SeleniumHelper.click_on_element(context.driver, FirstPage.sign_in)
    # context.driver.find_element(locator_info['type'], locator_info['value']).click()
    SeleniumHelper.enter_text_in_lower_case(context.driver, FirstPage.email_or_phone, "HELLO")
    SeleniumHelper.do_right_click_on_element(context.driver, FirstPage.button_next)
    SeleniumHelper.pause_for(context.driver, 10)
    # print(SeleniumHelper.is_element_visible(page.sign_in))
    # print(SeleniumHelper.get_attribute_value(page.sign_in, "hello"))
    # print(SeleniumHelper.get_dom_attribute_value(page.sign_in, "hello"))
    # SeleniumHelper.click_on_element(page.sign_in)
    # print(page.sign_in.click())
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
