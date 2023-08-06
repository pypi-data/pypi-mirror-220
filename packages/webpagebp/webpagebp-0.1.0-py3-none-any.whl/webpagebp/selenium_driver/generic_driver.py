from selenium.webdriver.common.by import By
import os

from webpagebp.utils import full_path


class _Driver:
    def __init__(self, service=None, webdriver=None, name=None, dir='', headless=False, *args, **kwargs):
        self.dir_path = full_path(dir)
        self.name = name
        self.run_headless = headless
        self.startup_options = self.load_startup_options()
        self.webdriver = webdriver
        self.service = service

    def load_startup_options(self) -> None:
        return None

    def start(self) -> None:
        if self.service is None:
            raise NotImplementedError("You should not use this class directly")
        self.driver = self.webdriver(service=self.service, options=self.startup_options)

    def start_headless(self) -> None:
        self.startup_options.add_argument('--headless')
        self.driver = self.webdriver(service=self.service, options=self.startup_options)

    def quit(self) -> None:
        self.driver.quit()

    def close_window(self) -> None:
        self.driver.close()

    def find(self, method, args, all=False):
        dic = {
            'tag': By.TAG_NAME,
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'link_text': By.LINK_TEXT,
        }
        if not all:
            return self.driver.find_element(dic[method], args)
        return self.driver.find_elements(dic[method], args)

    def find_all(self, method, args):
        return self.find(method, args, all=True)
