# Author: Luis Brochado
# Objective: Authentication modules
# Creation date: 29/10/2021
# Last edited: 17/01/2022
### Core packages

from datetime import datetime
import tweepy
import twitter

# tweepy auth function
def tweepy_auth(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
    # Authentication code
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

# validate authentication on the API
def validate_authentication(api):
    try:
        return api.verify_credentials()
    except:
        return api

# twitter auth function
def twitter_auth(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
    credentials = twitter.oauth.OAuth(
        ACCESS_TOKEN, ACCESS_SECRET, API_KEY, API_SECRET 
    )
    twitter_api = twitter.Twitter(auth=credentials)
    return twitter_api
