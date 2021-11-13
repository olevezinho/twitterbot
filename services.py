from datetime import datetime
import tweepy

# tweepy auth function
def tweepy_auth(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
    # Authentication code
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

# tweepy retweet likes function
def retweet_favorites(api, username, count):
    # retweet each tweet
    for tweet in api.get_favorites(username, count):
        try:
            api.retweet(tweet.id)
        except tweepy.TweepyException as e:
            print(e)
    return print("finished.")

# validate authentication on the API
def validate_authentication(api):
    try:
        return api.verify_credentials()
    except:
        return api

# validate if date differs from another one by less than five hours
def validateDates(tweet_date):
    currentDate = datetime.now()
    if (currentDate.strftime("%d") == tweet_date.strftime("%d") and ((int(currentDate.strftime("%H")) - int(tweet_date.strftime("%H"))) > 5)):
        return True
    else:
        return False