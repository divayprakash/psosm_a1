import config
import tweepy

auth = tweepy.AppAuthHandler(config.access['API_KEY'], config.access['API_SECRET'])

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
  print ("Can't Authenticate")
  sys.exit(-1)
else:
  print ("Success")
