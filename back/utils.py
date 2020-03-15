import diceware
import argparse
from . import models
from geopy.geocoders import Nominatim

def get_passphrase():
    options = diceware.handle_options(['--num', '4'])

    return diceware.get_passphrase(options)

def get_coordinates_from_address(address):
    geolocator = Nominatim(user_agent="covid")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)
