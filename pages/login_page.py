import os
import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class Login(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    username_feild = By.NAME, "email"
    password_feild = By.NAME, "password"
    login_btn = By.XPATH, "//button[@data-qa='login-button']"



    def login(self,username,password):
        self.do_send_keys(self.username_feild,username)
        self.do_send_keys(self.password_feild,password)
        self.do_click(self.login_btn)
        print("User Login Successfully ")
