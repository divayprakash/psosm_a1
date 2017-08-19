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
user = raw_input("Enter Twitter user handle: ")
tweets = []
tweetCount = 0

########## GET ALL TWEETS OF USER ##########
for tweet in tweepy.Cursor(api.user_timeline, id=user).items():
  tweets.append(tweet)
  tweetCount = tweetCount + 1

########## PRINT FIRST TWEET ##########
if tweetCount == 3000:
  print ("Very first tweet cannot be read due to Twitter API restrictions!")
else:
  tweet = tweets[-1]
  print tweet.text
  print tweet.created_at
