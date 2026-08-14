"""2GIS lead generation engine.

This module provides an interface for scraping business leads from 2GIS.
Currently a stub implementation - the actual scraping logic needs to be
implemented based on 2GIS website structure.

Example:
    >>> engine = TwoGisEngine('restaurants', 'Almaty')
    >>> await engine.run()  # Not implemented yet
    NotImplementedError: 2GIS scraping not yet implemented
"""

from py_lead_generation.src.engines.abstract import AbstractEngine
from py_lead_generation.src.engines.base import BaseEngine


class TwoGisEngine(BaseEngine, AbstractEngine):
    """2GIS lead generation engine.

    This engine scrapes business information from 2GIS (2gis.kz, 2gis.ru).
    Currently a stub implementation ready for future development.

    Attributes:
        BASE_URL: Base URL template for 2GIS search
        FIELD_NAMES: Column names for exported CSV data
        FILENAME: Default output filename

    Example:
        >>> engine = TwoGisEngine('gym', 'Astana')
        >>> await engine.run()
        NotImplementedError: 2GIS scraping not yet implemented
    """

    BASE_URL = "https://2gis.kz/search/{query}%20{location}"
    FIELD_NAMES = ["Title", "Address", "PhoneNumber", "WebsiteURL", "Category"]
    FILENAME = "twogis_leads.csv"

    def __init__(self, query: str, location: str) -> None:
        """Initialize TwoGisEngine.

        Args:
            query: Search query (e.g., 'restaurants', 'gym')
            location: Location to search in (e.g., 'Almaty', 'Astana')
        """
        self._entries: list[dict] = []
        self.query = query
        self.location = location
        self.url = self.BASE_URL.format(query=self.query, location=self.location)

    async def _get_search_results_urls(self) -> list[str]:
        """Get URLs of search results from 2GIS.

        This method should scroll through search results and collect
        individual business URLs for detailed scraping.

        Returns:
            List of business page URLs

        Raises:
            NotImplementedError: Method not yet implemented
        """
        raise NotImplementedError(
            "2GIS scraping not yet implemented. "
            "Contributions welcome at https://github.com/Madi-S/Lead-Generation"
        )

    def _parse_data_with_soup(self, html: str) -> list[str]:
        """Parse business data from HTML using BeautifulSoup.

        Args:
            html: HTML content of a business page

        Returns:
            List of extracted data matching FIELD_NAMES order

        Raises:
            NotImplementedError: Method not yet implemented
        """
        raise NotImplementedError(
            "2GIS parsing not yet implemented. "
            "Contributions welcome at https://github.com/Madi-S/Lead-Generation"
        )
