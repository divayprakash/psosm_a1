import config
import json
import facebook
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

client_id = config.facebook['client_id']
client_secret = config.facebook['client_secret']

base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'

redirect_uri = 'https://divayprakash.com/'
scope = ('user_birthday', 'user_hometown', 'user_likes')
fb = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
fb = facebook_compliance_fix(fb)

authorization_url, state = fb.authorization_url(base_url)
print 'Please authorize here: ', authorization_url

redirect_response = raw_input('Please paste the full redirect URL here: ')
result = fb.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

temp = fb.get("https://graph.facebook.com/me?fields=id,name,birthday,languages,hometown")
data = json.loads(temp.content)
print data
