import logging
import os
import re
import shutil
from datetime import datetime
from typing import Any, Dict, Generator, Optional, cast

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.main import Session
from _pytest.python import Function
from _pytest.reports import TestReport
from _pytest.runner import CallInfo, TResult
from pluggy._result import _Result
from selenium.webdriver.chrome.webdriver import WebDriver

logging.basicConfig(level=logging.INFO)

TEMP_SCREENSHOTS_DIR_NAME = 'execution is progress...'
HISTORY_DIR_NAME = 'history'
DEFAULT_TEST_SUITE_NAME = 'UnknownTestSuite'


def pytest_addoption(parser: Parser) -> None:
    parser.addoption('--save_screenshots',
                     action='store_true',
                     default=False,
                     help='Whenever a test fails, a screenshot will immediately be taken.')
    parser.addoption('--screenshots_dir',
                     action='store',
                     default='screenshots',
                     help='''The directory where the screenshots will be saved, from project root directory.
                     By default, they are saved in the "screenshots" directory.''')


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """
    To avoid CI failure, forces pytest to finish its process with return code 0 when it was supposed to return 1
    See more: https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
    """
    project_root_path = str(session.config.rootpath)
    screenshots_dir = session.config.getvalue('screenshots_dir')
    screenshot_dir_path = os.path.join(project_root_path, screenshots_dir)
    temp_dir_path = os.path.join(screenshot_dir_path, TEMP_SCREENSHOTS_DIR_NAME)
    last_run_dir_path = os.path.join(screenshot_dir_path, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    if os.path.exists(temp_dir_path):
        shutil.move(temp_dir_path, last_run_dir_path)


def pytest_configure(config: Config) -> None:
    if not config.getvalue('save_screenshots'):
        logging.info('Skipping screenshot: Feature is disabled by default.')
        return

    project_root_path = str(config.rootpath)
    screenshots_dir = config.getvalue('screenshots_dir')
    screenshots_root_path = os.path.join(project_root_path, screenshots_dir)

    if not os.path.exists(screenshots_root_path):
        return os.makedirs(screenshots_root_path)

    for directory in os.scandir(screenshots_root_path):
        if match_dir_date_time_format(directory.name):
            archive_old_screenshots(screenshots_root_path, directory.name)
        elif directory.name != HISTORY_DIR_NAME:
            shutil.rmtree(directory.path)


def find_web_driver_instance(test_function_arguments: Dict[str, Any]) -> Optional[WebDriver]:
    for value in test_function_arguments.values():
        if hasattr(value, 'save_screenshot'):
            return cast(WebDriver, value)
    return None


@pytest.hookimpl(hookwrapper=True)  # type: ignore
def pytest_runtest_makereport(item: Function, call: CallInfo[TResult]) -> Generator[None, None, None]:
    results_hook: _Result
    results_hook = yield
    test_result: TestReport = results_hook.get_result()
    after_test_case_routine(test_result, pytest_function=item)


def after_test_case_routine(test_result: TestReport, pytest_function: Function) -> None:
    save_screenshots = pytest_function.config.getvalue('save_screenshots')
    test_finished_phase = test_result.when == 'call'
    test_failed = test_result.failed

    if not all([save_screenshots, test_finished_phase, test_failed]):
        return

    web_driver = find_web_driver_instance(test_function_arguments=pytest_function.funcargs)
    if not web_driver:
        logging.warning('''No Selenium Web Driver instance found in any function arguments of the test context!
            Screenshots won't be taken.''')
        return

    project_root_path = str(pytest_function.config.rootpath)
    screenshots_dir = pytest_function.config.getvalue('screenshots_dir')
    session_dir_path = os.path.join(project_root_path, screenshots_dir, TEMP_SCREENSHOTS_DIR_NAME)
    test_suite_name = pytest_function.parent.name if pytest_function.parent else DEFAULT_TEST_SUITE_NAME
    capture_screenshot(web_driver, session_dir_path, test_suite=test_suite_name, test_name=pytest_function.name)


def capture_screenshot(web_driver: WebDriver, session_dir_path: str, test_suite: str, test_name: str) -> None:
    test_suite_dir_path = os.path.join(session_dir_path, test_suite)
    if not os.path.exists(test_suite_dir_path):
        os.makedirs(test_suite_dir_path)

    img_path = os.path.join(test_suite_dir_path, f'{test_name}.png')
    if os.path.exists(img_path):
        logging.warning(f'Screenshot on path "{img_path}" already exists and will be overwritten by the latest test.')

    try:
        web_driver.save_screenshot(img_path)
    except Exception as e:
        logging.error(f'Error while trying to take screen for failed {test_name=}. {e}')


def archive_old_screenshots(screenshots_root_path: str, screenshot_dir_name: str) -> None:
    dir_path_in_history = os.path.join(screenshots_root_path, HISTORY_DIR_NAME, screenshot_dir_name)
    if os.path.exists(dir_path_in_history):
        logging.warning(f'''The screenshots folder from the last execution, {dir_path_in_history}, is already archived  
        in folder in the history folder. The older screenshots will be overwritten by the newer ones.''')
        shutil.rmtree(dir_path_in_history)

    history_root_path = os.path.dirname(dir_path_in_history)
    screenshot_dir_path = os.path.join(screenshots_root_path, screenshot_dir_name)
    shutil.move(screenshot_dir_path, history_root_path)


def match_dir_date_time_format(dir_name: str) -> bool:
    date_time_regex = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$'
    return bool(re.search(date_time_regex, dir_name))
