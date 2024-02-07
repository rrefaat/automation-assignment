import os
import platform
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config.config import Resources

 

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )

@pytest.fixture(scope="function")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name").lower()
    browser_name = os.environ.get('BROWSER_NAME', browser_name)
    webdriver_Loading_error = "Couldn't load webdriver, fallback to local driver"
    if browser_name == "chrome":
        options = Options()
        options.add_argument("start-maximized")
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.implicitly_wait(5)
        except Exception:
            print(webdriver_Loading_error)
            if platform.system() == "Windows":
                driver = webdriver.Chrome(Resources.WINDOWS_CHROME_DRIVER)
            else:
                raise Exception("Unsupported Operating System")
    elif browser_name == "firefox":
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = False
        options = Options()
        options.add_argument("start-maximized")
        try:
            driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()), options=options)
        except Exception:
            print(webdriver_Loading_error)
            if platform.system() == "Windows":
                driver = webdriver.Firefox(capabilities=cap, executable_path=Resources.WINDOWS_FIREFOX_DRIVER)
            else:
                raise Exception("Unsupported Operating System")
    elif browser_name == "edge":
        try:
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        except Exception:
            print(webdriver_Loading_error)
            if platform.system() == "Windows":
                driver = webdriver.Chrome(Resources.WINDOWS_EDGE_DRIVER)
            else:
                raise Exception("Unsupported Operating System")
    else:
        print("Unsupported browser")
        raise Exception(f"Unsupported browser ${browser_name}, only [chrome - edge - firefox] are supported")
    driver.maximize_window()
    request.cls.driver = driver
    driver.get(os.environ.get('ENV_PATH', Resources.ENV_PATH))
    yield
    driver.quit()

