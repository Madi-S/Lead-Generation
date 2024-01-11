import json
import asyncio
import requests
from logger_config import get_logger
from webdriver import Webdriver

from pyppeteer.errors import TimeoutError

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from random import uniform
from time import sleep

from locators import *
from my_config import *

import sys
sys.path.append('..')


logger = get_logger('webdriver.yelp')
ua = UserAgent()


def _found(loc, desc): return not f'No Results for {desc}' in requests.get(
    yelp.format(desc, loc), headers={'User-Agent': ua.random}).text


class Yelp(Webdriver):
    _yelp = yelp.split('search')[0]

    async def search(self, loc=None, desc=None, url=None):
        '''

        :param desc: Description to generate leads (e.g., 'Sportswear') 
        :param loc: Location to search (e.g., 'London')
        :param url: Direct URL to yelp results page. Must be specified without `desc` and `loc` 
        :return: returns nothing
        '''
        if not '_page' in self.__dict__:
            raise ValueError(
                'Initialize the browser before searching by `await *.init_broswser()`')

        if loc and desc and not url:
            if _found(loc, desc):
                logger.debug(
                    'Working based on location `%s` and keyword `%s`', loc, desc)
                self._data = [desc, loc]
                await self._locate()
            else:
                raise ValueError(f'No result for `{desc}` and `{loc}`')

        elif not (loc and desc) and url:
            await self._jump(url, results_xpath)
            logger.debug('Working based on given URL `%s`', url)

        else:
            await self._shut_browser()
            raise ValueError(
                'Specify only location and description or only URL for yelp page')

        await self._scrape()
        await self._shut_browser()

    async def _locate(self):
        await self._page.goto(self._yelp)
        sleep(uniform(2.5, 3.5))

        inputs = await self._page.querySelectorAll(input_selector)
        for i, inp in enumerate(inputs[:2]):
            await inp.click()
            sleep(uniform(0.1, 0.2))
            await self._page.keyboard.type(self._data[i])
            sleep(uniform(0.2, 0.26))

        await self._page.click(search_button_selector)

    async def _scrape(self):

        def parse(html):
            soup = BeautifulSoup(html, 'html.parser')

            try:
                raw_data = json.loads(
                    soup.find('script', attrs=json_attrs).string)
            except AttributeError:
                logger.warning(
                    'Could not locate `raw_data` skipping current page')
                return

            try:
                website = soup.find(attrs=website_attrs).text
            except:
                website = '-'

            try:
                data = {
                    'WebSite': website,
                    'Title': raw_data['name'],
                    'PhoneNumber': raw_data['telephone'],
                    'Address': ', '.join(list(raw_data['address'].values())),
                }
                logger.debug('Extracted: %s', list(data.values()))
                self._buf.store(data)
            except Exception:
                logger.warning('Exception while scraping', exc_info=True)

        sleep(uniform(2, 3))
        while True:
            try:
                await self._page.waitForXPath(places_xpath, {'visible': True})
            except TimeoutError:
                logger.debug('Next page did not yield any results -> breaking')
                break
            places = len(await self._page.xpath(places_xpath))
            logger.debug('%s places found', places)

            for i in range(places):

                place = (await self._page.xpath(places_xpath))[i]

                await place.click()
                sleep(uniform(1.7, 2))
                await self._page.waitForXPath(inner_xpath, {'visible': True})

                parse(await self._page.content())

                await self._page.goBack()
                sleep(uniform(1, 2))
                await self._page.waitForXPath(results_xpath, {'visible': True})

            next_button = await self._page.xpath(next_xpath)

            if not next_button:
                break

            await self._do_retry(next_button[0].click, results_xpath)
            sleep(uniform(1.3, 1.7))

        self._buf.dump()


async def main():
    y = Yelp()
    await y.init_browser(hidden=False)
    await y.search('London', 'Hostel')


if __name__ == '__main__':
    asyncio.run(main())
