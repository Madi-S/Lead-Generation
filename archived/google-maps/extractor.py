#!C:/Users/DELL/AppData/Local/Programs/Python/Python312/python
import re
import asyncio
from playwright.async_api import async_playwright
from logger_config import get_logger
from locators import *
from my_config import *
from time import sleep
from random import uniform
from bs4 import BeautifulSoup
import sys
import csv

sys.path.append('..')

logger = get_logger('playwright.google_maps')

class GoogleMaps:
    def __init__(self):
        self.browser = None
        self.page = None

    async def init_browser(self, hidden=True):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=hidden)
        self.page = await self.browser.new_page()

    async def search(self, location, keyword, zoom_level):
        if not self.page:
            raise ValueError('Initialize the browser before searching by `await *.init_browser()`')

        logger.debug('Working based on location `%s` and keyword `%s`', location, keyword)
        self._location = location
        self._keyword = keyword
        self._zoom_level = zoom_level
        await self._locate()

        await self._scrape()
        await self._shut_browser()

    async def _locate(self):
        async def _enter(word):
            await self.page.keyboard.type(word)
            await self.page.keyboard.press('Enter')

        try:
            await self.page.goto(google_maps)
            await self.page.click('input')
            await _enter(self._location)
            await self.page.wait_for_selector(button_xpath, state='visible')
            await (await self.page.query_selector_all(button_xpath))[2].click()
            await self.page.wait_for_selector(search_xpath)
            await self.page.click('input')
            await _enter(self._keyword)
            await self.page.wait_for_selector(result_xpath, state='visible')
        except Exception as e:
            logger.warning('Error during _locate: %s', e)
            await self._shut_browser()

    async def _scrape(self):
        def extract(html):
            soup = BeautifulSoup(html, 'html.parser')
            data = {}
            try:
                name = soup.find('h1').text.strip()
                data['Name'] = name
            except:
                data['Name'] = '-'

            try:
                phone = soup.find(attrs={'data-tooltip': re.compile('Phone')}).parent.text.strip()
                data['Phone'] = phone
            except:
                data['Phone'] = '-'

            try:
                address = soup.find(attrs={'data-tooltip': re.compile('Address')}).parent.text.strip()
                data['Address'] = address
            except:
                data['Address'] = '-'

            try:
                location = soup.find('meta', attrs={'itemprop': 'image'})['content']
                data['Location'] = location
            except:
                data['Location'] = '-'

            logger.debug('Data: %s', list(data.values()))
            return data

        results = []
        while True:
            places = len(await self.page.query_selector_all(result_xpath))
            logger.debug('%s places found', places)

            for i in range(places):
                try:
                    logger.debug('Gonna scrape %s out of %s', i + 1, places)
                    place = (await self.page.query_selector_all(result_xpath))[i]
                    await self._do_retry(place.click, place_xpath)

                    data = extract(await self.page.content())
                    results.append(data)

                    back = (await self.page.query_selector_all(back_xpath))[0]
                    await self._do_retry(back.click, result_xpath)
                except Exception as e:
                    logger.warning('Error occurred: %s', e)

            next_button = (await self.page.query_selector_all(next_xpath))[0]
            if not next_button:
                break
            await next_button.click()
            sleep(uniform(0.7, 1))

        self._save_results(results)

    async def _shut_browser(self):
        if self.browser:
            await self.browser.close()
        self.page = None
        self.browser = None

    async def _do_retry(self, action, *args):
        for _ in range(3):  # Retry up to 3 times
            try:
                await action(*args)
                break
            except Exception as e:
                logger.warning('Retrying due to error: %s', e)
                await asyncio.sleep(2)  # Wait before retrying

    def _save_results(self, results):
        keys = results[0].keys()
        with open('google_maps_results.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

async def main():
    location = input("Enter the keyword of Your Search: ")
    keyword = input("Enter the City: ")
    zoom_level = input("Enter the zoom level of Google Maps: ")

    g = GoogleMaps()
    await g.init_browser(hidden=False)
    await g.search(location, keyword, zoom_level)

if __name__ == '__main__':
    asyncio.run(main())
