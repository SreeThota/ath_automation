import sys
from utils.selenium.driver_factory import DriverFactory


browser = 'chrome'
headless = False

for arg in sys.argv:
    if 'browser=' in arg:
        browser = arg.replace("browser=", "")
    if 'headless' in arg:
        headless = True


def before_all(context):
    print('before all execution')


def after_all(context):
    print('after all execution')


def before_feature(context, feature):
    print('before every feature file')
    print(feature.tags)


def after_feature(context, feature):
    print('after every feature file')


def before_scenario(context, scenario):
    print('before every scenario')
    print(scenario.tags)


def after_scenario(context, scenario):
    print('after every scenario')


def before_step(context, step):
    print('before every step')


def after_step(context, step):
    print()


def before_tag(context, tag):
    # This block runs before every tag.
    if 'ui' in tag:
        options = ['--disable-extensions']
        if headless:
            options.append('--headless')
        # options.append('--window-size=1920,1080');   Enable this only if we need to run tests in that resolution
        context.driver = DriverFactory(browser, options).get_driver_instance()
        context.driver.get("https://www.google.com")


def after_tag(context, tag):
    if 'ui' in tag and context.driver is not None:
        context.driver.quit()
    # This block runs after every tag
