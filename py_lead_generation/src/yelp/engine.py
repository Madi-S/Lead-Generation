import time
import asyncio
from bs4 import BeautifulSoup

from py_lead_generation.src.engines.base import BaseEngine
from py_lead_generation.src.engines.abstract import AbstractEngine


class YelpEngine(BaseEngine, AbstractEngine):
    '''
    `YelpEngine`

    Usage:

    `engine = YelpEngine(*args, **kwargs)`

    `await engine.run()`

    `await engine.save_to_csv()`

    `print(engine.entries)`
    '''

    BASE_URL = 'https://www.yelp.com/search?find_desc={query}&find_loc={location}%2C+Philippines&start=0'
    FIELD_NAMES = ['Title', 'Address', 'PhoneNumber', 'Tags']
    FILENAME = 'yelp_leads.csv'

    def __init__(self, query: str, location: str) -> None:
        '''
        '''
        self._entries = []
        self.query = query
        self.location = location
        self.url = self.BASE_URL.format(
            query=self.query, location=self.location
        )

    async def _get_search_results_urls(self) -> list[str]:
        '''
        '''
        urls = []
        host = 'https://www.yelp.com'
        while True:
            await asyncio.sleep(3)
            link_elements = await self.page.query_selector_all('.css-1hqkluu')
            for link_element in link_elements:
                url = await link_element.get_attribute('href')
                url = host + url
                urls.append(url)

            next_page_btn = await self.page.query_selector(
                '.next-link.navigation-button__09f24__m9qRz.css-ahgoya'
            )
            if not next_page_btn:
                break

            await next_page_btn.scroll_into_view_if_needed()
            await next_page_btn.click()

        return urls

    def _parse_data_with_soup(self, html: str) -> list[str]:
        '''
        `html: str` - html representation of the page to parse

        Returns `list[str]` typed parsed data - `[title, addr, phone, tags]`
        '''
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        title_selector = '.css-1se8maq'
        addr_selector = '.css-qyp8bo'
        phone_selector = '.css-djo2w .css-1p9ibgf'
        tags_selector = '.css-1xfc281 span.css-1fdy0l5'

        for selector in (title_selector, addr_selector, phone_selector):
            element = soup.select_one(selector)
            info = element.get_text() if element else '-'
            data.append(info)

        tags = ''
        tag_elements = soup.select(tags_selector)
        for tag_element in tag_elements:
            el = tag_element.find('a')
            tag = el.get_text() if el else '-'
            tags += tag + ','
        tags = tags[:-1]
        data.append(tags)

        return data
