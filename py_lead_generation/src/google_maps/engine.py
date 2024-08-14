import time
import sys
import io
import csv
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from geopy.distance import geodesic
from py_lead_generation.src.engines.base import BaseEngine
from py_lead_generation.src.engines.abstract import AbstractEngine
from py_lead_generation.src.misc.utils import get_coords_by_location

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class GoogleMapsEngine(BaseEngine, AbstractEngine):
    BASE_URL = 'https://www.google.com/maps/search/{query}/@{coords},{zoom}z/data=!3m1!4b1?entry=ttu'
    FIELD_NAMES = ['Title', 'Address', 'PhoneNumber', 'WebsiteURL']
    FILENAME = 'google_maps_leads.csv'

    SLEEP_PER_SCROLL_S = 1
    SCROLL_TIME_DURATION_S = 200

    def __init__(self, query: str, location: str, zoom: int | float = 12, radius: int = 50) -> None:
        self._entries = []
        self.zoom = zoom
        self.query = query
        self.location = location
        self.radius = radius
        self.coords = get_coords_by_location(self.location)
        self.search_query = f'{self.query}%20{self.location}'
        self.url = self.BASE_URL.format(
            query=self.search_query, coords=','.join(map(str, self.coords)), zoom=self.zoom
        )
        self.browser = None
        self.page = None

    async def init_browser(self, hidden=True):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=hidden)
        self.page = await self.browser.new_page()

    async def shut_browser(self):
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()

    async def search(self):
        if not self.page:
            raise ValueError('Initialize the browser before searching by `await *.init_browser()`')

        await self.page.goto(self.url)
        await self._get_search_results_urls()

    async def _get_search_results_urls(self) -> list[str]:
        async def hover_search_results() -> None:
            leftbar = await self.page.query_selector('[role="main"]')
            if leftbar:
                await leftbar.hover()
                await asyncio.sleep(0.5)

        async def scroll_and_sleep(delta_y: int = 1000) -> None:
            await self.page.mouse.wheel(0, delta_y)
            await asyncio.sleep(self.SLEEP_PER_SCROLL_S)

        async def end_locator_is_present() -> bool:
            end_locator = await self.page.query_selector('.m6QErb.tLjsW.eKbjU')
            return bool(end_locator)

        async def scrape_urls() -> list[str]:
            urls = []
            link_elements = await self.page.query_selector_all('a.hfpxzc')
            for link_element in link_elements:
                url = await link_element.get_attribute('href')
                coords = self._extract_coords_from_url(url)
                if coords and self._is_within_bounds(coords):
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
        soup = BeautifulSoup(html, 'html.parser')
        data = []

        title = soup.select_one('.DUwDvf.lfPIob')
        data.append(title.get_text() if title else 'No Info')

        address = soup.select_one('[data-item-id="address"] .Io6YTe')
        data.append(address.get_text() if address else 'No Info')

        phone = soup.select_one('[data-tooltip="Copy phone number"] .Io6YTe')
        data.append(phone.get_text() if phone else 'No Info')

        website = soup.select_one('[data-item-id="authority"] .Io6YTe')
        data.append(website.get_text() if website else 'No Info')

        return data

    async def run(self):
        if not self.page:
            raise ValueError('Initialize the browser before running by `await *.init_browser()`')

        await self.search()
        urls = await self._get_search_results_urls()

        with open(self.FILENAME, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.FIELD_NAMES)

            for url in urls:
                await self.page.goto(url)
                html = await self.page.content()
                data = self._parse_data_with_soup(html)
                print("Extracted ", [d.encode('utf-8', 'replace').decode('utf-8', 'replace') for d in data])
                self._entries.append(data)
                writer.writerow(data)

    def save_to_csv(self, filename=None):
        filename = filename or self.FILENAME
        if not self._entries:
            raise NotImplementedError("Entries are empty, call .run() method first to save them")

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.FIELD_NAMES)
            writer.writerows(self._entries)

    def _extract_coords_from_url(self, url: str) -> tuple[float, float]:
        import re
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
        if match:
            lat, lon = map(float, match.groups())
            return lat, lon
        return None

    def _is_within_bounds(self, coords: tuple[float, float]) -> bool:
        distance = geodesic(self.coords, coords).meters
        return distance <= self.radius
