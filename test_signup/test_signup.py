import pytest
import random
import string

import logging

logger = logging.getLogger()


@pytest.mark.usefixtures("init_driver")
class Test_Signup:
    """Signup form sample data"""

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
