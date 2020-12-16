import asyncio

import csv
import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyppeteer import launch
from time import sleep


google_maps = 'https://www.google.ru/maps'
ua = UserAgent()

button_xpath = '//*[@class="iRxY3GoUYUY__button gm2-hairline-border section-action-chip-button"]'
search_xpath = '//*[@role="gridcell"]'
wait_xpath = '//*[@jstcache="1098"]'
next_xpath = '//*[contains(@src, "chevron_right_black_24dp.png")]'


order = {
    'Title': None,
    'Address': re.compile(r'(place_gm_blue_24dp.png)'),
    'WebSite': re.compile(r'(public_gm_blue_24dp.png)'),
    'PhoneNumber': re.compile(r'(phone_gm_blue_24dp.png)')
}


class Buffer:
    lower_limit = 20
    upper_limit = 201
    fn = list(order.keys())

    def __init__(self, filename: str = 'leads.csv', buffer_size: int = 20):
        if not filename.endswith('.csv'):
            raise ValueError(
                'Incorrect filename specified. Filename should end with `.csv`')
        if not buffer_size in range(self.lower_limit, self.upper_limit):
            raise ValueError(
                f'Expected value between {self.upper_limit} and {self.upper_limit}. However, got {buffer_size}')

        self._buffer_size = buffer_size
        self._filename = filename
        self._data = []

        with open(self._filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fn)
            writer.writeheader()

    def _dump(self):
        with open('leads.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fn)
            for d in self._data:
                writer.writerow(d)

    def __iadd__(self, other: dict):
        self._data.append(dict)
        if self._data >= self._buffer_size:
            self._dump()


class Webdriver:
    viewport = {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1.0,
                'isMobile': False, 'hasTouch': False, 'isLandscape': False}

    buffer = Buffer()

    async def init_browser(self):
        self.browser = await launch(
            ignoreHTTPSErrors=True,
            headless=False,
            # slowMo=30,
            autoclose=True,
        )

    async def search(self, location=None, keyword=None, url=None):
        if location and keyword and not url:
            print(
                f'Working based on location {location} and keyword {keyword}')
            self._location = location
            self._keyword = keyword
            await self._locate()
        elif not (location and keyword) and url:
            print(f'Working based on given URL {url}')
            self._url = url
            await self._jump()
        else:
            raise ValueError(
                f'Specify location and keyword. Otherwise, specify URL only. Got location {location}, keyword {keyword} and URL {url}')

        await self.scrape()

        sleep(100)
        await self.page.close()
        await self.browser.close()

    async def _enter(self, word):
        await self.page.keyboard.type(word)
        await self.page.keyboard.press('Enter')

    async def _locate(self):
        self.page = (await self.browser.pages())[0]

        # await self.page.setViewport(self.viewport)
        await self.page.setUserAgent(ua.random)
        await self.page.reload()
        await self.page.goto(google_maps)

        await self._enter(self._location)

        await self.page.waitForXPath(button_xpath)
        button = (await self.page.xpath(button_xpath))[2]
        await button.click()

        await self.page.waitForXPath(search_xpath)
        await self._enter(self._keyword)

    async def _jump(self):
        await self.page.goto(self._url)

    async def scrape(self):
        next_button = True
        while next_button:
            await self.page.waitForSelector('.section-result-content')

            home = self.page.url
            overall = len(await self.page.querySelectorAll('.section-result-content'))
            print(f'Overall found {overall}')

            for i in range(overall):
                print(f'Gonna scrape {i} out of {overall}')
                element = (await self.page.querySelectorAll('.section-result-content'))[i]

                # await asyncio.wait([
                #    element.click(),
                #    self.page.waitForNavigation()
                # ])

                await element.click()
                await self.page.waitForNavigation()

                data = self.extract(await self.page.content())
                buffer += data

                # await asyncio.wait([
                #     self.page.goto(home),
                #     self.page.waitForNavigation()
                # ])

                await self.page.goto(home)
                await self.page.waitForNavigation()
                sleep(1.5)

            next_button = (await self.page.xpath(next_xpath))[0]
            await next_button.click()

    def extract(self, html):
        soup = BeautifulSoup(html, 'lxml')

        data = {}

        for field, src in order.items():
            try:
                if src:
                    value = soup.find(
                        attrs={'src': src}).parent.parent.parent.text.strip()
                else:
                    value = soup.select('h1')[0].text.strip()
            except:
                value = None
            data.update({field: value})

        print(data)
        return data


async def main():
    w = Webdriver()
    await w.init_browser()
    await w.search('Calgary', 'Thai food')


asyncio.run(main())
