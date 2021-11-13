import datetime
from time import sleep
import tweepy
import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")

except:
    print("Error during authentication")

user = api.get_user(screen_name='oLevezinho')

tweets = api.home_timeline(count=200)
# Consume the tweet index and like the tweet by id
#print(f"Liking tweet {tweet.id} of {tweet.author.name}")
#api.create_favorite(tweet.id)
#sleep(1)

# like a bunch of tweets on my feed
for tweet in tweets:
    status = api.get_status(tweet.id)
    # fetching the favorited attribute
    favorited = status.favorited 
    # if already liked, then skip, else like
    if favorited == True:
        print("The authenticated user has liked the tweet.")
    else:
        print("The authenticated user has not liked the tweet.")
        print(f"Liking tweet {tweet.id} of {tweet.author.name}")
        api.create_favorite(tweet.id)
        sleep(1)

# Listing the user id and friend's screen names
#print(user.id)
#print(user.followers_count)
#for friend in user.friends():
    #print(friend.screen_name)
# testing a post on twitter (working)
#api.update_status(status="I'm thinking about writing a Python article")

# Search tweets and like tweets in certain topics
for tweet in api.search_tweets(q="WebSummit", lang="en"):
    #print(f"{tweet.user.name}:{tweet.text}")
    status = api.get_status(tweet.id)
    # fetching the favorited attribute
    favorited = status.favorited 
    # if already liked, then skip, else like
    if favorited == True:
        print("The authenticated user has liked the tweet.")
    else:
        print("The authenticated user has not liked the tweet.")
        print(f"{tweet.id}")
        api.create_favorite(tweet.id)

# print the id for each of the tweets
#for tweet in tweet_list:
    #print(tweet.id)

# retweet tweet.id
#tweet_id = 1454151631289962498
#api.retweet(tweet_id)

# retweet each tweet
for tweet in api.get_favorites(screen_name='andrewlocknet', count=1):
    try:
        print(tweet.author.screen_name)
        #print(api.get_retweets(id=tweet.id))
        print(api.get_status(id=tweet.id).retweet_count)
        print(api.get_status(id=tweet.id).favorite_count)
        print(api.get_status(id=tweet.id).retweeted)
        print(api.get_status(id=tweet.id).created_at.strftime("%d-%m-%Y %H:%M:%S"))
        currentDate = datetime.now()
        print(currentDate.strftime("%d-%m-%Y %H:%M:%S"))
        print(currentDate.strftime("%d"))
        print(currentDate.strftime("%m"))
        print(currentDate.strftime("%Y"))
        #api.retweet(tweet.id)
    except tweepy.TweepyException as e:
        print(e)