import re

import asyncio

from locators import *

from time import sleep
from bs4 import BeautifulSoup

import sys
sys.path.append('..')
from webdriver import Webdriver
from logger_config import get_logger
from my_config import *


logger = get_logger('webdriver.google_maps')


class GoogleMaps(Webdriver):



    async def search(self, location=None, keyword=None, url=None):
        if not 'page' in self.__dict__:
            raise ValueError('Initialize the browser before searching by `await *.init_broswser()`')
        if location and keyword and not url:
            logger.debug(
                'Working based on location `%s` and keyword `%s`', location, keyword)
            self._location = location
            self._keyword = keyword
            await self._locate()
        elif not (location and keyword) and url:
            logger.debug('Working based on given URL `%s`', url)
            await self._jump(url, search_xpath)
        else:
            await self._shut_browser()
            raise ValueError(
                f'Specify location and keyword. Otherwise, specify URL only. Got location `{location}`, keyword `{keyword}` and URL `{url}`')
        await self._scrape()
        await self._shut_browser()

    async def _locate(self):
            # Go to google maps, type the location
        await self._page.goto(google_maps)
        await self._page.click('input')
        await self._enter(self._location)
        await self._page.waitForXPath(button_xpath, {'visible': True})

        # Click search nearby, type the keyword
        await (await self._page.xpath(button_xpath))[2].click()
        await self._page.waitForXPath(search_xpath)
        await self._page.click('input')
        await self._enter(self._keyword)

        await self._page.waitForXPath(result_xpath, {'visible': True})


    async def _scrape(self):
        while True:
            places = len(await self._page.xpath(result_xpath))
            logger.debug('%s places found', places)

            for i in range(places):
                logger.debug('Gonna scrape %s out of %s', i + 1, places)

                place = (await self._page.xpath(result_xpath))[i]
                await self._do_retry(place.click, place_xpath)

                data = self._extract(await self._page.content())
                self._buf.store(data)

                back = (await self._page.xpath(back_xpath))[0]
                await self._do_retry(back.click, result_xpath)

            next_button = (await self._page.xpath(next_xpath))[0]
            if not next_button:
                self._buf.dump()
                break
            await next_button.click()
            sleep(1)

    def _extract(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        data = {}

        for field, src in order.items():
            try:
                if src:
                    value = soup.find(
                        attrs={'src': re.compile(src)}).parent.parent.parent.text.strip()
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


async def main():
    g = GoogleMaps()
    await g.init_browser(headless=True)
    await g.search('Кокшетау','Спортзал')    



if __name__ == '__main__':
    asyncio.run(main())