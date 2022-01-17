# Author: Luis Brochado
# Objective: Modular services script to define functions
# Creation date: 29/10/2021
# Last edited: 17/01/2022
### Core packages

from datetime import datetime
import tweepy
import json

# tweepy retweet likes function
def retweet_favorites(api, username, count):
    # retweet each tweet
    for tweet in api.get_favorites(username, count):
        try:
            api.retweet(tweet.id)
        except tweepy.TweepyException as e:
            print(e)
    return print("finished.")

# validate if date differs from another one by less than five hours
def validateDates(tweet_date):
    currentDate = datetime.now()
    if (currentDate.strftime("%d") == tweet_date.strftime("%d") and ((int(currentDate.strftime("%H")) - int(tweet_date.strftime("%H"))) > 5)):
        return True
    else:
        return False

# get twitter trends
def getTrends(trends):
    # counter to print only the first 30 trends
    i=0
    # for cycle to iterate through the trends
    for trend in trends[0]["trends"]:
        with open('list-of-tags.txt', 'a') as f:
            f.write('\n')
            f.write(f"{trend['name']}")
        i += 1
    
        if i > 29:
            break
    
    return
    
# get user home timeline
def getHomeTimeline(twitter_api):
    statuses = twitter_api.statuses.home_timeline(count = 50)
    print(json.dumps(statuses[0], indent=3))

    for status in statuses:
        print("(%s) @%s %s" % (status["created_at"], status["user"]["screen_name"], status["text"]))

# get specific user's timeline
def getUserTimeline(twitter_api, users):
    i = 0

    for user in users:  
        statuses = twitter_api.statuses.user_timeline(screen_name=users[i], count=50)

        for status in statuses:
            dts = status["created_at"]
            dts = dts[:19] + dts[25:]
            usr = status["user"]["screen_name"]
            txt = status["text"]
            print("%s @%s %s" % (dts, usr, txt))
        
        i += 1

# query twitter for results
def queryTwitter_1(twitter_api):
    query = input('\nInput your query> ')
    search_results = twitter_api.search.tweets(q=query, count=100)
    statuses = search_results['statuses']

    print(json.dumps(statuses[0], indent=3))

    for (i, x) in enumerate(statuses):
        print("%3d --> %s" % (i,x["text"]))

# query twitter for results
def queryTwitter_2(twitter_api):
    query = input('\nInput your query> ')
    search_results = twitter_api.search.tweets(q=query, count=100)
    statuses = search_results['statuses']

    for i,s in enumerate(statuses): 
        print("%d %s (%s)" % (i, s["created_at"], s["user"]["screen_name"])) 
        print(s["text"], '\n')

# Iterate through 5 more batches of results by following the cursor
#def queryTwitter_3(twitter_api):