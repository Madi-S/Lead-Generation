import re
import requests
import lxml.html

from multiprocessing import Pool
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep

from locators import *
from config import *

import sys
sys.path.append('..')
from my_config import 
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

    async def _extract_urls(self, html):
        return ['https://www.yelp.com' + url for url in lxml.html.document_fromstring(html).xpath(urls_xpath)]

    async def _locate(self):
        self._page.goto()

    def _parse(self, html):
        soup = BeautifulSoup(html, 'lxml')

        try:
            title = soup.select_one('h1').text.strip()
        except:
            title = '-'

        try:
            phone = soup.find(string='Phone number').next_sibling().text().strip()
        except:
            phone = '-'

        try:
            addr = soup.find(string='Get Directions').next_sibling().text.strip()
        except:
            addr = None
        try:
            website = soup.find(attrs={'rel':'noopener'})['href'].split('/biz_redir?url=http%3A%2F%2F')[0].split('&')[0]
        except:
            website = None

        return dict(zip(order, [title, addr, website, phone]))

    async def scrape(self):
        # 1) Go to the yelp with given description and location
        # 2) Extract urls from each page
        # 3) Scrape each page using Pool
        # 4) Go to next page (if exists)
        # 5) Iterate it over
        while True:
            html = await self._locate()
            urls = self._extract_urls(html)
            with Pool(10) as p:
                p.map(self._parse, urls)


y = Yelp('London', 'Pizza')
