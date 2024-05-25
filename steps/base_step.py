from behave import *


@given('I am on login page')
def land_on_login_page(context):
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
