import re

from locators import *
from config import *

from bs4 import BeautifulSoup

import sys

sys.path.append('..')
from webdriver import Webdriver
from logger_config import get_logger


logger = get_logger('webdriver.google_maps')


class Searcher(Webdriver):

    def __init__(self):
        pass

    async def search(self, location=None, keyword=None, url=None):
        if location and keyword and not url:
            logger.debug(
                'Working based on location `%s` and keyword `%s`', location, keyword)
            self._location = location
            self._keyword = keyword
            await self._locate()
        elif not (location and keyword) and url:
            logger.debug('Working based on given URL `%s`', url)
            self._url = url
            await self._jump()
        else:
            await self._shut_browser()
            raise ValueError(
                f'Specify location and keyword. Otherwise, specify URL only. Got location `{location}`, keyword `{keyword}` and URL `{url}`')

        await self._scrape()
        await self._shut_browser()

    async def _locate(self):
        async def _enter(word):
            await self.page.keyboard.type(word)
            await self.page.keyboard.press('Enter')

        # Go to google maps, type the location
        await self.page.goto(google_maps)
        await self.page.click('input')
        await _enter(self._location)
        await self.page.waitForXPath(button_xpath, {'visible': True})

        # Click search nearby, type the keyword
        await (await self.page.xpath(button_xpath))[2].click()
        await self.page.waitForXPath(search_xpath)
        await self.page.click('input')
        await _enter(self._keyword)

        await self.page.waitForXPath(result_xpath, {'visible': True})

    async def _jump(self):
        try:
            await self.page.goto(self._url)
            logger.debug('Validating given URL')
            self.page.waitForXPath(check_xpath, {'visible': True})
        except:
            await self._shut_browser()
            raise ValueError('Got invalid URL for google maps')

    async def _scrape(self):
        while True:
            places = len(await self.page.xpath(result_xpath))
            logger.debug('%s places found', places)

            for i in range(places):
                logger.debug('Gonna scrape %s out of %s', i + 1, places)

                place = (await self.page.xpath(result_xpath))[i]
                await self._do_retry(place.click, place_xpath)

                data = self._extract(await self.page.content())
                self._buf.store(data)

                back = (await self.page.xpath(back_xpath))[0]
                await self._do_retry(back.click, result_xpath)
                # await self._do_retry(self.page.goBack, result_xpath)

            next_button = (await self.page.xpath(next_xpath))[0]
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
