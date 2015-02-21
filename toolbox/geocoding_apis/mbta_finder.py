""" Finds the MBTA stops closest to a given location
	Joey L. Maalouf
"""


import json
import sys
from urllib2 import urlopen


GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


def get_lat_long(place_name):
	"""
	Given a place name or address, return a (latitude, longitude) tuple
	with the coordinates of the given place.
	See https://developers.google.com/maps/documentation/geocoding/
	for Google Maps Geocode API URL formatting requirements.
	"""
	place_name = place_name.replace(" ", "%20")
	url = GMAPS_BASE_URL+"?address="+place_name
	json_response = urlopen(url).read()
	data_obj = json.loads(json_response)
	location = data_obj["results"][0]["geometry"]["location"]
	return (location["lat"], location["lng"])


def get_nearest_station(latitude, longitude):
	"""
	Given latitude and longitude strings, return a (station_name, distance)
	tuple for the nearest MBTA station to the given coordinates.
	See http://realtime.mbta.com/Portal/Home/Documents for URL
	formatting requirements for the "stopsbylocation" API.
	"""
	url = MBTA_BASE_URL+"?api_key="+MBTA_DEMO_API_KEY+"&lat="+str(latitude)+"&lon="+str(longitude)+"&format=json"
	json_response = urlopen(url).read()
	data_obj = json.loads(json_response)
	closest_stop = data_obj["stop"][0]
	return (closest_stop["stop_name"], closest_stop["distance"])


def find_stop_near(place_name):
	"""
	Given a place name or address, print the nearest MBTA stop and the 
	distance from the given place to that stop.
	"""
	lat, lon = get_lat_long(place_name)
	stop, dist = get_nearest_station(lat, lon)
	print("Closest stop: "+stop)
	print("Distance: "+dist+" miles")


if __name__ == '__main__':
	find_stop_near(sys.argv[1])
