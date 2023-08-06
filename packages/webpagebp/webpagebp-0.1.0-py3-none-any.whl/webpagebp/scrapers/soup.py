from typing import List
from bs4 import BeautifulSoup


class Soup:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def find(self, arguments: List):
        """Returns first result for matching criteria"""
        if len(arguments) == 1:
            return self.soup.find(arguments[0])
        elif len(arguments) == 3:
            return self.soup.find(arguments[0], (arguments[1], arguments[2]))
        else:
            raise ValueError("Arguments must be either 1 or 3")

    def find_all(self, arguments: List):
        """Returns all results for matching criteria"""
        if len(arguments) == 1:
            return self.soup.find_all(arguments[0])
        elif len(arguments) == 3:
            return self.soup.find_all(arguments[0], (arguments[1], arguments[2]))
        else:
            raise ValueError("Arguments must be either 1 or 3")
