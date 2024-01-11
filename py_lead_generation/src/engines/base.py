import asyncio
from playwright.async_api import Playwright, async_playwright

from py_lead_generation.src.misc.writer import CsvWriter
from py_lead_generation.src.engines.playwright_config import PlaywrightEngineConfig


class BaseEngine(PlaywrightEngineConfig):
    '''
    `BaseEngine`

    Base engine class expressing methods, which are shared between all engines, does not provide implementation of `AbstractEngine` methods
    '''

    async def run(self) -> None:
        '''
        Uses headles webdriver powered by Playwright

        Creates a web url based on initialized parameters

        Parses results by given query and url one by one

        Assigns collected results to `.entries`

        To save the results call `.save_to_csv()` method after       
        '''
        async with async_playwright() as playwright:
            self.playwright: Playwright = playwright
            await self._setup_browser()
            await self._open_url_and_wait(self.url)
            urls: list[str] = await self._get_search_results_urls()
            self._entries: list[dict] = await self._get_search_results_entries(urls)
            await self.browser.close()

    def save_to_csv(self, filename: str = None) -> None:
        '''
        `filename: str = None` - optional parameter, by default uses `self.FILENAME`
        
        If file with such name already exists, it will not overwrite it but append newly found entries to existing ones

        If file with such name does not exist, it will create a new csv file with predetermined fieldnames
        '''
        if filename:
            self.FILENAME = filename

        if not self.FILENAME.endswith('.csv'):
            raise ValueError('Use .csv file extension')
        if not self._entries:
            raise NotImplementedError(
                'Entries are empty, call .run() method first to save them'
            )
        csv_writer = CsvWriter(self.FILENAME, self.FIELD_NAMES)
        csv_writer.append(self._entries)

    @property
    def entries(self) -> list[dict]:
        '''
        Returns `list[dict]` typed entries once `.run()` method was called
        '''
        if not self._entries:
            raise NotImplementedError(
                'Entries are empty, call .run() method first to create them'
            )
        return self._entries

    @entries.setter
    def entries(self, _) -> None:
        '''
        You cannot do that ;)

        Made for durability reasons
        '''
        raise ValueError('Cannot set value to data. This is not allowed')

    async def _open_url_and_wait(self, url: str, sleep_duration_s: int = 3) -> None:
        '''
        `url: str` - url to open
        `sleep_duration_s: int = 3` - amount of seconds to wait for the page to load before any operations on that page

        Navigates to initialized `self.url` and waits for `sleep_duration_s` seconds
        '''
        await self.page.goto(url)
        await asyncio.sleep(sleep_duration_s)

    async def _get_search_results_entries(self, urls: list[str]) -> list[dict]:
        '''
        `urls: list[str]` - list of urls for google maps entities to scrape for

        Goes over each url in the list and retreives data from opening page one by one

        Searches for data using exact image source values selectors, no other unique way to extract data using selectors is not found yet

        Returns `list[dict]` typed search result entries for each seperate given url from `urls`
        '''
        entries = []
        for url in urls:
            await self._open_url_and_wait(url, 1.5)
            html = await self.page.content()
            data = self._parse_data_with_soup(html)
            entry = dict(zip(self.FIELD_NAMES, data))
            entries.append(entry)

        return entries
