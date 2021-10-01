import pytest
import random
import string

from selenium.webdriver.common.keys import Keys


@pytest.mark.usefixtures("init_driver")
class Test_Application:
    # Signup form sample data
    email = (
        "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(12)
        )
        + "@pytest.com"
    )
    password = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
    student_id = "9".join(random.choice(string.digits) for _ in range(8))
    first_name = "Selenium"
    last_name = "Test"
    address = "1000 Testing Ave"
    city = "Testsite"
    state = "TS"
    zip_code = "10000"

    # Signup form ids set to sample data values
    signup_form = {
        "emailTxt": email,
        "cfmEmailTxt": email,
        "passwordTxt": password,
        "cfmPasswordTxt": password,
        "studentIdTxt": student_id,
        "fnameTxt": first_name,
        "lnameTxt": last_name,
        "addressTxt": address,
        "stateTxt": city,
        "cityTxt": state,
        "zipTxt": zip_code,
    }

    # Application data
    application_email = "test_application@pytest.com"
    application_email_password = "123456"
    application_signature = "".join(
        random.choice(string.ascii_lowercase) for _ in range(10)
    )

    def test_signup(self, server):
        self.driver.get(server + "/signup")

        for form_id, form_value in self.signup_form.items():
            self.driver.find_element_by_xpath('//*[@id="' + form_id + '"]').send_keys(
                form_value
            )

        self.driver.find_element_by_xpath('//*[@id="signupBtn"]').click()

        assert (
            self.driver.find_element_by_xpath("/html/body/div/h1").text
            == "Welcome " + self.first_name + "!"
        )

    def test_bio_application(self, server):
        # Login with premade applicant
        self.driver.get(server + "/login")
        username_field = self.driver.find_element_by_xpath("//*[@id='emailTxt']")
        username_field.send_keys(self.application_email)
        password_field = self.driver.find_element_by_xpath("//*[@id='passwordTxt']")
        password_field.send_keys(self.application_email_password)
        password_field.send_keys(Keys.RETURN)

        # Set bio application's signature and printed name to randomly generated string
        self.driver.get(server + "/editBIO")
        signature_field = self.driver.find_element_by_xpath("//*[@id='signatureTxt']")
        signature_field.send_keys(Keys.CONTROL + "a")
        signature_field.send_keys(Keys.DELETE)
        signature_field.send_keys(self.application_signature)
        printed_field = self.driver.find_element_by_xpath("//*[@id='printedTxt']")
        printed_field.send_keys(Keys.CONTROL + "a")
        printed_field.send_keys(Keys.DELETE)
        printed_field.send_keys(self.application_signature)
        printed_field.send_keys(Keys.RETURN)

        # Assert bio applicant's signature and printed name is the randomly generated string
        self.driver.get(server + "/home")
        self.driver.find_element_by_xpath(
            "//*[@id='applicationTableOnHomePage']/table/tbody/tr[1]/td[4]/a/span"
        ).click()
        applicant_signature = self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/table[1]/tbody/tr[37]/td[2]"
        ).text
        applicant_printed_name = self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/table[1]/tbody/tr[38]/td[2]"
        ).text
        assert (
            self.application_signature == applicant_signature
            and self.application_signature == applicant_printed_name
        )

    def test_itec_application(self, server):
        # Login with premade applicant
        self.driver.get(server + "/login")
        username_field = self.driver.find_element_by_xpath("//*[@id='emailTxt']")
        username_field.send_keys(self.application_email)
        password_field = self.driver.find_element_by_xpath("//*[@id='passwordTxt']")
        password_field.send_keys(self.application_email_password)
        password_field.send_keys(Keys.RETURN)

        # Set itec application's signature and printed name to randomly generated string
        self.driver.get(server + "/editITEC")
        signature_field = self.driver.find_element_by_xpath("//*[@id='signatureTxt']")
        signature_field.send_keys(Keys.CONTROL + "a")
        signature_field.send_keys(Keys.DELETE)
        signature_field.send_keys(self.application_signature)
        printed_field = self.driver.find_element_by_xpath("//*[@id='printedTxt']")
        printed_field.send_keys(Keys.CONTROL + "a")
        printed_field.send_keys(Keys.DELETE)
        printed_field.send_keys(self.application_signature)
        printed_field.send_keys(Keys.RETURN)

        # Assert itec applicant's signature and printed name is the randomly generated string
        self.driver.get(server + "/home")
        self.driver.find_element_by_xpath(
            "//*[@id='applicationTableOnHomePage']/table/tbody/tr[2]/td[4]/a/span"
        ).click()
        applicant_signature = self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/table[1]/tbody/tr[22]/td[2]"
        ).text
        applicant_printed_name = self.driver.find_element_by_xpath(
            "/html/body/div/div[2]/table[1]/tbody/tr[23]/td[2]"
        ).text
        assert (
            self.application_signature == applicant_signature
            and self.application_signature == applicant_printed_name
        )
