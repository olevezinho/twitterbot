import logging
import logging.config
import os
from dotenv import load_dotenv

from twitter_geography import Geography
from tweepy_client import TweepyClient
from twitter_hashtags import Hashtags

load_dotenv()

# Access credentials within .env
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

# hashtags file
filename = "./hashtags.txt"

# Logging configuration
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('twitterbot')

# Main function
if __name__ == '__main__':
    client = TweepyClient(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    logger.info("Welcome to twitterbot! Authenticating ...")
    api = client.tweepy_auth(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    logger.info(api.user_agent)

    # Available Locations
    logger.info("Fetching available locations.")
    geography = Geography(api, logger)
    geography.get_location_trends(api, logger)

    # Trends for Specific Country
    logger.info("Finding closest location.")
    geolocation = geography.finding_close_location()

    # Storing trends in an array
    logger.info("Gathering trends closer to your location.")
    closest_loc = api.closest_trends(geolocation.lat, geolocation.lng)
    array = api.get_place_trends(closest_loc[0]['woeid'])

    # Instantiate and call hashtags class
    file = Hashtags(filename, array, api, logger)
    try:
        logger.info("Writing trends to a file.")
        file.write_tags(filename, array)
        logger.info("Reading trends from file.")
        tags = file.read_tags(filename)
        file.like_tags(api, logger, tags)   
    except Exception as e:        
        logger.error(e)
        logger.exception(e.with_traceback())