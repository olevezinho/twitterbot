from webbrowser import get
import os
from dotenv import load_dotenv
import logging
import logging.config

from services.authentication import twitter_auth
from services.services import getTrends

load_dotenv()
logging.config.fileConfig('logging.conf')

# Access credentials within .env
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Authenticate on twitter
twitter_api = twitter_auth(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

WORLD_WOE_ID = 1
__PT__WOE_ID = 23424925

world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
pt_trends    = twitter_api.trends.place(_id=__PT__WOE_ID)

getTrends(pt_trends)