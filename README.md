# Lead-Generation

The updated version of my outdated dirty clumsy with a shockingly high amount of stars repository on Python

# Installation

```bash
pip install py-lead-generation
```

[Pypi Link](https://pypi.org/project/py-lead-generation)

OR

```bash
git clone https://github.com/Madi-S/Lead-Generation
cd Lead-Generation
cd archived
cd google-maps
python extractor.py
```

OR to use the previous archived version
```bash
git clone https://github.com/Madi-S/Lead-Generation
cd Lead-Generation
python run.py
```

# Quickstart

```python
import asyncio
from py_lead_generation import GoogleMapsEngine, YelpEngine


async def main() -> None:
    q = input('Enter your search query: ').strip() or 'Barbershop'
    addr = input('Enter the location you would like to search in: ').strip() \
        or 'Paris'
    zoom = float(input('[Optional] Enter google maps zoom: ').strip() or 12)

    engine = GoogleMapsEngine(q, addr, zoom)
    await engine.run()
    engine.save_to_csv()

    engine = YelpEngine('Pizza', 'Mexico, Pampanga, Philippines')
    await engine.run()
    engine.save_to_csv('pizza_leads.csv')

if __name__ == '__main__':
    asyncio.run(main())
```

# Current functionality

    - Parse Google Maps
    - Parse Yelp
    - Export collected data to a CSV file

# Expectations of this project:

    - Parse Google Maps and Yelp for telephone number, email, address, and other information by given keyword
    - Somehow parse search results in Google Search for the same information using regex or other algorithms
    - Export all parsed data to CSV or Excel
    - For parsed emails send a message, which will be prevented from going to spam
    - For parsed telephone numbers send an SMS, which will be prevented from going to spam as well
