from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from webpagebp.selenium_driver.generic_driver import _Driver


class ChromeDriver(_Driver):
    def __init__(
        self, 
        service: Service = Service(ChromeDriverManager().install()), 
        webdriver: webdriver = webdriver.Chrome, 
        name = 'chrome', 
        *args, 
        **kwargs):
        super().__init__(service=service, webdriver=webdriver, name=name, *args, **kwargs)

    def load_startup_options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument("log-level=3")
        options.add_argument("enable-automation")
        if self.run_headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        options.add_argument("--silent")
        prefs = {"download.default_directory" : self.dir_path}
        options.add_experimental_option("prefs", prefs)
        return options


class FirefoxDriver(_Driver):
    def __init__(
        self, 
        service: Service = Service(GeckoDriverManager().install()),
        webdriver: webdriver = webdriver.Firefox,
        name = 'firefox', 
        *args, 
        **kwargs):
        super().__init__(service=service, webdriver=webdriver, name=name, *args, **kwargs)

    def load_startup_options(self) -> FirefoxOptions:
        options = FirefoxOptions()
        options.headless = False
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", self.dir_path)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")        
        if self.run_headless:
            options.headless = True
        return options
