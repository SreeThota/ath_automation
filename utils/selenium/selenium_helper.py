from selenium import webdriver


# Class supports:
#     1. All Driver level methods
#     2. All Element level methods
#     3. All Wait methods
#     4. All Actions related methods
#     5. All Select related methods
#     6. All keyboard actions

class SeleniumHelper:

    @staticmethod
    def is_visible(driver, locator: str):
        # webdriver.Chrome().
        print()
