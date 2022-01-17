import json
from webbrowser import get
import os
from dotenv import load_dotenv
import logging
import logging.config
from urllib.parse import unquote

from services.authentication import twitter_auth, tweepy_auth, validate_authentication
from services.services import getHomeTimeline, getUserTimeline, queryTwitter_1, queryTwitter_2

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

#getHomeTimeline(twitter_api)

users = [
    "@andrewlocknet",   "@shanselman",      "@elonmusk",
    "@timoreilly",      "@bramcohen"
]

#getUserTimeline(twitter_api, users)

#queryTwitter_2(twitter_api)

# Authenticate on twitter
api = tweepy_auth(API_KEY=API_KEY, API_SECRET=API_SECRET, ACCESS_TOKEN=ACCESS_TOKEN, ACCESS_SECRET=ACCESS_SECRET)
validate_authentication(api)

for user in users:
    for follower in api.get_followers(user_id=user):
        print(follower.screen_name)