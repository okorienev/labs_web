import unittest
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import choice
from labs_web.test_data import tutors, students
from . import TestConfig


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = selenium.webdriver.Chrome()
        self.driver.get(f"{TestConfig.SERVER_URL}:{TestConfig.SERVER_PORT}/auth/login/")
        self.username = self.driver.find_element_by_id("username")
        self.password = self.driver.find_element_by_id("password")
        self.form = self.driver.find_element_by_tag_name("form")
        self.submit = self.form.find_element_by_tag_name("button")

    def test_login_login_not_exist(self):
        self.username.send_keys("NON-EXISTING")
        self.password.send_keys("DEFINITELY_WRONG")
        self.submit.click()
        alert_present = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "alert")))
        self.assertTrue(alert_present)

    def test_wrong_password(self):
        row = choice(tutors)
        login = row[1]
        self.username.send_keys(login)
        self.password.send_keys("DEFINITELY_WRONG")
        self.submit.click()
        alert = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "alert")))
        self.assertTrue(alert)

    def test_correct_login_tutor(self):
        row = choice(tutors)
        login = row[1]
        self.username.send_keys(login)
        self.password.send_keys(TestConfig.DEFAULT_PASSWORD)
        self.submit.click()
        navbar_present = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
        self.assertTrue(navbar_present)
        self.assertIn("/tutor/home/", self.driver.current_url)

    def test_correct_login_student(self):
        row = choice(students)
        login = row[2]
        self.username.send_keys(login)
        self.password.send_keys(TestConfig.DEFAULT_PASSWORD)
        self.submit.click()
        navbar_present = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
        self.assertTrue(navbar_present)
        self.assertIn("/student/home/", self.driver.current_url)

    def tearDown(self):
        self.driver.close()
