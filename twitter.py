import config
import tweepy
import sys
import json
import jsonpickle
import os

auth = tweepy.AppAuthHandler(config.access['API_KEY'], config.access['API_SECRET'])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
  print ("Twitter API authentication failed")
  sys.exit(-1)
else:
  print ("Twitter API authentication successfull")

searchQuery = '#PanamaPapers'
maxTweets = 10000
fName = 'tweets.txt'

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

tweets_list = []

with open(fName, 'w') as f:
  for tweet in tweepy.Cursor(api.search,q=searchQuery,iso_language_code="en").items(maxTweets) :
    obj = jsonpickle.encode(tweet._json, unpicklable=False)
    data = json.loads(obj)
    text = data['text'].encode('utf-8')
    text = str.lower(text)
    if text[0:2] != 'rt' and text not in tweets_list:
      tweets_list.append(text)
      f.write(obj + '\n')
      tweetCount += 1
      print("Downloaded {0} tweets".format(tweetCount))

print ("Downloaded {0} tweets, saved to {1}".format(tweetCount, fName))
