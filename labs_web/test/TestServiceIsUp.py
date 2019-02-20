import unittest
import selenium.webdriver
from . import TestConfig


class TestServiceIsUp(unittest.TestCase):
    """
    Check that server is alive and returning login view
    """

    def test_login_view(self):
        driver = selenium.webdriver.Chrome()
        driver.get(f"{TestConfig.SERVER_URL}:{TestConfig.SERVER_PORT}")
        self.assertEqual(driver.title, "Sign in")
        driver.close()

