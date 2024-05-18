# ath_automation
Cumulative framework to handle multiple type of tools

##behave related

features: This directory supports to add your feature files (Ex: feature_name.feature). It can contain subdirectories too.
steps: This directory holds all the step implementation files for the behave steps defined in features directory.
environment.py -- A file which must be located (if created in project) in directory where steps directory is locating.

##pytest related

tests: A directory which holds tests written using pytest executor.

##Root directory- Dependencies

requirements.txt -- A file which includes all dependencies to support this project.
    We can use command pip3 install -r requirements.txt to install all the dependencies declared