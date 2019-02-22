import unittest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class AbstractTest(unittest.TestCase):
    def setUp(self):
        chrome_opts = Options()
        # chrome_opts.add_argument("--headless")
        # chrome_opts.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_opts)

    def tearDown(self):
        self.driver.close()
