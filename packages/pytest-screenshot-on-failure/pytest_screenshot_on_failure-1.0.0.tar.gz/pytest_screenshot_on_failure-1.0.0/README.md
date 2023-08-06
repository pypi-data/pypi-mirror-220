# Pytest Screenshot on Failure
Saves a screenshot when a test case from a pytest execution fails.

## Requirements
This plugin requires that you have an instance of your selenium `WebDriver` being yielded by a `@pytext.fixture`, in 
your `conftest.py` file.

This is not just a good practice, but it also helps pytest-screenshot-on-failure to identify your WebDriver instance 
for the moment it needs to capture a screenshot.
```python
# conftest.py
from selenium import webdriver
from selenium.webdriver import Chrome

# WebDriver fixture example
@pytest.fixture(scope='session', autouse=True)
def web_driver():
    options = webdriver.ChromeOptions()
    driver = Chrome(options=options)
    
    yield driver
    
    driver.quit()
```

## How to use
You can enable this plugin by using the `--save_screenshots` flag when running your tests. 

Example:
```
python3 -m pytest /tests --save_screenshots
```

The screenshots will be saved by default into the "screenshots" folder. You can change this folder name by using the 
flag `--screenshots_dir=<custom_dir_name>`.

Example:
```
python3 -m pytest /tests --save_screenshots --screenshots_dir=images
```

## Screenshots folder structure
* The screenshots from the latest execution will be saved directly on the screenshots root folder, with the date/time 
of the execution.
* Give your test file a class name, and the screenshots will be organized by test suite.
* Whenever you star a new execution, older images will be stored in the history folder.

![img.png](images/folder_structure.png)

## Test coverage
The current test coverage rate is **97%**! It's only missing coverage on the `pytest_runtest_makereport` hook. 
I couldn't find a way of covering methods that yields a Generator, yet.
```commandline
---------- coverage: platform linux, python 3.10.6-final-0 -----------
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
src/__init__.py                           0      0   100%
src/pytest_screenshot_on_failure.py      91      3    97%   80-82
-------------------------------------------------------------------
TOTAL                                    91      3    97%
```

## Static Analysis & Lint
The repository has no offenses on autoflake, yapf, isort and strict mypy checks. Pending to add CI/CD actions to assert 
these checks automatically.