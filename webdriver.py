import asyncio

import csv
import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyppeteer import launch
from time import sleep


URL = 'https://www.google.ru/maps'
ua = UserAgent()

button_xpath = '//*[@class="iRxY3GoUYUY__button gm2-hairline-border section-action-chip-button"]'
search_xpath = '//*[@role="gridcell"]'
wait_xpath = '//*[@jstcache="1098"]'
next_xpath = '//*[contains(@src, "chevron_right_black_24dp.png")]'


class Webdriver:

    order = {
        'Title': None,
        'Address': re.compile(r'(place_gm_blue_24dp.png)'),
        'WebSite': re.compile(r'(public_gm_blue_24dp.png)'),
        'PhoneNumber': re.compile(r'(phone_gm_blue_24dp.png)')
    }

    viewport = {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1.0,
                'isMobile': False, 'hasTouch': False, 'isLandscape': False}

    def __init__(self, filename='leads.csv',newline=''):
        if not filename.endswith('.csv'):
            raise ValueError(
                'Incorrect filename specified. Filename should end with `.csv`')
        self._filename = filename
        with open(self._filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.order.keys()))
            writer.writeheader()

    async def init_browser(self):
        self.browser = await launch(
            ignoreHTTPSErrors=True,
            headless=False,
            # slowMo=30,
            autoclose=True,
        )
        # self.browser.setUserAgent(ua.random)

    async def locate(self, location, keyword):
        async def enter(word):
            await self.page.keyboard.type(word)
            await self.page.keyboard.press('Enter')

        self.page = (await self.browser.pages())[0]

        # await self.page.setViewport(self.viewport)
        await self.page.setUserAgent(ua.random)
        await self.page.reload()
        await self.page.goto(URL)

        await enter(location)

        await self.page.waitForXPath(button_xpath)
        button = (await self.page.xpath(button_xpath))[2]
        await button.click()

        await self.page.waitForXPath(search_xpath)
        await enter(keyword)

        await self.scrape()

        sleep(100)
        await self.page.close()
        await self.browser.close()

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

                #await asyncio.wait([
                #    element.click(),
                #    self.page.waitForNavigation()
                #])

                await element.click()
                await self.page.waitForNavigation()

                data = self.extract(await self.page.content())
                self.store(data)

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

        # info = soup.select_one('.ugiz4pqJLAG__primary-text gm2-body-2')
        data = {}
        dict()

        for field, src in self.order.items():
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

    def store(self, data):
        with open('leads.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.order.keys()))
            writer.writerow(data)


async def main():
    w = Webdriver()
    await w.init_browser()
    await w.locate('Moscow', 'Cafe')


asyncio.run(main())
