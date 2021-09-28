import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import glob


def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="localhost:8000")


def get_asset_paths():
    filenames = []
    import logging

    # logging.warning(os.getcwd())
    for filename in glob.glob(os.getcwd() + "/assets/*"):
        filenames.append(filename)
        # logging.warning(filename)
    for f in filenames:
        logging.warn("fileNAME: " + f)
    logging.warn("filenames: ", filenames)


@pytest.fixture(scope="session")
def server(request):
    return "http://" + request.config.getoption("--server")


@pytest.fixture(scope="module")
def authenticate(server):
    opts = webdriver.ChromeOptions()
    opts.headless = False
    opts.add_argument("start-maximized")
    cd = webdriver.Chrome(options=opts)
    cd.get(server + "/login")
    username = "test@test.com"
    password = "123456"

    username_field = cd.find_element_by_xpath("//*[@id='emailTxt']")
    username_field.send_keys(username)
    password_field = cd.find_element_by_xpath("//*[@id='passwordTxt']")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)


@pytest.fixture(scope="class")
def init_chrome_driver(request):
    opts = webdriver.ChromeOptions()
    opts.headless = False
    opts.add_argument("start-maximized")
    opts.add_argument("user-data-dir=selenium")
    web_driver = webdriver.Chrome(options=opts)
    request.cls.driver = web_driver
    yield
    web_driver.close()


@pytest.fixture(scope="session")
def init_driver(server, request):
    opts = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": os.getcwd() + "/",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    opts.add_experimental_option("prefs", prefs)
    opts.headless = False
    opts.add_argument("start-maximized")
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
    yield
    get_asset_paths()
    web_driver.close()


@pytest.fixture(scope="class")
def init_firefox_driver(request):
    opts = webdriver.FirefoxOptions()
    opts.headless = False
    web_driver = webdriver.Firefox(options=opts)
    request.cls.driver = web_driver
    yield
    web_driver.close()
