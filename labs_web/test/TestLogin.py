import unittest
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import choice
from labs_web.test_data import tutors, students
from . import TestConfig, AbstractTest


class TestLogin(AbstractTest):
    """
    Test login scenarios
    """

    def setUp(self):
        """
        1. Call super setUp()
        2. Get login page
        3. Find form elements
        """
        super(TestLogin, self).setUp()
        # self.driver = selenium.webdriver.Chrome()
        self.driver.get(f"{TestConfig.SERVER_URL}:{TestConfig.SERVER_PORT}/auth/login/")
        # WebDriverWait(self.driver, 10).until(EC.element_to_be_selected(By.ID, ))
        # self.driver.implicitly_wait(4)
        wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        self.username = self.driver.find_element_by_id("username")
        self.password = self.driver.find_element_by_id("password")
        self.form = self.driver.find_element_by_tag_name("form")
        self.submit = self.form.find_element_by_tag_name("button")

    def test_login_login_not_exist(self):
        """
        send un-existing credentials, alert should be shown
        """
        self.username.send_keys("NON-EXISTING")
        self.password.send_keys("DEFINITELY_WRONG")
        self.submit.click()
        alert_present = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "alert")))
        self.assertTrue(alert_present)

    def test_wrong_password(self):
        """
        send correct username with wrong password
        """
        row = choice(tutors)
        login = row[1]
        self.username.send_keys(login)
        self.password.send_keys("DEFINITELY_WRONG")
        self.submit.click()
        alert = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "alert")))
        self.assertTrue(alert)

    def test_correct_login_tutor(self):
        """
        sending correct tutor's credentials, should redirect to tutor home page
        """
        row = choice(tutors)
        login = row[1]
        self.username.send_keys(login)
        self.password.send_keys(TestConfig.DEFAULT_PASSWORD)
        self.submit.click()
        navbar_present = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
        self.assertTrue(navbar_present)
        self.assertIn("/tutor/home/", self.driver.current_url)

    def test_correct_login_student(self):
        """
        sending correct student's credentials, should redirect to student home page
        """
        row = choice(students)
        login = row[2]
        self.username.send_keys(login)
        self.password.send_keys(TestConfig.DEFAULT_PASSWORD)
        self.submit.click()
        navbar_present = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
        self.assertTrue(navbar_present)
        self.assertIn("/student/home/", self.driver.current_url)

    # def tearDown(self):
    #     self.driver.close()
