import os
from bs4 import BeautifulSoup

from job import Chrome, Firefox

class Webpage:
    def __init__(
                    self, 
                    url, 
                    action = 'start',
                    browser = 'chrome',
                    filename = 'webpage.html',
                    dir = 'data', 
                    hide_browser = True, 
                    load_page_delay = 10,
                    # find_element = [],
                    # single_element = False
                ):
        self.url = url
        self.dir = dir
        self.browser = self.determine_browser(browser, action, hide_browser, load_page_delay)
        self.filename = filename
        self.full_path = f'{self.dir}/{self.filename}'
        # self.find_element = find_element
        # self.single_element = single_element
        self.raw_html_content = self.open_file()
        self.html_content = self.parse_file()

    def determine_browser(self, browser, action, hide_browser, load_page_delay):
        if browser == 'chrome':
            return Chrome(self.url, action=action, dir=self.dir, filename=self.filename, headless=hide_browser, load_page_delay=load_page_delay)
        elif browser == 'firefox':
            return Firefox(self.url, action=action, dir=self.dir, filename=self.filename, headless=hide_browser, load_page_delay=load_page_delay)


    def downloaded_file(self) -> str:
        try:
            file = os.listdir(self.dir)
            return file[0]
        except FileNotFoundError:
            return None

    def file_exists(self):
        return os.path.isfile(self.full_path)

    def open_file(self) -> object:
        file = self.downloaded_file()
        if file and file == self.filename:
            with open(self.full_path, 'r', encoding="utf-8") as html:
                return BeautifulSoup(html, 'html.parser')
        print("You need to download a webpage first")

    def parse_file(self):
        content = self.open_file()
        if isinstance(self.find_element, list) and self.find_element:
            if self.single_element:
                result = content.find_all(self.find_element[0])
            elif len(self.find_element) == 3:
                result = content.find(self.find_element[0], (self.find_element[1], self.find_element[2]))
            elif len(self.find_element) == 2:
                result = content.find(self.find_element[0], (self.find_element[1]))
            if not result:
                print("BS4 didn't find any matches")
            return result
        else:
            return content
