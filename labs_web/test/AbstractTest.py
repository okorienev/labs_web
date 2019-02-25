import unittest
from selenium.webdriver.chrome.options import Options
from .Config import TestConfig
from selenium import webdriver


class AbstractTest(unittest.TestCase):
    def setUp(self):
        chrome_opts = Options()
        # chrome_opts.add_argument("--headless")
        # chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("window-size=" + str(TestConfig.SCREEN_WIDTH) + 'x' + str(TestConfig.SCREEN_HEIGHT))
        self.driver = webdriver.Chrome(options=chrome_opts)

    def tearDown(self):
        self.driver.close()
