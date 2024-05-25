from selenium import webdriver
import sys


# Takes which browser would like to launch as one mandatory param
# and stores driver object in driver variable. Need to call get_driver_instance()
# to get driver object. Takes options (options to set at browser level) as an optional param.
class DriverFactory:

    def __init__(self, browser: str, options=None):
        if options is None:
            options = []
        if browser == 'firefox' or browser == 'mozilla firefox':
            firefox_options = webdriver.FirefoxOptions()
            for option in options:
                firefox_options.add_argument(option)
            self.driver = webdriver.Firefox(firefox_options)
        elif browser == 'edge' or browser == 'microsoft edge' or browser == 'msedge':
            edge_options = webdriver.EdgeOptions()
            for option in options:
                edge_options.add_argument(option)
            self.driver = webdriver.Edge(edge_options)
        elif browser == 'safari' and sys.platform == 'darwin':
            safari_options = webdriver.SafariOptions()
            for option in options:
                safari_options.add_argument(option)
            self.driver = webdriver.Safari(safari_options)
        elif browser == 'safari' and sys.platform != 'darwin':
            print("""***Request to run on safari, but the sys platform is not type of darwin. 
            Launching chrome by default***""")
            chrome_options = webdriver.ChromeOptions()
            for option in options:
                chrome_options.add_argument(option)
            self.driver = webdriver.Chrome(chrome_options)
        else:
            chrome_options = webdriver.ChromeOptions()
            for option in options:
                chrome_options.add_argument(option)
            self.driver = webdriver.Chrome(chrome_options)
        self.driver.maximize_window()

    def get_driver_instance(self):
        return self.driver
