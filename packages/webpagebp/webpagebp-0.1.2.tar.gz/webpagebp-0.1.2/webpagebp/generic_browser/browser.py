from datetime import datetime
import re
import time

from webpagebp.utils import make_dir, html_from_file
from webpagebp.scrapers.soup import Soup


class _Browser:
    def __init__(
                    self, 
                    url = '', 
                    dir = 'data',
                    file = 'webpage.html',
                    action = '',
                    browser_driver = None,
                    load_page_delay = 10, 
                    date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                    *args,
                    **kwargs
                ) -> None:
        self.url = url
        self.dir = dir
        self.file = file
        self.date = date
        self.load_page_delay = load_page_delay
        if browser_driver is None:
            raise NotImplementedError("You're not supposed to use this class directly")
        self.browser = browser_driver(*args, **kwargs)
        self.soup = None

        self.start()

        if action == 'auto_download_and_exit':
            self.auto_download_and_exit()
            self.quit()
        elif action == 'exit':
            self.quit()
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

    def open(self, url, soup: Soup = Soup):
        self.browser.driver.get(self.fix_url(url))
        self.soup = soup(self.browser.driver.page_source)

    def open_file(self, file):
        return html_from_file(file)

    def wait(self):
        time.sleep(self.load_page_delay)

    def save(self, file=None, dir=None):
        dir = dir if dir else self.dir
        filename = file if file else self.file
        make_dir(dir_name=dir)
        with open(f'{dir}/{filename}', 'w', encoding="utf-8") as file:
            file.write(self.browser.driver.page_source)
        print(f"Saving to ./{dir}/{filename}..")

    def find(self, method, args):
        self.browser.driver.find(method, args)

    def auto_download_and_exit(self):
        self.open(self.url)
        self.wait()
        self.save()
        self.quit()
