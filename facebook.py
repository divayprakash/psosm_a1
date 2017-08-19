########## IMPORTS ##########
import config  # external configuration file with API keys
import json
import facebook
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

client_id = config.facebook['client_id']
client_secret = config.facebook['client_secret']

fb = OAuth2Session(client_id, redirect_uri='https://divayprakash.com/', scope=('user_birthday', 'user_hometown', 'user_likes'))
fb = facebook_compliance_fix(fb)

authorization_url, state = fb.authorization_url('https://www.facebook.com/dialog/oauth')
print 'Please authorize here: ', authorization_url

redirect = raw_input('Redirect URL here: ')
result = fb.fetch_token('https://graph.facebook.com/oauth/access_token', client_secret=client_secret, authorization_response=redirect)

unset = fb.get("https://graph.facebook.com/me?fields=id,name,birthday,languages,hometown")
data = json.loads(unset.content)
print data
