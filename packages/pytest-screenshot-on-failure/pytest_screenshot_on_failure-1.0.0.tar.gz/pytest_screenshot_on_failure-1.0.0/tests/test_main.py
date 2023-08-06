from pathlib import Path
from typing import Union
from unittest.mock import Mock

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.main import Session
from _pytest.python import Function
from _pytest.reports import TestReport
from pytest_mock import MockFixture
from selenium.webdriver.chrome.webdriver import WebDriver

from src import pytest_screenshot_on_failure as psf


def get_parser_option_value(parameter: str) -> Union[bool, str]:
    if parameter == 'save_screenshots':
        return True
    elif parameter == 'screenshots_dir':
        return 'screenshot/dir/example'
    raise Exception(f'Unknown {parameter=} given.')


invalid_dir_names = [
    '2023-07-18-15:25:03.980',
    '2023-07-18.15:25:03.980',
    '2023-07-18-15:25:03.980',
    '2023-07-18:15:25:03.980',
    '2023-07-18 15:25:03-543',
    '2023.07.18 15:25:03.543',
    '2023:07:18 15:25:03.543',
    '2023-07-18 15.25.03.543',
    '2023-07-18 15-25-03.543',
    '2023.07.18 15:25:03.543',
    '2023-07-18 15.25.03.543',
    '2023-07-18 15:25:03:543',
    '2023-07-18 15:25:03',
    '2023-07-18 15:25',
    '2023-07-18',
    '15:25:03',
    'asd',
    '123',
    ''
]  # yapf: disable


@pytest.mark.parametrize('invalid_name', invalid_dir_names)
def test_dir_do_not_match_date_time_format(invalid_name: str) -> None:
    assert not psf.match_dir_date_time_format(invalid_name), f'{invalid_name=} was accepted as a valid date time format'


valid_dir_names = [
    '2023-07-18 15:25:03.980',
    '1998-12-31 20:04:58.763'
]  # yapf: disable


@pytest.mark.parametrize('valid_name', valid_dir_names)
def test_dir_match_date_time_format(valid_name: str) -> None:
    assert psf.match_dir_date_time_format(valid_name), f'{valid_name=} was not accepted as a valid date time format'


def test_archive_old_screenshots_method(mocker: MockFixture) -> None:
    mock_file_or_dir_exists = mocker.patch('os.path.exists', return_value=True)
    mock_remove_dir = mocker.patch('shutil.rmtree', return_value=True)
    mock_move_dir = mocker.patch('shutil.move', return_value=True)
    mock_log_warning = mocker.patch('logging.warning', return_value=True)

    screenshots_root_path = 'root_path/test_example'
    screenshot_dir_name = 'screenshots'
    psf.archive_old_screenshots(screenshots_root_path, screenshot_dir_name)

    mock_file_or_dir_exists.assert_called_once()
    mock_log_warning.assert_called_once()
    mock_remove_dir.assert_called_once()
    mock_move_dir.assert_called_once()


def test_capture_screenshot(mocker: MockFixture) -> None:

    def assert_image_exist(dir_name: str) -> bool:
        return '.png' in dir_name

    mock_file_or_dir_exists = mocker.patch('os.path.exists', side_effect=assert_image_exist)
    mock_create_test_suite_dir = mocker.patch('os.makedirs', return_value=True)
    mock_logging_warning = mocker.patch('logging.warning')

    mock_web_driver = Mock(spec=WebDriver)
    mock_save_screenshot = mocker.patch.object(mock_web_driver, 'save_screenshot', return_value=True)

    screenshots_root_path = 'root_path/test_example'
    psf.capture_screenshot(mock_web_driver, screenshots_root_path, test_suite='CoolTestSuite', test_name='cool_test')

    assert mock_file_or_dir_exists.call_count == 2
    mock_create_test_suite_dir.assert_called_once()
    mock_logging_warning.assert_called_once()
    mock_save_screenshot.assert_called_once()


def test_unable_to_capture_screenshot(mocker: MockFixture) -> None:

    def raise_exception(dir_path: str) -> None:
        raise Exception('Simulate exception')

    mock_file_or_dir_exists = mocker.patch('os.path.exists', return_value=True)
    mock_logging_error = mocker.patch('logging.error')

    mock_web_driver = Mock(spec=WebDriver)
    mock_save_screenshot = mocker.patch.object(mock_web_driver, 'save_screenshot', side_effect=raise_exception)

    screenshots_root_path = 'invalid/path'
    psf.capture_screenshot(mock_web_driver, screenshots_root_path, test_suite='CoolTestSuite', test_name='cool_test')

    assert mock_file_or_dir_exists.call_count == 2
    mock_save_screenshot.assert_called_once()
    mock_logging_error.assert_called_once()


def test_find_web_driver_instance() -> None:
    mock_web_driver = Mock(spec=WebDriver)

    mock_test_function_arguments = {'invalid_driver': 'web_driver', 'valid_driver': mock_web_driver}

    assert not psf.find_web_driver_instance({}), 'Expected method to return None when not finding a WebDriver instance'
    assert psf.find_web_driver_instance(mock_test_function_arguments), '''Expected method to return True when finding 
    a WebDriver instance'''


def test_skip_pytest_configure_if_there_is_no_screenshots_dir(mocker: MockFixture) -> None:
    mock_screenshot_root_exists = mocker.patch('os.path.exists', return_value=False)
    mock_make_screenshot_dir = mocker.patch('os.makedirs', return_value=True)

    mock_config = Mock(spec=Config)
    mock_config._rootpath = Path('project_root_path/example')
    mock_get_value = mocker.patch.object(mock_config, 'getvalue', side_effect=get_parser_option_value)

    psf.pytest_configure(mock_config)

    mock_make_screenshot_dir.assert_called_once()
    mock_screenshot_root_exists.assert_called_once()
    assert mock_get_value.call_count == 2


def test_skip_pytest_configure_if_feature_is_disabled(mocker: MockFixture) -> None:
    mock_logging_info = mocker.patch('logging.info')

    mock_config = Mock(spec=Config)
    mock_getvalue = mocker.patch.object(mock_config, 'getvalue', return_value=False)

    psf.pytest_configure(mock_config)

    mock_getvalue.assert_called_once()
    mock_logging_info.assert_called_once()


dir_names_list = ['history', 'not valid', '2023-07-18 15:25:03.980']
mock_dir_list = [Mock(spec=Config) for _ in range(3)]
for mock_dir, dir_name in zip(mock_dir_list, dir_names_list):
    mock_dir.name = dir_name
    mock_dir.path = 'path_to_dir'


def test_pytest_configure_archive_screenshots_and_delete_invalid_dirs(mocker: MockFixture) -> None:
    mock_screenshot_root_exists = mocker.patch('os.path.exists', return_value=True)
    mock_dir_lookup = mocker.patch('os.scandir', return_value=mock_dir_list)
    mock_archive = mocker.patch('src.pytest_screenshot_on_failure.archive_old_screenshots', return_value=True)
    mock_remove_dirs = mocker.patch('shutil.rmtree', return_value=True)

    mock_config = Mock(spec=Config)
    mock_config._rootpath = Path('project_root_path/example')
    mock_get_value = mocker.patch.object(mock_config, 'getvalue', side_effect=get_parser_option_value)

    psf.pytest_configure(mock_config)

    assert mock_get_value.call_count == 2
    mock_screenshot_root_exists.assert_called_once()
    mock_dir_lookup.assert_called_once()
    mock_archive.assert_called_once()
    mock_remove_dirs.assert_called_once()


def test_pytest_sessionfinish(mocker: MockFixture) -> None:
    mock_temp_dir_exists = mocker.patch('os.path.exists', return_value=True)
    mock_rename_dir = mocker.patch('shutil.move', return_value=True)

    mock_session = Mock(spec=Session)
    mock_session.config._rootpath = Path('project_root_path/example')
    mock_get_value = mocker.patch.object(mock_session.config, 'getvalue', side_effect=get_parser_option_value)

    psf.pytest_sessionfinish(mock_session, 0)

    mock_get_value.assert_called_once()
    mock_temp_dir_exists.assert_called_once()
    mock_rename_dir.assert_called_once()


def test_pytest_addoption(mocker: MockFixture) -> None:
    mock_parser = Mock(spec=Parser)
    mock_parser_addoption = mocker.patch.object(mock_parser, 'addoption', return_value=True)

    psf.pytest_addoption(mock_parser)

    assert mock_parser_addoption.call_count == 2


def test_conditions_to_capture_screenshot_on_test_case_routine_conditions(mocker: MockFixture) -> None:
    mock_web_driver = mocker.patch('src.pytest_screenshot_on_failure.find_web_driver_instance', return_value=None)

    mock_test_report = Mock(spec=TestReport)
    mock_test_report.when = None
    mocker.patch.object(mock_test_report, 'failed', return_value=False)
    mock_pytest_function = Mock(spec=Function)
    mock_pytest_function.funcargs = {}
    mock_getvalue = mocker.patch.object(mock_pytest_function.config, 'getvalue', return_value=False)

    psf.after_test_case_routine(mock_test_report, mock_pytest_function)

    mock_getvalue.assert_called_once()
    mock_web_driver.assert_not_called()


def test_after_test_case_routine_without_web_driver_found(mocker: MockFixture) -> None:
    mock_log_warning = mocker.patch('logging.warning', return_value=True)
    mock_find_web_driver = mocker.patch('src.pytest_screenshot_on_failure.find_web_driver_instance', return_value=None)

    mock_test_report = Mock(spec=TestReport)
    mock_test_report.when = 'call'
    mocker.patch.object(mock_test_report, 'failed', return_value=True)
    mock_pytest_function = Mock(spec=Function)
    mock_pytest_function.funcargs = {'key1': 'nothing_here', 'key2': 'nor_here'}
    mock_get_value = mocker.patch.object(mock_pytest_function.config, 'getvalue', side_effect=get_parser_option_value)

    psf.after_test_case_routine(mock_test_report, mock_pytest_function)

    mock_find_web_driver.assert_called_once()
    mock_get_value.assert_called_once()
    mock_log_warning.assert_called_once()


def test_after_test_case_routine_capturing_screenshot(mocker: MockFixture) -> None:
    mock_capture_screenshot = mocker.patch('src.pytest_screenshot_on_failure.capture_screenshot', return_value=True)
    mock_web_driver = Mock(spec=WebDriver)
    mock_web_driver_found = mocker.patch('src.pytest_screenshot_on_failure.find_web_driver_instance',
                                         return_value=mock_web_driver)

    mock_test_report = Mock(spec=TestReport)
    mock_test_report.when = 'call'
    mocker.patch.object(mock_test_report, 'failed', return_value=True)

    mock_pytest_function = Mock(spec=Function)
    mock_pytest_function.config._rootpath = Path('project_root_path/example')
    mock_pytest_function.funcargs = {'key1': 'nothing_here', 'key2': 'nor_here'}
    mock_pytest_function.name = 'Very creative test CASE name'
    mock_pytest_function.parent = Mock()
    mock_pytest_function.parent.name = 'Very creative test SUITE name'
    mock_get_value = mocker.patch.object(mock_pytest_function.config, 'getvalue', side_effect=get_parser_option_value)

    psf.after_test_case_routine(mock_test_report, mock_pytest_function)

    mock_web_driver_found.assert_called_once()
    mock_capture_screenshot.assert_called_once()
    assert mock_get_value.call_count == 2
