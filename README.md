# GGC InternApp Tests (Pytest/Selenium)
Tests written using Pytest and Selenium in Python 3.9. They were made to automate the functional testing of account, document, and application operations.

## Account tests
[Test_signup.py](test_signup/test_signup.py) tests the signup feature by randomizing an email and password and filling out the other necessary fields and asserting 
that the page has navigated to /home. Failure would imply a change to the codebase is interfering with this essential operation.

## Document tests
[Test_documents.py](test_documents/test_documents.py) tests the document upload, download, and delete features. The upload test first asserts that the document table is empty before proceeding to upload a sample document with a randomized, unique file name. The download test then scans the document table and asserts that a document exists in the document table, clicks the download button for the document in the table, then asserts that the document downloaded to "tmp" directory matches the file name of the document that was uploaded. Lastly, the delete test asserts that there is a document in the documents table and clicks the delete button. 

## Application tests
[Test_application.py](test_application/test_applications.py) tests that the two types of applications ("bio" and "itec" programs) can be accessed upon logging in, that their respective applications' signature fields are settable upon signing with a randomly generated signature at runtime, and that the signature matches the randomly generated signature upon viewing the application's details page, verifying the application has updated properly.

## Purpose
This suite of tests verifies that the account creation, document management, and application management features are in working order - the failure of any one of which causes total or major unusability of the application. 

## Benefits
Running the tests prior to merging any changes into the main branch protects the application from non-production ready changes, thereby minimizing the downtime caused by crashes and reverting to a prior version. Additionally, while the tests can be run serially, they are intended and configured to be run in parallel using pytest-xdist.

## Issues
While the tests can point to a problem with a feature, since these are functional tests they cannot pinpoint why there is a problem. In the example below, the test suite was run against a pull request which resulted in the failure of one of the tests. Opening the details for the failed test we see that pytest complains about an ``AssertionError: Signatures do not match`` at ``test_application/test_application.py:81``. Further, line 41 of the error report shows that the signature assertion specifically failed in the ``test_itec_application`` test, so we know that there was an issue with the itec application. However, we do not know why exactly. Since the assert statement shows two different signatures, the one read from the application and the one that was randomly generated for the test, we can assume there was an issue updating the itec application after setting the signature field in the ``_set_signatures`` test method.

Manually attempting to set the signature in the application shows that indeed there is a problem; the phone number field is empty, when it is a required field that must have been filled out prior to the application being submitted. By checking out from the PR branch back to master and running the tests again, we instead see a 100% pass rate, which includes the troublesome test from the PR branch. This information tells us that it is in fact the changes made in the PR branch that have caused the problem, which ensures that we do not accept the pull request and that we can instead direct the PR author's attention to code that may have broken the itec application only, since the same tests that ran for the bio application did not cause any issues.

This is a real example of a pull request made by an actual student working on the application. The problem ended up being related to changes the student had made to how the phone number data was accessed by the application for the _itec_ application as a part of their attempt to fulfil a functional requirement. As one of two maintainers of the application, having the tests beforehand meant that I saved significant time in reviewing a student's pull request because the tests could inform me if any major features had become broken. While a 100% pass would not mean a pull request was ready or that I could avoid manual review of the code in the commmits, a fail did mean I could know whether to reject one in seconds.
