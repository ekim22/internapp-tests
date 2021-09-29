import pytest
import tempfile
import time
import pickle
import os


@pytest.mark.usefixtures("init_driver")
class Test_Documents:
    def test_document_ops(self, server, document, temp_dir):
        # TODO: create tempfile with extension .docx and upload using sel
        # TODO: make tempdir, download file to temp dir, check the right
        # dl folder for existence of file to pass test.
        # TODO: delete file from app; assert file is gone.
        doc_path = document[0]
        doc_count = str(document[1])
        import logging

        logger = logging.getLogger()
        logger.warning(document[0])
        logger.warning(document[1])

        self.driver.get(server + "/home")
        self._doc_upload(doc_path)
        self.driver.get(server + "/home")
        # time.sleep(3)
        self._doc_download(doc_count)
        # sample_doc_path = os.scandir(temp_dir)
        # logger.warning(temp_dir)
        # dir2 = os.listdir("/tmp")
        # assert len(dir2) > 0
        # logger.info(dir2)
        # time.sleep(60)
        self.driver.get(server + "/home")
        # time.sleep(5)
        self._doc_delete(doc_count)

    def _doc_upload(self, doc_path):
        self.driver.find_element_by_xpath(
            "//*[@id='uploadForm1']/div[1]/input"
        ).send_keys(doc_path)
        self.driver.find_element_by_xpath("//*[@id='uploadForm1']").click()
        self.driver.find_element_by_xpath("//*[@id='uploadResume']").click()
        # time.sleep(5)

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
        # time.sleep(2)

    def _doc_delete(self, doc_count):
        self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr['
            + doc_count
            + "]/td[8]/a/span"
        ).click()
        # time.sleep(4)
