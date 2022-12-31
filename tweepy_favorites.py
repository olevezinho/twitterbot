# Author: Luis Brochado
# Objective: Script to favor and retweet tweets
# Creation date: 29/10/2021
# Last edited: 10/11/2021
### Core packages
from time import sleep
import tweepy
import os
from dotenv import load_dotenv
import logging
import logging.config
from services.services import validateDates
from services.database import add_data, close_connection, database_auth
from services.authentication import tweepy_auth, validate_authentication
import re
### Core packges

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
api = tweepy_auth(API_KEY=API_KEY, API_SECRET=API_SECRET, ACCESS_TOKEN=ACCESS_TOKEN, ACCESS_SECRET=ACCESS_SECRET)
validate_authentication(api)

# connect to the database
connection = database_auth(username=USERNAME, password=PASSWORD, host='127.0.0.1', dbname='tweets')
cursor = connection.cursor()

# Read list of tags
with open('list-of-tags.txt') as f:
    list_of_hashtags = list(f)

# Create logger
logger = logging.getLogger('simpleExample')

try:
    # search for topics in a list of hashtags
    for i in list_of_hashtags:
        logger.info(f"tweets about {i}")
        # search for the tweets related to a specific topic
        for tweet in api.search_tweets(q=i, lang="en"):
            # the status contains all information about a specific tweet, like date_of_creation, author name, etc
            status = api.get_status(tweet.id)
            # fetching the favorited attribute
            favored = status.favorited 
            # fetching for special characters in the username
            special = re.search("[^a-zA-Z0-9]+", tweet.author.name)
            # if already liked, then skip, else like
            if favored == True:
                logger.info("The authenticated user already liked the tweet.")
                # Validate some stuff before retweeting
                timeDiff = validateDates(status.created_at)
                if ((status.retweeted == False) and ((status.favorite_count > 50) or (status.retweet_count > 20)) and timeDiff == True):
                    try:
                        api.retweet(tweet.id)
                        sleep(150)
                        # if there are no special characters, then update my status with the recent retweeted author name
                        if special == True:
                            sleep(5)
                        else:
                            api.update_status(status=f"Just retweeted @{tweet.author.screen_name}!!")
                        logger.info("The tweet was retweeted")
                    except tweepy.TweepyException as e:
                        print(e)
                else:
                    logger.info("The tweet didn't fulfull the requirements in order to be retweeted")
            # like the tweet
            else:
                logger.info("The authenticated user has not yet liked the tweet.")
                logger.info(f"tweet id: [{tweet.id}] tweeted at: [{status.created_at}]")
                logger.info(f"tweeted by: \"[{tweet.author.name}]\"")
                logger.info(f"body: \"{tweet.text}\"")
                logger.info("The tweet was favored!")
                api.create_favorite(tweet.id)
                # Validate if tweet is of type airdrop, if so, like, and follow account
                sleep(10)
                add_data(connection, cursor, tweet.id, status.created_at.strftime("%d-%m-%Y %H:%M"), i, tweet.author.name, tweet.text)
                sleep(10)
except tweepy.TweepyException as e:
    #print(e)
    logger.error(e)

close_connection(connection=connection)

# 1 - Reducing the amount of hashtags and increase the interaction/engagement with relevant users/topics                     |# To do
# 2 - Focus on twitter, creating content (within reach), following trends                                                    |# To do
# 3 - Dynamically select a range of hot topics/trends, investigate the trending part, it will most definitey have some value |# Done
# 4 - For Portuguese audience, search for popular hashtags in Brazil                                                         |# To do
# 5 - Get airdrop metadata, and follow, comment, like                                                                        |# Optional
# 6 - Dentro dos tópicos tentar perceber se é um tópico com sentimento positivo/negativo                                     |# Optional