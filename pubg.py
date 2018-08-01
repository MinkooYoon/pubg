import requests
import json

print ('PUBG !!!')

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiMTUyOGY4MC02YTIzLTAxMzYtY2YyYS03YjNmNWYzNGQzMmEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTMxNjM1MDI3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InNldmVuX2VsZXZlbiJ9.4hYq6VQAxMBw1-HoJjAwWsZfyqblmP5IP9lrt28666A'
api_url = 'https://api.pubg.com/shards'
region = 'pc-kakao'

headers = {'accept': 'application/vnd.api+json', 'authorization': 'Bearer %s' % api_key}

api_url_userinfo = '%s/%s/%s' % (api_url, region, 'players') + '?filter[playerNames]=' + 'KR_MattYoon'

print (api_url_userinfo)
print (headers)

# Get user info
res = requests.get(api_url_userinfo, headers=headers)
user_data = json.loads(res.text)

# Get match list
match_list = user_data['data'][0]['relationships']['matches']['data']
