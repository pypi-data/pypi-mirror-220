from datetime import datetime
import re
import time

from utils import make_dir
from scrapers.soup import Soup


class _Browser:
    def __init__(
                    self, 
                    url = '', 
                    action = '',
                    browser_driver = None,
                    dir = 'data', 
                    filename = 'webpage.html',
                    headless = False, 
                    load_page_delay = 10, 
                    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                ) -> None:
        self.url = url
        self.filename = filename
        self.dir = dir
        self.date = date
        self.load_page_delay = load_page_delay
        if browser_driver is None:
            raise NotImplementedError("You're not supposed to use this class directly")
        self.browser = browser_driver(dir=self.dir, headless=headless)
        self.soup = None

        self.start()

        if action == 'auto_download_and_exit':
            self.auto_download_and_exit()
        elif self.url != '':
            self.open(url)

    def fix_url(self, url):
        return 'https://' + url if not re.search('http(s|)://', url) else url

    def start(self):
        self.browser.start()

    def start_headless(self):
        self.browser.start_headless()

    def quit(self):
        if self.browser.driver.service.is_connectable():
            self.browser.quit()

    def open(self, url):
        self.browser.driver.get(self.fix_url(url))
        self.soup = Soup(self.browser.driver.page_source)

    def wait(self):
        time.sleep(self.load_page_delay)

    def save(self):
        make_dir(dir_name=self.dir)
        with open(f'{self.dir}/{self.filename}', 'w', encoding="utf-8") as file:
            file.write(self.browser.driver.page_source)

    def find(self, method, args):
        self.browser.driver.find(method, args)

    def auto_download_and_exit(self):
        self.open(self.url)
        self.wait()
        self.save()
        self.quit()
