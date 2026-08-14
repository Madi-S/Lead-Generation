from abc import ABC, abstractmethod
from typing import Any


class AbstractEngine(ABC):
    '''
    `AbstractEngine`

    Abstract class specifying main methods and attributes

    [CONSTANT] `BASE_URL` - base url for google maps website with substitute search query, coordinates and zoom

    [CONSTANT] `FIELD_NAMES` - field names of scraped data, extracts data entries to csv file based on these field names

    [EDITABLE] `FILENAME` - file name for exporting collected leads, must have .csv extension
    '''

    BASE_URL = ''
    FIELD_NAMES: list[str] = []
    FILENAME = 'leads.csv'

    @abstractmethod
    async def _get_search_results_urls(self, *args: Any, **kwargs: Any) -> list[str]:
        '''
        Retreiving search results URLs from the website (Yelp/Google Maps) method
        '''
        ...

    @abstractmethod
    def _parse_data_with_soup(self, html: str) -> list[str]:
        '''
        `html: str` - html representation of the page to parse

        Should be defined in child class

        Returns list of values matching FIELD_NAMES order - `[title, addr, phone, website]`
        '''
        ...
