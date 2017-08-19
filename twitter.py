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
tweets_time_zones = []
accounts_created = []
usernames = []
time_zone_dict = {}

time_zone_dict["International Date Line West"] = "Pacific/Midway"
time_zone_dict["Midway Island"] = "Pacific/Midway"
time_zone_dict["American Samoa"] = "Pacific/Pago_Pago"
time_zone_dict["Hawaii"] = "Pacific/Honolulu"
time_zone_dict["Alaska"] = "America/Juneau"
time_zone_dict["Pacific Time (US & Canada)"] = "America/Los_Angeles"
time_zone_dict["Tijuana"] = "America/Tijuana"
time_zone_dict["Mountain Time (US & Canada)"] = "America/Denver"
time_zone_dict["Arizona"] = "America/Phoenix"
time_zone_dict["Chihuahua"] = "America/Chihuahua"
time_zone_dict["Mazatlan"] = "America/Mazatlan"
time_zone_dict["Central Time (US & Canada)"] = "America/Chicago"
time_zone_dict["Saskatchewan"] = "America/Regina"
time_zone_dict["Guadalajara"] = "America/Mexico_City"
time_zone_dict["Mexico City"] = "America/Mexico_City"
time_zone_dict["Monterrey"] = "America/Monterrey"
time_zone_dict["Central America"] = "America/Guatemala"
time_zone_dict["Eastern Time (US & Canada)"] = "America/New_York"
time_zone_dict["Indiana (East)"] = "America/Indiana/Indianapolis"
time_zone_dict["Bogota"] = "America/Bogota"
time_zone_dict["Lima"] = "America/Lima"
time_zone_dict["Quito"] = "America/Lima"
time_zone_dict["Atlantic Time (Canada)"] = "America/Halifax"
time_zone_dict["Caracas"] = "America/Caracas"
time_zone_dict["La Paz"] = "America/La_Paz"
time_zone_dict["Santiago"] = "America/Santiago"
time_zone_dict["Newfoundland"] = "America/St_Johns"
time_zone_dict["Brasilia"] = "America/Sao_Paulo"
time_zone_dict["Buenos Aires"] = "America/Argentina/Buenos_Aires"
time_zone_dict["Montevideo"] = "America/Montevideo"
time_zone_dict["Georgetown"] = "America/Guyana"
time_zone_dict["Greenland"] = "America/Godthab"
time_zone_dict["Mid-Atlantic"] = "Atlantic/South_Georgia"
time_zone_dict["Azores"] = "Atlantic/Azores"
time_zone_dict["Cape Verde Is."] = "Atlantic/Cape_Verde"
time_zone_dict["Dublin"] = "Europe/Dublin"
time_zone_dict["Edinburgh"] = "Europe/London"
time_zone_dict["Lisbon"] = "Europe/Lisbon"
time_zone_dict["London"] = "Europe/London"
time_zone_dict["Casablanca"] = "Africa/Casablanca"
time_zone_dict["Monrovia"] = "Africa/Monrovia"
time_zone_dict["UTC"] = "Etc/UTC"
time_zone_dict["Belgrade"] = "Europe/Belgrade"
time_zone_dict["Bratislava"] = "Europe/Bratislava"
time_zone_dict["Budapest"] = "Europe/Budapest"
time_zone_dict["Ljubljana"] = "Europe/Ljubljana"
time_zone_dict["Prague"] = "Europe/Prague"
time_zone_dict["Sarajevo"] = "Europe/Sarajevo"
time_zone_dict["Skopje"] = "Europe/Skopje"
time_zone_dict["Warsaw"] = "Europe/Warsaw"
time_zone_dict["Zagreb"] = "Europe/Zagreb"
time_zone_dict["Brussels"] = "Europe/Brussels"
time_zone_dict["Copenhagen"] = "Europe/Copenhagen"
time_zone_dict["Madrid"] = "Europe/Madrid"
time_zone_dict["Paris"] = "Europe/Paris"
time_zone_dict["Amsterdam"] = "Europe/Amsterdam"
time_zone_dict["Berlin"] = "Europe/Berlin"
time_zone_dict["Bern"] = "Europe/Zurich"
time_zone_dict["Zurich"] = "Europe/Zurich"
time_zone_dict["Rome"] = "Europe/Rome"
time_zone_dict["Stockholm"] = "Europe/Stockholm"
time_zone_dict["Vienna"] = "Europe/Vienna"
time_zone_dict["West Central Africa"] = "Africa/Algiers"
time_zone_dict["Bucharest"] = "Europe/Bucharest"
time_zone_dict["Cairo"] = "Africa/Cairo"
time_zone_dict["Helsinki"] = "Europe/Helsinki"
time_zone_dict["Kyiv"] = "Europe/Kiev"
time_zone_dict["Riga"] = "Europe/Riga"
time_zone_dict["Sofia"] = "Europe/Sofia"
time_zone_dict["Tallinn"] = "Europe/Tallinn"
time_zone_dict["Vilnius"] = "Europe/Vilnius"
time_zone_dict["Athens"] = "Europe/Athens"
time_zone_dict["Istanbul"] = "Europe/Istanbul"
time_zone_dict["Minsk"] = "Europe/Minsk"
time_zone_dict["Jerusalem"] = "Asia/Jerusalem"
time_zone_dict["Harare"] = "Africa/Harare"
time_zone_dict["Pretoria"] = "Africa/Johannesburg"
time_zone_dict["Kaliningrad"] = "Europe/Kaliningrad"
time_zone_dict["Moscow"] = "Europe/Moscow"
time_zone_dict["St. Petersburg"] = "Europe/Moscow"
time_zone_dict["Volgograd"] = "Europe/Volgograd"
time_zone_dict["Samara"] = "Europe/Samara"
time_zone_dict["Kuwait"] = "Asia/Kuwait"
time_zone_dict["Riyadh"] = "Asia/Riyadh"
time_zone_dict["Nairobi"] = "Africa/Nairobi"
time_zone_dict["Baghdad"] = "Asia/Baghdad"
time_zone_dict["Tehran"] = "Asia/Tehran"
time_zone_dict["Abu Dhabi"] = "Asia/Muscat"
time_zone_dict["Muscat"] = "Asia/Muscat"
time_zone_dict["Baku"] = "Asia/Baku"
time_zone_dict["Tbilisi"] = "Asia/Tbilisi"
time_zone_dict["Yerevan"] = "Asia/Yerevan"
time_zone_dict["Kabul"] = "Asia/Kabul"
time_zone_dict["Ekaterinburg"] = "Asia/Yekaterinburg"
time_zone_dict["Islamabad"] = "Asia/Karachi"
time_zone_dict["Karachi"] = "Asia/Karachi"
time_zone_dict["Tashkent"] = "Asia/Tashkent"
time_zone_dict["Chennai"] = "Asia/Kolkata"
time_zone_dict["Kolkata"] = "Asia/Kolkata"
time_zone_dict["Mumbai"] = "Asia/Kolkata"
time_zone_dict["New Delhi"] = "Asia/Kolkata"
time_zone_dict["Kathmandu"] = "Asia/Kathmandu"
time_zone_dict["Astana"] = "Asia/Dhaka"
time_zone_dict["Dhaka"] = "Asia/Dhaka"
time_zone_dict["Sri Jayawardenepura"] = "Asia/Colombo"
time_zone_dict["Almaty"] = "Asia/Almaty"
time_zone_dict["Novosibirsk"] = "Asia/Novosibirsk"
time_zone_dict["Rangoon"] = "Asia/Rangoon"
time_zone_dict["Bangkok"] = "Asia/Bangkok"
time_zone_dict["Hanoi"] = "Asia/Bangkok"
time_zone_dict["Jakarta"] = "Asia/Jakarta"
time_zone_dict["Krasnoyarsk"] = "Asia/Krasnoyarsk"
time_zone_dict["Beijing"] = "Asia/Shanghai"
time_zone_dict["Chongqing"] = "Asia/Chongqing"
time_zone_dict["Hong Kong"] = "Asia/Hong_Kong"
time_zone_dict["Urumqi"] = "Asia/Urumqi"
time_zone_dict["Kuala Lumpur"] = "Asia/Kuala_Lumpur"
time_zone_dict["Singapore"] = "Asia/Singapore"
time_zone_dict["Taipei"] = "Asia/Taipei"
time_zone_dict["Perth"] = "Australia/Perth"
time_zone_dict["Irkutsk"] = "Asia/Irkutsk"
time_zone_dict["Ulaanbaatar"] = "Asia/Ulaanbaatar"
time_zone_dict["Seoul"] = "Asia/Seoul"
time_zone_dict["Osaka"] = "Asia/Tokyo"
time_zone_dict["Sapporo"] = "Asia/Tokyo"
time_zone_dict["Tokyo"] = "Asia/Tokyo"
time_zone_dict["Yakutsk"] = "Asia/Yakutsk"
time_zone_dict["Darwin"] = "Australia/Darwin"
time_zone_dict["Adelaide"] = "Australia/Adelaide"
time_zone_dict["Canberra"] = "Australia/Melbourne"
time_zone_dict["Melbourne"] = "Australia/Melbourne"
time_zone_dict["Sydney"] = "Australia/Sydney"
time_zone_dict["Brisbane"] = "Australia/Brisbane"
time_zone_dict["Hobart"] = "Australia/Hobart"
time_zone_dict["Vladivostok"] = "Asia/Vladivostok"
time_zone_dict["Guam"] = "Pacific/Guam"
time_zone_dict["Port Moresby"] = "Pacific/Port_Moresby"
time_zone_dict["Magadan"] = "Asia/Magadan"
time_zone_dict["Srednekolymsk"] = "Asia/Srednekolymsk"
time_zone_dict["Solomon Is."] = "Pacific/Guadalcanal"
time_zone_dict["New Caledonia"] = "Pacific/Noumea"
time_zone_dict["Fiji"] = "Pacific/Fiji"
time_zone_dict["Kamchatka"] = "Asia/Kamchatka"
time_zone_dict["Marshall Is."] = "Pacific/Majuro"
time_zone_dict["Auckland"] = "Pacific/Auckland"
time_zone_dict["Wellington"] = "Pacific/Auckland"
time_zone_dict["Nuku'alofa"] = "Pacific/Tongatapu"
time_zone_dict["Tokelau Is."] = "Pacific/Fakaofo"
time_zone_dict["Chatham Is."] = "Pacific/Chatham"
time_zone_dict["Samoa"] = "Pacific/Apia"

count_image = 0
count_media = 0
count_url = 0
count_user_mentions = 0
count_hashtags = 0
count_quote = 0
count_rt = 0
count_image_rt = 0

stop_words = set(stopwords.words('english'))
stop_words.update(
  ('u','https','fakenews','fake','news')
)

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
                  if data['retweet_count'] > 0:
                    count_image_rt = count_image_rt + 1
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
          # get time zone info
          try:
            if data['user']['time_zone'] != "null":
              tweets_time_zones.append(time_zone_dict[data['user']['time_zone']])
          except KeyError:
            pass
          # get account creation info
          if data['user']['id'] not in usernames:
            c = data['user']['created_at'].split()
            accounts_created.append(c[-1])
            usernames.append(data['user']['id'])
      print("Downloaded {0} tweets".format(tweetCount))
      max_id = new_tweets[-1].id
    # error handling
    except tweepy.TweepError as e:
      print("ERROR! : " + str(e))
      break

########## ENTITIES INFORMATION ##########
print ("Downloaded {0} tweets, saved to {1}".format(tweetCount, fName))
print ("{0} tweets contained URLs".format(count_url))
print ("{0} tweets contained images".format(count_image))
print ("{0} tweets contained media other than images".format(count_media))
print ("{0} tweets mentioned other users".format(count_user_mentions))
print ("{0} tweets contained hashtags".format(count_hashtags))
print ("{0} tweets were quote tweets".format(count_quote))

########## IMAGES CONCLUSION ##########
print ("Out of {0} tweets containing images, {1} were retweeted by other users".format(count_image, count_image_rt))
temp = (count_image_rt  * 100.0) / count_image
print ("Only {:f}%% of tweets containing images were retweeted!".format(temp))
print ("Out of {0} tweets, {1} were retweeted by other users".format(tweetCount, count_rt))
temp = ((count_rt - count_image_rt) * 100.0) / (tweetCount - count_image)
print ("However {:f}%% of all tweets except those containing images were retweeted!".format(temp))

########## PROCESSING DATA AND PRINTING ENTITIES GRAPH ##########
keys = ['URLs', 'Images', 'Other media', 'Mentions', 'Hashtags', 'Retweeted', 'Quotes']
height = [6 for i in range(0, 8)]
size = [count_url, count_image, count_media, count_user_mentions, count_hashtags, count_rt, count_quote]
color = ['rgb(213,0,0)', 'rgb(26,35,126)', 'rgb(106,27,154)', 'rgb(118,255,3)', 'rgb(255,196,0)', 'rgb(255,61,0)', 'rgb(33,150,243)']
label = []
for i in range(7):
  s = str.lower(keys[i]) + " : " + str(size[i])
  label.append(s)
plot(
  [go.Scatter(
    x=keys,
    y=height,
    text=label,
    mode='markers',
    marker=dict(
      color=color,
      size=[i/2 for i in size])
  )],
  show_link=False,
  filename='Entities Graph.html',
  image='svg',
  image_filename='bubble'
)

########## PROCESSING DATA AND PLOTTING WORDS HISTOGRAM ##########
words_dict = Counter(tweets_words)
histogram_data = words_dict.most_common(20)
keys = [x[0] for x in histogram_data]
values = [x[1] for x in histogram_data]
plot(
  [go.Bar(
    x=keys,
    y=values
  )],
  show_link=False,
  filename='Words Histogram.html',
  image='svg',
  image_filename='hist'
)

########## PROCESSING DATA AND PLOTTING COUNTRY PIE CHART ##########
countries_dict = Counter(tweets_countries)
pie_data = countries_dict.most_common()
labels = [x[0] for x in pie_data]
values = [x[1] for x in pie_data]
plot(
  [go.Pie(
    labels=labels,
    values=values
  )],
  show_link=False,
  filename='Country Pie Chart.html',
  image='svg',
  image_filename='pie'
)

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
plot(
  [go.Scatter(
    x=keys,
    y=values
  )],
  show_link=False,
  filename='Time Series Graph.html',
  image='svg',
  image_filename='line'
)

########## PROCESSING DATA AND PLOTTING TIMEZONE PIE CHART ##########
time_dict = Counter(tweets_time_zones)
pie2_data = time_dict.most_common()
labels = [x[0] for x in pie2_data]
values = [x[1] for x in pie2_data]
plot(
  [go.Pie(
    labels=labels,
    values=values
  )],
  show_link=False,
  filename='Timezone Pie Chart.html',
  image='svg',
  image_filename='pie2'
)

########## PROCESSING DATES AND PLOTTING ACCOUNT CREATION GRAPH ##########
created_dict = {}
for date in accounts_created:
  if date in created_dict:
    created_dict[date] = created_dict[date] + 1
  else:
    created_dict[date] = 1
created = created_dict.keys()
created_sorted = sorted(created, key=lambda date: datetime.strptime(date, "%Y"))
keys = created_sorted
values = []
for create in created_sorted:
  values.append(created_dict[create])
plot(
  [go.Scatter(
    x=keys,
    y=values
  )],
  show_link=False,
  filename='Account Creation Line Graph.html',
  image='svg',
  image_filename='line2'
)
