########## IMPORTS ##########
import config  # external configuration file with API keys
import tweepy
import sys
import json
import jsonpickle
import os
from collections import Counter
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from datetime import datetime

########## CONNECTING TO TWITTER API USING TWEEPY ##########
auth = tweepy.AppAuthHandler(config.access['API_KEY'], config.access['API_SECRET'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
  print ("Twitter API authentication failed")
  sys.exit(-1)
else:
  print ("Twitter API authentication successfull")

########## SETTING SEARCH PARAMETERS ##########
searchQuery = '#PanamaPapers'
maxTweets = 10000
tweetsPerQry = 100
fName = 'tweets.txt'
language = 'en'
max_id = -1L

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

########## VARIABLES FOR STORING RELEVANT DATA AS REQUIRED FOR ANALYSIS ##########
tweets_text_lowercase = []
tweets_list = []
tweets_words = []
tweets_countries = []
tweets_dates = []
count_image = 0
count_media = 0
count_url = 0
count_user_mentions = 0
count_hashtags = 0
count_quote = 0
count_rt = 0

stop_words = set(stopwords.words('english'))

########## MAIN LOOP FOR TWEET RETREIVAL AND PROCESSING ##########
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
        # Check tweet is not a retweet and is not a repeat of any tweet that occured earlier (copy-paste)
        if text[0:2] != 'rt' and text not in tweets_text_lowercase:
          tweets_text_lowercase.append(text)
          tweets_list.append(tweet)
          temp = text.split()
          for word in temp:
            # remove stop words and add unique words to a list
            if word.isalpha() and word not in stop_words:
              tweets_words.append(word)
          f.write(obj + '\n')
          tweetCount += 1
          # get country data
          if data['place']:
            country = data['place']['country'].encode('utf-8')
            tweets_countries.append(country)
          # get tweet creation time
          created = data['created_at'].encode('utf-8')
          c = created.split()
          date = c[1] + ' ' + c[2]
          tweets_dates.append(date)
          # get count of tweets containing urls
          try:
            if data['entities']['urls']:
              count_url = count_url + 1
          except KeyError:
            pass
          # get count of tweets containing media
          try:
            if data['entities']['media']:
              for image in data['entities']['media']:
                if image['type'] == 'photo':
                  count_image = count_image + 1
                elif image['media_url']:
                  count_media = count_media + 1
          except KeyError:
            pass
          # get count of tweets mentioning other users
          try:
            if data['entities']['user_mentions']:
              count_user_mentions = count_user_mentions + 1
          except KeyError:
            pass
          # get count of tweets containing hashtags
          try:
            if data['entities']['hashtags']:
              count_hashtags = count_hashtags + 1
          except KeyError:
            pass
          # get count of tweets that were retweeted by other users
          try:
            if data['retweet_count'] > 0:
              count_rt = count_rt + 1
          except KeyError:
            pass
          # get count of tweets that were quote tweets
          try:
            if data['quoted_status']:
              count_quote = count_quote + 1
          except KeyError:
            pass
      print("Downloaded {0} tweets".format(tweetCount))
      max_id = new_tweets[-1].id
    # error handling
    except tweepy.TweepError as e:
      print("ERROR! : " + str(e))
      break

print ("Downloaded {0} tweets, saved to {1}".format(tweetCount, fName))
print ("{0} tweets contained URLs".format(count_url))
print ("{0} tweets contained images".format(count_image))
print ("{0} tweets contained media other than images".format(count_media))
print ("{0} tweets mentioned other users".format(count_user_mentions))
print ("{0} tweets contained hashtags".format(count_hashtags))
print ("{0} tweets out of the total were retweeted by other users".format(count_rt))
print ("{0} tweets were quote tweets".format(count_quote))
keys = ['URL', 'Image', 'Other media', 'Mentions', 'Hashtags', 'Retweet', 'Quote']
height = [5, 5, 5, 5, 5, 5, 5]
size = [count_url, count_image, count_media, count_user_mentions, count_hashtags, count_rt, count_quote]
label = []
for i in size:
  label.append('Tweets: ' + str(i))
plot([go.Scatter(x=keys, y=height, text=label, mode='markers', marker=dict(size=size))], show_link=False, filename='histogram.html', image='svg', image_filename='hist')

########## PROCESSING DATA AND PLOTTING WORDS HISTOGRAM ##########
words_dict = Counter(tweets_words)
histogram_data = words_dict.most_common(20)
keys = [x[0] for x in histogram_data]
values = [x[1] for x in histogram_data]
plot([go.Bar(x=keys, y=values)], show_link=False, filename='histogram.html', image='svg', image_filename='hist')

########## PROCESSING DATA AND PLOTTING COUNTRY PIE CHART ##########
countries_dict = Counter(tweets_countries)
pie_data = countries_dict.most_common()
labels = [x[0] for x in pie_data]
values = [x[1] for x in pie_data]
plot([go.Pie(labels=labels, values=values)], show_link=False, filename='pie.html', image='svg', image_filename='pie')

########## PROCESSING DATES AND PLOTTING TIME SERIES GRAPH ##########
dates_dict = {}
for date in tweets_dates:
  if date in dates_dict:
    dates_dict[date] = dates_dict[date] + 1
  else:
    dates_dict[date] = 1
dates = dates_dict.keys()
dates_sorted = sorted(dates, key=lambda date: datetime.strptime(date, "%b %d"))
keys = dates_sorted
values = []
for date in dates_sorted:
  values.append(dates_dict[date])
plot([go.Scatter(x=keys, y=values)], show_link=False, filename='line.html', image='svg', image_filename='line')
