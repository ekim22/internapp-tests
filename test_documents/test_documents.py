from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException


@pytest.mark.usefixtures("driver", "logger")
class Test_Documents:
    def test_document_ops(self, server, document):
        doc_path = document[0]
        doc_count = document[1]

        self._doc_upload(doc_count, doc_path)
        self.driver.get(server + "/home")
        self._doc_download(doc_count)
        self.driver.get(server + "/home")
        # 2 secs will fail; 3 appears to be optimal
        sleep(2)
        self._doc_delete(doc_count)

    def _doc_upload(self, doc_count, doc_path):
        try:
            # There should be no documents visible at the point of upload
            self.driver.find_element_by_xpath(
                '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
                + doc_count
                + "]/td[7]/a/span"
            ).is_displayed()
            assert False, "A document already exists in row " + doc_count
        except NoSuchElementException:
            assert True

        self.driver.find_element_by_xpath(
            "//*[@id='uploadForm1']/div[1]/input"
        ).send_keys(doc_path)
        self.driver.find_element_by_xpath("//*[@id='uploadForm1']").click()
        self.driver.find_element_by_xpath("//*[@id='uploadResume']").click()

    def _doc_download(self, doc_count):
        assert self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
            + doc_count
            + "]/td[7]/a/span"
        ).is_displayed(), ("No document exists in row " + doc_count + " to download")

        self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
            + doc_count
            + "]/td[7]/a/span"
        ).click()

    def _doc_delete(self, doc_count):
        assert self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
            + doc_count
            + "]/td[8]/a/span"
        ).is_displayed(), ("No document exists in row " + doc_count + " to delete")

        self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
            + doc_count
            + "]/td[8]/a/span"
        ).click()
