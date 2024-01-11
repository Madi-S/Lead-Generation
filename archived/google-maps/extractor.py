import re
import asyncio
from webdriver import Webdriver
from logger_config import get_logger

from locators import *
from my_config import *

from time import sleep
from random import uniform
from bs4 import BeautifulSoup

from pyppeteer.errors import PageError

import sys
sys.path.append('..')


logger = get_logger('webdriver.google_maps')


class GoogleMaps(Webdriver):

    async def search(self, location=None, keyword=None, url=None):
        '''

        :param desc: Description to generate leads (e.g., 'Pizza Delivery') 
        :param loc: Location to search (e.g., 'California')
        :param url: Direct URL to yelp results page. Must be specified without `desc` and `loc` 
        :return: returns nothing
        '''

        if not '_page' in self.__dict__:
            raise ValueError(
                'Initialize the browser before searching by `await *.init_broswser()`')

        if location and keyword and not url:
            logger.debug(
                'Working based on location `%s` and keyword `%s`', location, keyword)
            self._location = location
            self._keyword = keyword
            await self._locate()

        elif not (location and keyword) and url:
            await self._jump(url, search_xpath)
            logger.debug('Working based on given URL `%s`', url)

        else:
            await self._shut_browser()
            raise ValueError(
                f'Specify location and keyword. Otherwise, specify URL only. Got location `{location}`, keyword `{keyword}` and URL `{url}`')

        await self._scrape()
        await self._shut_browser()

    async def _locate(self):
        async def _enter(word):
            await self._page.keyboard.type(word)
            await self._page.keyboard.press('Enter')

        try:
            await self._page.goto(google_maps)
            await self._page.click('input')
            await _enter(self._location)
            sleep(2.5)

            await self._page.waitForXPath(button_xpath, {'visible': True})
            await (await self._page.xpath(button_xpath))[2].click()
            await self._page.waitForXPath(search_xpath)
            await self._page.click('input')
            await _enter(self._keyword)

            await self._page.waitForXPath(result_xpath, {'visible': True})
        except PageError:
            self._page.reload()
            self._locate()

    async def _scrape(self):

        def extract(html):
            soup = BeautifulSoup(html, 'html.parser')

            data = {}

            for field, src in order.items():
                try:
                    if src:
                        value = soup.find(attrs={'src': re.compile(
                            src)}).parent.parent.parent.text.strip()
                    else:
                        value = soup.find('h1').text.strip()
                    if 'Add' in value or 'Добавить' in value:
                        logger.debug('Got empty information %s', value)
                        value = '-'
                except:
                    value = '-'
                data.update({field: value})

            logger.debug('Data: %s', list(data.values()))
            return data

        while True:
            places = len(await self._page.xpath(result_xpath))
            logger.debug('%s places found', places)

            for i in range(places):
                try:
                    logger.debug('Gonna scrape %s out of %s', i + 1, places)

                    place = (await self._page.xpath(result_xpath))[i]
                    await self._do_retry(place.click, place_xpath)

                    data = extract(await self._page.content())
                    self._buf.store(data)

                    back = (await self._page.xpath(back_xpath))[0]
                    await self._do_retry(back.click, result_xpath)
                except:
                    logger.warning('Error occured', exc_info=True)

            next_button = (await self._page.xpath(next_xpath))[0]
            if not next_button:
                break
            await next_button.click()
            sleep(uniform(0.7, 1))

        self._buf.dump()


async def main():
    g = GoogleMaps()
    await g.init_browser(hidden=False)
    await g.search('Nur-Sulatn', 'Hotel')


if __name__ == '__main__':
    asyncio.run(main())
