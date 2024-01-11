import asyncio
from webdriver import Webdriver
from logger_config import get_logger

from locators import *
from my_config import *

from os import environ
from time import sleep
from random import uniform, randint
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


import sys
sys.path.append('..')


logger = get_logger('webdriver.linkedin')

ua = UserAgent()


class LinkedIn(Webdriver):

    def __init__(self, email=None, pwd=None):
        if not (email and pwd):
            try:
                self.email = environ.get('linkedin_mail')
                self.pwd = environ.get('linkedin_pwd')
            except:
                logger.fatal(
                    'Cannot get email and password to login in LinkedIn account', exc_info=True)
        else:
            logger.warning(
                'Specify email and pwd as local variables `linkedin_mail` and `linkedin_pwd` for your privacy')
            self.email = email
            self.pwd = pwd

    async def login(self):
        await self._page.goto(linkedin_link)
        sleep(uniform(1.7, 3.4))
        await asyncio.wait([
            self._page.click(
                login_locator, {'button': 'left', 'delay': uniform(50, 100)}),
            self._page.waitForNavigation()
        ])

        sleep(uniform(1.7, 3.4))
        await self.type_(self.email)

        await self._page.click(pwd_locator)
        sleep(uniform(0.3, 0.9))
        await self.type_(self.pwd)

        if randint(0, 1) == 0:
            sleep(0.1, 0.5)
            await self._page.click(show_pwd_locator)

        sleep(uniform(2, 5))

    async def search_title(self, title):
        # await self._page.click(search_locator)
        # sleep(uniform(2, 3))

        # await self.type_(title)
        # sleep(uniform(0.5, 1))

        # await self._page.keyboard.press('Enter')
        # sleep(uniform(2,5))

        # select_bar = (await self._page.xpath(select_bar_xpath))[0]
        # await select_bar.click()

        await self._page.goto(f'https://www.linkedin.com/search/results/companies/?keywords={title}&origin=GLOBAL_SEARCH_HEADER')
        companies = await self._page.querySelectorAll(companies_locator)

        if not companies:
            return 'Nothing Found'

        await companies[0].click()

    async def open_members(self):
        pass

    def break_title(self, title):
        return

    def find_head(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        position = soup.find(string=head_regex)
        name = position.parent.parent.parent.find(
            attrs={'aria-hidden': True}).text

        return (position, name)

    async def use_module(self):
        pass

    async def type_(self, string):
        for letter in string:
            self._page.keyboard.type(letter)
            sleep(uniform(0.1, 0.3))

    async def behave_like_human(self):
        pass
