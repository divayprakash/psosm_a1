import json
from collections import Counter
import plotly
from plotly.offline import plot
import plotly.graph_objs as go

with open('data.json') as json_data:
  data = json.load(json_data)

list_hometown = []
list_languages = []
list_birthday = []

for record in data:
  list_hometown.append(record['hometown']['name'].encode('utf-8'))
  list_birthday.append(record['birthday'].encode('utf-8'))
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
