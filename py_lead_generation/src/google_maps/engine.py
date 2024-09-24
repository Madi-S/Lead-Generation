import time
import asyncio
import re
from bs4 import BeautifulSoup

from py_lead_generation.src.engines.base import BaseEngine
from py_lead_generation.src.engines.abstract import AbstractEngine
from py_lead_generation.src.misc.utils import get_coords_by_location


class GoogleMapsEngine(BaseEngine, AbstractEngine):
    '''
    `GoogleMapsEngine`

    [EDITABLE] `SCROLL_TIME_DURATION_S` - scroll time duration to view the search results, preferably should be not less than 150, for testing purposes can be decreased

    [EDITABLE] `SLEEP_PER_SCROLL_S` - amount of seconds to wait before each scroll of search results so that google maps does not output endless loading ~ aka simulate human-like activity, preferable should be not less than 5

    Usage:

    `engine = GoogleMapsEngine(*args, **kwargs)`

    `await engine.run()`

    `await engine.save_to_csv()`

    `print(engine.entries)`
    '''

    BASE_URL = 'https://www.google.com/maps/search/{query}/@{coords},{zoom}z/data=!3m1!4b1?entry=ttu'
    FIELD_NAMES = ['Title', 'Address', 'PhoneNumber', 'WebsiteURL']
    FILENAME = 'google_maps_leads.csv'

    SLEEP_PER_SCROLL_S = 5
    SCROLL_TIME_DURATION_S = 200

    def __init__(self, query: str, location: str, zoom: int | float = 12) -> None:
        '''
        `query: str` - what are you looking for? e.g., `gym`
        `location: str` - where are you looking for that query? e.g., `Astana`
        `zoom: int | float` - google maps zoom e.g., `8.75`

        Creates `GoogleMapsEngine` instance
        '''
        self._entries = []
        self.zoom = zoom
        self.query = query
        self.location = location
        self.coords = get_coords_by_location(self.location)
        self.search_query = f'{self.query}%20{self.location}'
        self.url = self.BASE_URL.format(
            query=self.search_query, coords=','.join(self.coords), zoom=self.zoom
        )

    async def _get_search_results_urls(self) -> list[str]:
        '''
        Goes through the search results for `GoogleMapsEngine.SCROLL_TIME_DURATION_S` seconds

        Waits for `GoogleMapsEngine.SLEEP_PER_SCROLL_S` seconds so that GoogleMaps will not output endless load, aka simulate human-like activity

        Or scrapes the results urls, once the are no more results
        '''
        async def hover_search_results() -> None:
            '''
            Hovers on leftbar, where search results are located

            Needed so that scroll function is used properly - not on the map but on the search results div
            '''
            leftbar = await self.page.query_selector('[role="main"]')
            await leftbar.hover()
            await asyncio.sleep(0.5)

        async def scroll_and_sleep(delta_y: int = 1000) -> None:
            '''
            `delta_y: int = 1000` pixel units to scroll down along y-axis

            Scrolls down by `delta_y` and waits for `GoogleMapsEngine.SCROLL_TIME_DURATION_S` seconds
            '''
            await self.page.mouse.wheel(0, delta_y)
            await asyncio.sleep(self.SLEEP_PER_SCROLL_S)

        async def end_locator_is_present() -> bool:
            '''
            Retunrs `end_locator` as boolean value, which correlates with the possible end of the search results

            Once `end_locator` is Truthy, aka ElemenetHandle, it means that there is nothing more to scroll
            '''
            end_locator = await self.page.query_selector('.m6QErb.tLjsW.eKbjU')
            return bool(end_locator)

        async def scrape_urls() -> list[str]:
            '''
            Should be called once page is being scrolled all the way down (`end_locator` found) or `GoogleMapsEngine.SCROLL_TIME_DURATION_S` duration limit is exceeded

            Returns `list[str]` typed scraped urls list using query_selector
            '''
            urls = []
            link_elements = await self.page.query_selector_all('a.hfpxzc')
            for link_element in link_elements:
                url = await link_element.get_attribute('href')
                urls.append(url)
            return urls

        await hover_search_results()
        start_scroll_time = time.time()

        while True:
            await scroll_and_sleep()
            finish_scroll_time = time.time()
            if (await end_locator_is_present()) or (finish_scroll_time - start_scroll_time > self.SCROLL_TIME_DURATION_S):
                break

        urls = await scrape_urls()
        return urls

    def _parse_data_with_soup(self, html: str) -> list[str]:
        '''
        Parse HTML content to extract business details.

        Parameters:
        html (str): HTML representation of the page to parse.

        Returns:
            list[str]: A list containing parsed data in the order [title, address, phone, website]
        '''
        soup = BeautifulSoup(html, 'html.parser')

        selectors = {
            'title': '.DUwDvf.lfPIob',
            'address': '[data-item-id="address"]',
            'phone_number': '[data-item-id^="phone:"]',
            'website_url': '[data-item-id="authority"]'
        }

        def extract_text(selector: str, default: str = '', cleaner: callable = None) -> str:
            element = soup.select_one(selector)
            text = element.get_text() if element else default
            return cleaner(text) if cleaner else text

        # Cleaners
        def clean_phone_number(text: str) -> str:
            return re.sub(r'\D', '', text)
        
        def clean_address(text: str) -> str:
            return text.replace('', '').strip()
        
        def clean_website_url(text: str) -> str:
            return text.replace('', '').strip()
        
        cleaners = {
            'phone_number': clean_phone_number,
            'address': clean_address,
            'website_url': clean_website_url
        }

        # Parsing and cleaning
        parsed_data = [
            extract_text(selectors[key], cleaner=cleaners.get(key)) for key in selectors
        ]

        return parsed_data