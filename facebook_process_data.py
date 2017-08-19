import json

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

print list_hometown
print list_birthday
print list_languages
