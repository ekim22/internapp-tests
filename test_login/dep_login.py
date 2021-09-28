import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


@pytest.mark.usefixtures("init_chrome_driver")
class Test_Login:
    def test_login(self, server):
        # TODO: should have a dynamic way of setting/getting address
        self.driver.get(server + "/login")

        username = "test@test.com"
        password = "123456"

        username_field = self.driver.find_element_by_xpath("//*[@id='emailTxt']")
        username_field.send_keys(username)
        password_field = self.driver.find_element_by_xpath("//*[@id='passwordTxt']")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # time.sleep(3)

        expected_welcome_user = "Welcome test!"
        welcome_user = self.driver.find_element_by_xpath("/html/body/div/h1").text
        assert expected_welcome_user == welcome_user
