import sys
from utils.selenium.driver_factory import DriverFactory

print('hello')

for arg in sys.argv:
    if 'browser=' in arg:
        browser = arg.replace("browser=", "")
    print('arg: ', arg)


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
        context.driver = DriverFactory(browser).get_driver_instance()
        context.driver.get("https://www.google.com")


def after_tag(context, tag):
    if 'ui' in tag and context.driver is not None:
        context.driver.quit()
    # This block runs for after every tag
