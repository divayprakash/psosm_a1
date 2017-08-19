import json
from collections import Counter
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import datetime

with open('data.json') as json_data:
  data = json.load(json_data)

list_hometown = []
list_languages = []
list_birthmonth = []

for record in data:
  list_hometown.append(record['hometown']['name'].encode('utf-8'))
  birthday = record['birthday'].encode('utf-8')
  birthday = birthday.split('/')
  birthmonth = birthday[0]
  list_birthmonth.append(birthmonth)
  for language in record['languages']:
    list_languages.append(language['name'].encode('utf-8'))

hometown_dict = Counter(list_hometown)
pie_data = hometown_dict.most_common()
labels = [x[0] for x in pie_data]
values = [x[1] for x in pie_data]
plot(
  [go.Pie(
    labels=labels,
    values=values
  )],
  show_link=False,
  filename='Hometown Pie Chart.html',
  image='svg',
  image_filename='fb_pie'
)

language_dict = Counter(list_languages)
pie_data = language_dict.most_common()
labels = [x[0] for x in pie_data]
values = [x[1] for x in pie_data]
plot(
  [go.Pie(
    labels=labels,
    values=values
  )],
  show_link=False,
  filename='Language Pie Chart.html',
  image='svg',
  image_filename='fb_pie2'
)

month_mapping = {}
month_mapping["01"] = "January"
month_mapping["02"] = "February"
month_mapping["03"] = "March"
month_mapping["04"] = "April"
month_mapping["05"] = "May"
month_mapping["06"] = "June"
month_mapping["07"] = "July"
month_mapping["08"] = "August"
month_mapping["09"] = "September"
month_mapping["10"] = "October"
month_mapping["11"] = "November"
month_mapping["12"] = "December"

list_birthmonth_name = []
for month in list_birthmonth:
  list_birthmonth_name.append(month_mapping[month])

birthmonth_dict = {}
for month in list_birthmonth_name:
  if month in birthmonth_dict:
    birthmonth_dict[month] = birthmonth_dict[month] + 1
  else:
    birthmonth_dict[month] = 1
months = birthmonth_dict.keys()
months_sorted = sorted(months, key=lambda month: datetime.strptime(month, "%B"))
keys = months_sorted
values = []
for month in months_sorted:
  values.append(birthmonth_dict[month])
plot(
  [go.Scatter(
    x=keys,
    y=values
  )],
  show_link=False,
  filename='Birthday Graph.html',
  image='svg',
  image_filename='fb_line'
)
