import re
import requests
import lxml.html

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep

from locators import *
from config import *

import sys
sys.path.append('..')
from webdriver import Webdriver


not_found = lambda loc, desc: f'No Results for {desc}' in requests.get(url.format(desc, loc), headers={'User-Agent': ua.random}).text
ua = UserAgent()

def validate_args(func):
    
    def inner(self, loc, desc):
        if not_found(loc, desc):
            raise ValueError(f'No results for `{desc}` in `{loc}`')
        func(self, loc, desc)

    return inner


class Yelp(Webdriver):   

    @validate_args
    def __init__(self, loc, desc):
        self._loc = loc
        self._desc = desc

    async def _collect_urls(self, html):
        tree = lxml.html.document_fromstring(html)
        urls = ['https://www.yelp.com' + url for url in tree.xpath(urls_xpath)]

    async def _locate(self):
        pass

    def _extract_urls(self, html):
        soup = BeautifulSoup(html, 'lxml')


    async def scrape(self):
        # 1) Go to the yelp with given description and location
        # 2) Extract urls from each page
        # 3) Scrape each page using Pool
        # 4) Go to next page (if exists)
        # 5) Iterate it over
        while True:
            html = await self._locate()
            urls = self._extract_urls(html)
            self.page


y = Yelp('London', 'Pizza')
