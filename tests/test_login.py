import os
import time
from tests.test_base import BaseTest
from pages.login_page import Login
from config.config import Resources


class TestLogin(BaseTest):
    def test_login(self):
        Loginpage = Login(self.driver)
        Loginpage.login(Resources.USERNAME,Resources.PASSWORD)