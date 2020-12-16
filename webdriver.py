import asyncio

import csv
import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyppeteer import launch
from time import sleep


URL = 'https://www.google.ru/maps'
ua = UserAgent()
css_selector = '.section-action-chip-button:nth-of-type(3)'  # third button
css_parent = '.section-layout-justify-space-between:nth-child(3) .section-action-chip-button'
# section-layout section-layout-justify-space-between section-layout-flex-vertical section-layout-flex-horizontal
xpath = '//*[@id="pane"]/div/div[1]/div/div/div[5]/div[3]/div/button'


class Webdriver:

    order = {
        'Title': None,
        'Address': re.compile(r'(place_gm_blue_24dp.png)'),
        'WebSite': re.compile(r'(public_gm_blue_24dp.png)'),
        'PhoneNumber': re.compile(r'(phone_gm_blue_24dp.png)')
    }

    def __init__(self, filename='leads.csv'):
        if not filename.endswith('.csv'):
            raise ValueError(
                'Incorrect filename specified. Filename should end with `.csv`')
        self._filename = filename
        with open(self._filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.order.keys()))
            writer.writeheader()

        # self.browser = await launch(
        #    ignoreHTTPSErrors=True,
        #    headless=False,
        #    # slowMo=300,
        #    # userDatadir='C:\\Users\\khova\\AppData\\Local\\Google\\Chrome\\User Data',
        #    # autoclose=False,
        # )

    async def locate(self, city, keyword):
        self.page = await self.browser.newPage()

        await self.page.setUserAgent(ua.random)
        await self.page.goto(URL)

        await self.page.keyboard.type(city)
        await self.page.keyboard.press('Enter')

        await self.page.waitForXPath(xpath)
        button = await self.page.xpath(xpath)[0]
        await button.click()

        # sleep(100)
        # await self.page.close()
        # await browser.close()

    async def scrape(self):
        elements = await self.page.querySelectorEval('.section-result-content')
        while elements:
            element = elements.pop()

            await asyncio.wait([
                element.click(),
                self.page.waitForNavigation()
            ])

            data = self.extract(await self.page.content())
            self.store(data)

    def extract(self, html=open('test.html', encoding='utf-8')):
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
        with open('leads.csv', 'a', encoding='utf-8') as csv_file:
            csv_file.write(data)


async def main():
    w = Webdriver()
    w.extract()
    # await w.locate('Moscow', 'Night clubs')


asyncio.run(main())
