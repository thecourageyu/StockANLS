import os
import sys
import unittest

import urllib
import urllib.request as urllib2

urllib.Request(http://lvr.land.moi.gov.tw/homePage.action)
response = urllib2.urlopen("http://www.baidu.com")
print(response.read())



from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ChromeDriver = "D:/chromedriver_win32/chromedriver.exe"
browser = webdriver.Chrome(executable_path=ChromeDriver)
browser.get("http://www.python.org")
#assert "afv" in browser.title


elem = browser.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
print(browser.page_source)


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()