from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent='google-leads')


def get_coords_by_location(location: str) -> tuple[str]:
    '''
    `location: str` - specific location or city name

    Returns a tuple of the coordinates, two strings represented as float numbers - (latitude, longitude)
    '''
    loc = geolocator.geocode(location)
    coords = (loc.latitude, loc.longitude)
    coords = list(map(str, coords))
    return coords
