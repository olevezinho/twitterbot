import tweepy

class TweepyClient:
    def __init__(self, API_KEY: str, API_SECRET: str, ACCESS_TOKEN: str, ACCESS_SECRET: str):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ACCESS_SECRET = ACCESS_SECRET

    # Tweepy authentication
    def tweepy_auth(self, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth)
        return api