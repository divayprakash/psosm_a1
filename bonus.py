########## IMPORTS ##########
import config  # external configuration file with API keys
import tweepy

########## CONNECTING TO TWITTER API USING TWEEPY ##########
auth = tweepy.AppAuthHandler(config.access['API_KEY'], config.access['API_SECRET'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
  print ("Twitter API authentication failed")
  sys.exit(-1)

########## DEFINE VARIABLES ##########
user = "@divayprakash3"
tweets = []

########## GET ALL TWEETS OF USER ##########
for tweet in tweepy.Cursor(api.user_timeline, id=user).items():
  tweets.append(tweet)

########## PRINT FIRST TWEET ##########
print tweets[-1].text
print tweets[-1].created_at
