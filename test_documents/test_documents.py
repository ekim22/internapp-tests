import pytest
import tempfile
import time
import pickle
import os


@pytest.mark.usefixtures("init_driver")
class Test_Documents:
    def test_document_ops(self, server, sample_doc):
        # TODO: create tempfile with extension .docx and upload using sel
        # TODO: make tempdir, download file to temp dir, check the right
        # dl folder for existence of file to pass test.
        # TODO: delete file from app; assert file is gone.

        # import logging

        # logger = logging.getLogger()
        # logger.warn(sample_file)
        # a = []
        # print("a: " + a)

        self.driver.get(server + "/home")
        self._doc_upload(sample_doc)
        time.sleep(50)
        # assert self.driver.find_element_by_xpath("//*[@id='documentTableOnHomePage']/div[1]/table/tbody/tr/td[2]").is_displayed()
        # self.driver.get(server + "/home")
        # self._doc_download()
        # self.driver.get(server + "/home")
        # self._doc_delete()

    def _doc_upload(self, sample_doc):
        f = self.driver.find_element_by_xpath("//*[@id='uploadForm1']/div[1]/input")
        f.send_keys(sample_doc)
        self.driver.find_element_by_xpath("//*[@id='uploadForm1']").click()
        self.driver.find_element_by_xpath("//*[@id='uploadResume']").click()
        # time.sleep(5)

    def _doc_download(self):
        assert self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr/td[7]/a/span'
        ).is_displayed()
        self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr/td[7]/a/span'
        ).click()
        # time.sleep(2)

    def _doc_delete(self):
        self.driver.find_element_by_xpath(
            '//*[@id="documentTableOnHomePage"]/div[1]/table/tbody/tr/td[8]/a/span'
        ).click()
        # time.sleep(4)
