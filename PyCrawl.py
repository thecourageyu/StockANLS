import os
import sys
import unittest

import urllib
import urllib.request as urllib2


request = urllib2.Request("https://www.rakuten.com.tw/shop/food-collect/product/apple2017072100/?s-id=Event-supersale-170814-index-081820-003")
response = urllib2.urlopen(request)
print(response.read())

import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

url1 = "https://www.rakuten.com.tw/shop/food-collect/product/apple2017072100/?s-id=Event-supersale-170814-index-081820-003"
ChromeDriver = "D:/chromedriver_win32/chromedriver.exe"
browser = webdriver.Chrome(executable_path=ChromeDriver)
browser.get(url1)
#assert "afv" in browser.title

webdriver.find_element(By.XPATH, '//button[text()="Some text"]')
browser.find_elements(By.XPATH, '//button')
browser.find_element_by_class_name("b-btn")


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