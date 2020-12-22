import re
import requests
import lxml.html
import asyncio

from multiprocessing import Pool
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep

from locators import *
from my_config import *

import sys
sys.path.append('..')
from logger_config import get_logger
from webdriver import Webdriver


logger = get_logger('webdriver.yelp')


ua = UserAgent()

_found = lambda loc, desc: not f'No Results for {desc}' in requests.get(yelp.format(desc, loc), headers={'User-Agent': ua.random}).text

class Yelp(Webdriver):   
    _yelp = yelp.split('search')[0] 


    async def search(self, loc=None, desc=None, url=None):
        if not '_page' in self.__dict__:
            raise ValueError('Initialize the browser before searching by `await *.init_broswser()`')
        
        if loc and desc and not url:
            if _found(loc, desc):
                logger.debug('Working based on location `%s` and keyword `%s`', loc, desc)
                self._data = [desc, loc]
                await self._locate()
            else:
                raise ValueError(f'No result for `{desc}` and `{loc}`')
        
        elif not (loc and desc) and url:
            await self._jump(url, yelp_xpath)
            logger.debug('Working based on given URL `%s`', url)
        
        else:
            await self._shut_browser()
            raise ValueError('Specify only location and description or only URL for yelp page')
        
        await self._scrape()
        await self._shut_browser()
        
    async def _locate(self):
        await self._page.goto(self._yelp)
        sleep(2.5)

        inputs = await self._page.querySelectorAll(input_locator)
        for i in range(2):
            await inputs[i].click()
            sleep(0.13)
            await self._page.keyboard.type(self._data[i])

        sleep(0.21)
        await self._page.keyboard.press('Enter')

    async def _scrape(self):

        def parse(url):
            r = requests.get(url, headers={'User-Agent': ua.random})
            html = r.text
            if r.ok:
                soup = BeautifulSoup(html, 'lxml')

                try:
                    title = soup.select_one('h1').text.strip()
                except:
                    title = '-'

                try:
                    phone = soup.find(string='Phone number').next_sibling().text().strip()
                except:
                    phone = '-'

                try:
                    addr = soup.find(string='Get Directions').next_sibling().text.strip()
                except:
                    addr = '-'
                try:
                    website = soup.find(attrs={'rel':'noopener'})['href'].split('/biz_redir?url=http%3A%2F%2F')[0].split('&')[0]
                except:
                    website = '-'

                self._buf.store(dict(zip(order, [title, addr, website, phone])))
            else:
                logger.warning(f'Failed request {r} to {url}')

        def extract_urls(html):
            return ['https://www.yelp.com' + url for url in lxml.html.document_fromstring(html).xpath(urls_xpath)]


        while True:
            urls = extract_urls(await self._page.content())

            with Pool(10) as p:
                p.map(parse, urls)

            next_button = await self._page.xpath(next_xpath)
            if not next_button:
                self._buf.dump()
                break

            await next_button.click()
            sleep(2)

async def main():
    y = Yelp()
    await y.init_browser()
    await y.search('London','Sportswear')


if __name__ == '__main__':
    asyncio.run(main())
    
