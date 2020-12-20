import re
import requests

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
    
    def inner(self, loc, desc, *args, **kwargs):
        if not_found(loc, desc):
            raise ValueError(f'No results for `{desc}` in `{loc}`')
        func(self, loc, desc, *args, **kwargs)

    return inner





class Yelp(Webdriver):   

    @validate_args
    def __init__(self, loc, desc):

        self._loc = loc
        self._desc = desc
        print(self._loc, self._desc)

    


y = Yelp('London', 'Pizza')
