from .. import AbstractTest, TestConfig
from labs_web.test_data import tutors
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import choice


class AbstractTutorTest(AbstractTest):
    """
    Abstract class for testing features for tutors
    """
    def setUp(self):
        """
        perform login as tutor
        """
        super(AbstractTutorTest, self).setUp()
        self.driver.get(f"{TestConfig.SERVER_URL}:{TestConfig.SERVER_PORT}/auth/login/")
        wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        self.username = self.driver.find_element_by_id("username")
        self.password = self.driver.find_element_by_id("password")
        self.form = self.driver.find_element_by_tag_name("form")
        self.submit = self.form.find_element_by_tag_name("button")
        user = choice(tutors)
        self.username.send_keys(user[1])
        self.password.send_keys(TestConfig.DEFAULT_PASSWORD)
        self.submit.click()
        wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))


