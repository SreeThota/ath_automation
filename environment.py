print('hello')


def before_all(context):
    print('before all execution')


def after_all(context):
    print('after all execution')


def before_feature(context, feature):
    print('before every feature file')


def after_feature(context, feature):
    print('after every feature file')


def before_scenario(context, scenario):
    print('before every scenario')


def after_scenario(context, scenario):
    print('after every scenario')


def before_step(context, step):
    print('before every step')


def after_step(context, step):
    print('after every step')


def before_tag(context, tag):
    print('before every tag -- must be controlled by using if condition like when tag matches')


def after_tag(context, tag):
    print('after every tag -- must be controlled by using if condition like when tag matches')