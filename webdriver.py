import asyncio

import csv
import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyppeteer import launch
from time import sleep

from locators import *
from config import *
from logger_config import get_logger
from bufferization import Buffer


ua = UserAgent()
logger = get_logger('driver')


class Webdriver:
    viewport = {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1.0,
                'isMobile': False, 'hasTouch': False, 'isLandscape': False}

    buf = Buffer()

    async def init_browser(self, language='ru'):
        self.browser = await launch(
            ignoreHTTPSErrors=True,
            headless=False,
            # slowMo=30,
            autoclose=True,
        )
        self.page = (await self.browser.pages())[0]

        # await self.page.setViewport(self.viewport)
        await self.page.setUserAgent(ua.random)
        await self.page.setExtraHTTPHeaders({'Accept-Language': language})
        await self.page.reload()

    async def _shut_browser(self):
        await asyncio.sleep(50)
        await self.page.close()
        await self.browser.close()

    async def search(self, location=None, keyword=None, url=None):
        if location and keyword and not url:
            print(
                f'Working based on location `{location}` and keyword `{keyword}`')
            self._location = location
            self._keyword = keyword
            await self._locate()
        elif not (location and keyword) and url:
            print(f'Working based on given URL `{url}`')
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

        await self.page.goto(google_maps)
        await self.page.click('input')
        await _enter(self._location)

        await self.page.waitForXPath(button_xpath, {'visible': True})
        await (await self.page.xpath(button_xpath))[2].click()
        await self.page.waitForXPath(search_xpath)
        await self.page.click('input')
        await _enter(self._keyword)

    async def _jump(self):
        try:
            await self.page.goto(self._url)
            print('Checking the given URL')
            self.page.waitForXPath(check_xpath, {'visible': True})
        except:
            await self._shut_browser()
            raise ValueError('Got invalid URL for google maps')

    async def _scrape(self):
        next_button = True
        while next_button:
            await self.page.waitForSelector(result_css, {'visible': True})

            home = self.page.url
            overall = len(await self.page.querySelectorAll(result_css))
            print(f'Overall found {overall}')

            for i in range(overall):
                print(f'Gonna scrape {i} out of {overall}')
                element = (await self.page.querySelectorAll(result_css))[i]

                await asyncio.wait([
                    element.click(),
                    self.page.waitForNavigation()
                ])
                sleep(0.5)

                data = self._extract(await self.page.content())
                self.buf.store(data)

                await asyncio.wait([
                    self.page.goto(home),
                    self.page.waitForNavigation()
                ])
                sleep(0.5)

            next_button = (await self.page.xpath(next_xpath))[0]
            await next_button.click()

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
            except:
                value = None
            data.update({field: value})

        print(data)
        return data

    async def _scrape_pages(self):
        pass


async def main():
    w = Webdriver()
    await w.init_browser()
    await w.search('Кокшетау', 'Спортзал')


asyncio.run(main())
