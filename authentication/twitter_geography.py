import json
import sys
import geocoder

class Geography:
    def __init__(self, api, logger):
        self.api = api
        self.logger = logger

    # Writing a JSON file that has the available trends around the world
    def get_location_trends(self, api, logger):
        available_loc = api.available_trends()
        with open("./available_locs_for_trend.json","w") as wp:
            logger.info("Writing locations to a file.")
            wp.write(json.dumps(available_loc, indent=1))
        return None

    # Finding the closest location
    def finding_close_location(self):
        location = sys.argv[0]     # location as argument variable 
        geolocation = geocoder.osm(location) # getting object that has location's latitude and longitude
        return geolocation
