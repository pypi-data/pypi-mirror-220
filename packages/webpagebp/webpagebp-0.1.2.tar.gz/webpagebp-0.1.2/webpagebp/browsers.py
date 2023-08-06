from webpagebp.generic_browser.browser import _Browser
from webpagebp.selenium_driver.drivers import ChromeDriver, FirefoxDriver


class ChromeBrowser(_Browser):
    def __init__(self, browser_driver=ChromeDriver, *args, **kwargs):
        super().__init__(browser_driver=browser_driver, *args, **kwargs)


class ChromeHBrowser(_Browser):
    def __init__(self, browser_driver=ChromeDriver, headless=True, *args, **kwargs):
        super().__init__(browser_driver=browser_driver, headless=headless, *args, **kwargs)


class FirefoxBrowser(_Browser):
    def __init__(self, browser_driver=FirefoxDriver, *args, **kwargs):
        super().__init__(browser_driver=browser_driver, *args, **kwargs)


class FirefoxHBrowser(_Browser):
    def __init__(self, browser_driver=FirefoxDriver, headless=True, *args, **kwargs):
        super().__init__(browser_driver=browser_driver, headless=headless, *args, **kwargs)
