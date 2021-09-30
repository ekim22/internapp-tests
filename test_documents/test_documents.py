import pytest
import time


@pytest.mark.usefixtures("init_driver")
class Test_Documents:
    def test_document_ops(self, server, document):
        doc_path = document[0]
        doc_count = str(document[1])

        # self.driver.get(server + "/home")
        self._doc_upload(doc_path)

        self.driver.get(server + "/home")
        # time.sleep(3)
        self._doc_download(doc_count)

        self.driver.get(server + "/home")
        # 2 secs will fail; 3 appears to be optimal
        time.sleep(3)
        self._doc_delete(doc_count)

    def _doc_upload(self, doc_path):
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
        ).is_displayed()

        self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
            + doc_count
            + "]/td[7]/a/span"
        ).click()

    def _doc_delete(self, doc_count):
        self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
            + doc_count
            + "]/td[8]/a/span"
        ).click()
