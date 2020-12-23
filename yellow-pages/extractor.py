import re
import lxml.html
import requests
import asyncio

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
            await self._jump(url, results_xpath)
            logger.debug('Working based on given URL `%s`', url)
        
        else:
            await self._shut_browser()
            raise ValueError('Specify only location and description or only URL for yelp page')
        
        await self._scrape()
        await self._shut_browser()
        
    async def _locate(self):
        await self._page.goto(self._yelp)
        sleep(2.5)

        inputs = await self._page.querySelectorAll(input_selector)
        for i in range(2):
            await inputs[i].click()
            sleep(0.13)
            await self._page.keyboard.type(self._data[i])
            sleep(0.21)

        await self._page.click(search_button_selector)

    async def _scrape(self):
        
        def parse(html):
            data = {}
            soup = BeautifulSoup(html, 'lxml')

            for field, cls_ in order.items():
                try:
                    if cls_:
                        value = soup.find(class_=cls_,).parent.previous_sibling().text.strip()
                    else:
                        value = soup.find('h1').text.strip()
                except:
                    value = '-'
                data.update({field: value})

            self._buf.store(data)


        while True:
            await self._page.waitForXPath(results_xpath)
            places = await self._page.xpath(places_xpath)
            
            for place in places:
                await self._page.waitForXPath(results_xpath)
                await place.click()
                await self._page.waitForXPath(inner_xpath)
                sleep(1.5)
                parse(await self._page.content())
                await self._page.goBack()

            next_button = await self._page.xpath(next_xpath)

            if not next_button:
                self._buf.dump()
                break

            await next_button[0].click()
            sleep(2)

async def main():
    y = Yelp()
    await y.init_browser()
    await y.search('London','Sportswear')


if __name__ == '__main__':
    asyncio.run(main())
    
