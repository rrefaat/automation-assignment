import os
import os.path
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

 
class BasePage:

    """This class is the parent of all pages it contains all the generic methods and utilities for all pages"""

    def __init__(self, driver):
        self.driver = driver

    def assert_text_on_url(self, text):
        time.sleep(20)
        current_url = self.driver.current_url
        assert text in current_url

    def go_page_back(self):
        self.driver.execute_script("window.history.go(-1)")

    def assert_on_element_text(self, element,expected_text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(element))
        element_text = self.get_text(element)
        if( expected_text in element_text):
            return True
        else:
            return False
        
    def select_from_list(self, list,option):
        self.do_send_keys(list, self.random_string(3))
        found = self.assert_on_text("No items found")
        while(found == True):
            self.clear(list)
            self.do_send_keys(list, self.random_string(3))
            found = self.assert_on_text("No items found")
        self.do_click(option)

    def assert_on_text(self,expected_text):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_text}')]")))
            return True
            print(f"Assertion: '{expected_text}' is visible on the page.")
        except Exception as e:
            return False
            print(f"Assertion failed: '{expected_text}' is not visible on the page.")
            print(e)   

    def get_page_title(self, title):
        WebDriverWait(self.driver, 10).until(EC.title_is(title))
        return self.driver.title

    def do_toggle(self, button):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(button)).click()

    def do_click(self, button):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(button)).click()


    def navigate_to_link(self, link):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(link)).click()


    def do_hover(self, element):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(element))
        hover = ActionChains(self).move_to_element(element)
        hover.perform()


    def check_downloaded_file(self, file_name):
        download_path = self.get_download_folder()
        file_path = os.path.join(download_path, file_name)
        os.path.isfile(file_path)
        print(file_path)
        assert file_name in file_path
        time.sleep(3)

    def get_root_path(self, foldername):
        return os.path.dirname(os.path.abspath(foldername))

    def get_path(self, first_path, second_path):
        return os.path.join(first_path, second_path)

    def clear(self, text_field):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(text_field)).clear()

    def click_on_element(self, btn):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(btn)).click()

    def do_search(self, text):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located())
            result = self.assert_on_text(element, text)
            return result
        except Exception:
            return False

    def do_send_keys(self, text_field, text):
        field = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(text_field))
        field.send_keys(text)


    def upload_file(self, input_file_field, filepath):
        try:
            filename = os.path.abspath(filepath)
            print(filename)
            file_upload = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(input_file_field))
            file_upload.send_keys(filename)
        except Exception as e:
            print(e)
            print('Either element was not found, or cant upload file') 

    def get_text(self, element):
        try:
            actual_text = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(element)).text
            print(actual_text)
            return actual_text
        except Exception as e:
            print(e)
            print('Either element was not found, or Bot could not click on it.')


    def check_text(self, element, text):
        try:
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element(element, text))
            print("Desired text was present")
        except Exception:
            print("Desired text was not present")
 

    def random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
 

    def random_number(self, value):
        return random.randint(2, value)
    
    def select_option_from_list(self, selected_option, list):
        dropdown =  WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(list))
        # Click on the dropdown to open the options
        dropdown.click()
        # Find the specific option you want by its text
        option_text = selected_option
        option_locator = (By.XPATH, f"//option[text()='{option_text}']")
        option = self.driver.find_element(*option_locator)
        # Click on the option to select it
        option.click()