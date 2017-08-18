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
tweetsPerQry = 100
fName = 'tweets.txt'
language = 'en'

max_id = -1L

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

tweets_list_lowercase = []

with open(fName, 'w') as f:
  while tweetCount < maxTweets:
    try:
      if (max_id <= 0):
        new_tweets = api.search(q=searchQuery, lang=language, count=tweetsPerQry)
      else:
        new_tweets = api.search(q=searchQuery, lang=language, count=tweetsPerQry, max_id=str(max_id - 1))
      if not new_tweets:
        print("No more tweets found!")
        break
      for tweet in new_tweets:
        obj = jsonpickle.encode(tweet._json, unpicklable=False)
        data = json.loads(obj)
        text = data['text'].encode('utf-8')
        text = str.lower(text)
        if text[0:2] != 'rt' and text not in tweets_list_lowercase:
          tweets_list_lowercase.append(text)
          f.write(obj + '\n')
          tweetCount += 1
      print("Downloaded {0} tweets".format(tweetCount))
      max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
      print("some error : " + str(e))
      break

print ("Downloaded {0} tweets, saved to {1}".format(tweetCount, fName))
