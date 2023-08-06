from pathlib import Path
from typing import List

from webpagebp.utils import make_dir
from webpagebp.browsers import ChromeBrowser, ChromeHBrowser, FirefoxBrowser, FirefoxHBrowser


class DefaultJob:
    def __init__(self, url: str, browser: str=ChromeHBrowser, file='webpage.html', dir='data', load_page_delay=10, *args, **kwargs) -> None:
        self.url = url,
        self.file = file
        self.dir = dir
        # self.dir = Path(dir)
        self.load_page_delay = load_page_delay
        self.browser = browser(url=url, file=file, dir=dir, load_page_delay=load_page_delay, *args, **kwargs)

    def save(self, file=None, dir=None):
        dir = dir if dir else self.dir
        filename = file if file else self.filename
        make_dir(dir_name=dir)
        with open(f'{dir}/{filename}', 'w', encoding="utf-8") as file:
            file.write(self.browser.browser.driver.page_source)
        print(f"Saving to ./{dir}/{filename}..")

    def quit(self):
        self.browser.quit()


class FindAll(DefaultJob):
    def __init__(self, url: str, find_all: List, *args, **kwargs) -> None:
        super().__init__(url, browser=ChromeHBrowser, *args, **kwargs)
        self.result = self.browser.soup.find_all(find_all)


class ReadFile(DefaultJob):
    def __init__(self, file: str, *args, **kwargs) -> None:
        super().__init__(url='', browser=ChromeHBrowser, action='exit', *args, **kwargs)
        self.result = self.browser.open_file(file)


class Download(DefaultJob):
    def __init__(self, url: str, *args, **kwargs) -> None:
        super().__init__(url, browser=ChromeHBrowser, action='auto_download_and_exit', *args, **kwargs)


class Chrome(DefaultJob):
    def __init__(self, url: str, *args, **kwargs) -> None:
        super().__init__(url, browser=ChromeBrowser, *args, **kwargs)


class ChromeH(DefaultJob):
    def __init__(self, url: str, *args, **kwargs) -> None:
        super().__init__(url, browser=ChromeHBrowser, *args, **kwargs)


class Firefox(DefaultJob):
    def __init__(self, url: str, *args, **kwargs) -> None:
        super().__init__(url, browser=FirefoxBrowser, *args, **kwargs)


class FirefoxH(DefaultJob):
    def __init__(self, url: str, *args, **kwargs) -> None:
        super().__init__(url, browser=FirefoxHBrowser, *args, **kwargs)

