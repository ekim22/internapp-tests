import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import glob
import tempfile
import sys

import logging


"""
pytest-xdist doesn't produce live logs without redirecting
stdout to stderr, even when log_cli is set to true. Running
pytest without -n (therefore vanilla pytest) produces live logs
appropriately, so it is only when running xdist this is needed.#!/usr/bin/env python

Refer to this issue for further updates:
https://github.com/pytest-dev/pytest-xdist/issues/402
"""
sys.stdout = sys.stderr

logger = logging.getLogger()


def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="localhost:8000")


def pytest_generate_tests(metafunc):
    test_docs = []
    for count, doc in enumerate(glob.glob(os.getcwd() + "/assets/documents/*")):
        test_docs.append((doc, count + 1))
    logger.info(test_docs)
    if "document" in metafunc.fixturenames:
        metafunc.parametrize("document", test_docs)


@pytest.fixture(scope="session")
def server(request):
    return "http://" + request.config.getoption("--server")


@pytest.fixture(scope="session")
def temp_dir(request):
    # temp directory for downloads
    temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
    import logging

    # logger = logging.getLogger()
    # logger.info(temp_dir.name)
    return temp_dir


@pytest.fixture(scope="session")
def init_driver(server, temp_dir, request):
    import logging

    # logger = logging.getLogger()
    # logger.info(temp_dir)
    opts = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": temp_dir.name,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }
    opts.add_experimental_option("prefs", prefs)
    opts.headless = True
    # opts.headless = False
    opts.add_argument("--window-size=1920,1080")
    # opts.add_argument("start-maximized")
    web_driver = webdriver.Chrome(options=opts)
    web_driver.get(server + "/login")
    username = "test@test.com"
    password = "123456"

    username_field = web_driver.find_element_by_xpath("//*[@id='emailTxt']")
    username_field.send_keys(username)
    password_field = web_driver.find_element_by_xpath("//*[@id='passwordTxt']")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", web_driver)
    # request.cls.driver = web_driver
    yield
    web_driver.close()
