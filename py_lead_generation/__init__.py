"""py-lead-generation: A Python package for lead generation using web scraping.

This package provides engines for scraping business leads from various sources,
along with tools for email outreach, MCP server integration, and a GUI application.

Engines:
    GoogleMapsEngine: Scrape leads from Google Maps
    YelpEngine: Scrape leads from Yelp
    TwoGisEngine: Scrape leads from 2GIS (stub - not yet implemented)

Modules:
    email: Gmail SMTP email outreach
    mcp: Model Context Protocol server
    gui: Tkinter GUI application
"""

from py_lead_generation.src.google_maps.engine import GoogleMapsEngine
from py_lead_generation.src.twogis.engine import TwoGisEngine
from py_lead_generation.src.yelp.engine import YelpEngine

__all__ = ["GoogleMapsEngine", "YelpEngine", "TwoGisEngine"]
__version__ = "0.1.0"
