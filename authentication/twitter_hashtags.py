import re
from time import sleep
import tweepy
from datetime import datetime

class Hashtags:
    def __init__(self, filename: str, array, api, logger):
        self.filename = filename
        self.array = array
        self.api = api
        self.logger = logger

    # Read list of tags
    def read_tags(self, filename: str):
        with open(filename, "r") as f:
            list_of_hashtags = list(f)
        return list_of_hashtags

    # Write list of tags
    def write_tags(self, filename: str, array):
        with open(filename, 'w') as f:
            for data in array:
                for trends in data['trends']:
                    f.write(trends['name']+'\n')
        return None

    # Validate dates
    def _validateDates(self, tweet_date):
        currentDate = datetime.now()
        if (currentDate.strftime("%d") == tweet_date.strftime("%d") and ((int(currentDate.strftime("%H")) - int(tweet_date.strftime("%H"))) > 5)):
            return True
        else:
            return False

    # Like tags logic
    def like_tags(self, api, logger, hashtags):
        # Count likes
        count = 0
        try:
            # search for topics in a list of hashtags
            for i in hashtags:
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
                        timeDiff = self._validateDates(status.created_at)
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
                                logger.error(e)
                                logger.exception(e.with_traceback())
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
                        count += 1
                        #add_data(connection, cursor, tweet.id, status.created_at.strftime("%d-%m-%Y %H:%M"), i, tweet.author.name, tweet.text)
                        #sleep(10)
        except tweepy.TweepyException as e:
            #print(e)
            logger.error(e)
            logger.info(f"{count} tweets favored!")
            logger.exception(e.with_traceback())
        return None