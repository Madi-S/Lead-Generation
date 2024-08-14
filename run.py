import argparse
import asyncio
from py_lead_generation.src.google_maps.engine import GoogleMapsEngine


async def main(search_query, location, zoom):
    try:
        engine = GoogleMapsEngine(search_query, location, zoom)
        await engine.run()
        
        if not engine.has_entries():
            raise RuntimeError("No entries found. Ensure that .run() method was successful.")
        
        engine.save_to_csv('leads.csv')
        
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, handle specific cases or clean up resources

    finally:
        # Ensure browser is always closed
        await engine.shut_browser()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Google Maps search.')
    parser.add_argument('--search_query', required=True, help='The search query')
    parser.add_argument('--location', required=True, help='The location for search')
    parser.add_argument('--zoom', default='12', help='Optional zoom level for Google Maps')
    args = parser.parse_args()
    asyncio.run(main(args.search_query, args.location, args.zoom))
