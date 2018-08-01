import requests
import json
import datetime

print ('PUBG !!!')

# 조회 기준 유저
target_user = 'KR_MattYoon'
team_users = ['KR_MattYoon', 'ashyuram', 'IrakasaI', 'Sonicss1']

# 팀정보 세팅
team_user_info = {}
for team_user in team_users:
    team_user_info[team_user] = []
print ('Set crew')

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiMTUyOGY4MC02YTIzLTAxMzYtY2YyYS03YjNmNWYzNGQzMmEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTMxNjM1MDI3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InNldmVuX2VsZXZlbiJ9.4hYq6VQAxMBw1-HoJjAwWsZfyqblmP5IP9lrt28666A'
api_url = 'https://api.pubg.com/shards'
region = 'pc-kakao'

# set request info
headers = {'accept': 'application/vnd.api+json', 'authorization': 'Bearer %s' % api_key}
api_url_userinfo = '%s/%s/%s' % (api_url, region, 'players') + '?filter[playerNames]=' + target_user
api_url_matchinfo = '%s/%s/%s' % (api_url, region, 'matches')

print (api_url_userinfo)
print (headers)

# Request user info
res = requests.get(api_url_userinfo, headers=headers)
user_data = json.loads(res.text)

# Get match list
match_list = user_data['data'][0]['relationships']['matches']['data']

# Get match id list
match_id_list = []
for match_basic_info in match_list:
    match_id_list.append(match_basic_info['id'])

print (match_id_list)

for match_id in match_id_list:
    # request match detail info
    res = requests.get(api_url_matchinfo + '/%s' % match_id, headers=headers)
    match_info = json.loads(res.text)
    start_date = match_info['data']['attributes']['createdAt']
    map_name = match_info['data']['attributes']['mapName']
    telemetry_id = match_info['data']['relationships']['assets']['data'][0]['id'] # telemetry id
    # 어제날짜만 계산
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    if not start_date.startswith(yesterday):
        break
    for included_data in match_info['included']:
        # telemetry url 분리
        if included_data['type'] == 'asset' and included_data['id'] == telemetry_id:
            telemetry_url = included_data['attributes']['URL']
        if included_data['type'] == 'participant' and included_data['attributes']['stats']['name'] in team_users:
            team_user_info[included_data['attributes']['stats']['name']].append(included_data['attributes']['stats'])
print ('END')

print ('PLAY DATE : %s' % yesterday)
for user_name in team_users:
    print ('###############')
    print ('user : %s' % user_name)
    count = 0
    sum_damage_dealt = 0
    sum_kills = 0
    sum_headshot_kills = 0
    sum_assists = 0
    sum_heals = 0
    sum_longest_kill = 0
    sum_revives = 0
    sum_time_survived = 0
    count = 0
    max_damage_dealt = 0
    max_kills = 0
    max_headshot_kills = 0
    max_assists = 0
    max_heals = 0
    max_longest_kill = 0
    max_revives = 0
    max_time_survived = 0
    for match_info in team_user_info[user_name]:
        count = count + 1
        sum_damage_dealt = sum_damage_dealt + match_info['damageDealt']
        sum_kills = sum_kills + match_info['kills']
        sum_headshot_kills = sum_headshot_kills + match_info['headshotKills']
        sum_assists = sum_assists + match_info['assists']
        sum_heals = sum_heals + match_info['heals']
        sum_longest_kill = sum_longest_kill + match_info['longestKill']
        sum_revives = sum_revives + match_info['revives']
        sum_time_survived = sum_time_survived + match_info['timeSurvived']
        max_damage_dealt = max_damage_dealt if (max_damage_dealt > match_info['damageDealt']) else match_info['damageDealt']
        max_kills = max_kills if (max_kills > match_info['kills']) else match_info['kills']
        max_headshot_kills = max_headshot_kills if (max_headshot_kills > match_info['headshotKills']) else match_info['headshotKills']
        max_assists = max_assists if (max_assists > match_info['assists']) else match_info['assists']
        max_heals = max_heals if (max_heals > match_info['heals']) else match_info['heals']
        max_longest_kill = max_longest_kill if (max_longest_kill > match_info['longestKill']) else match_info['longestKill']
        max_revives = max_revives if (max_revives > match_info['revives']) else match_info['revives']
        max_time_survived = max_time_survived if (max_time_survived > match_info['timeSurvived']) else match_info['timeSurvived']
    print ('%s : %s' %('gameNum', count))
    # 0판 제외
    if count == 0:
        continue
    print ('%s : %s' % ('damageDealt', sum_damage_dealt))
    print ('%s : %s' % ('kills', sum_kills))
    print ('%s : %s' % ('headshotKills', sum_headshot_kills))
    print ('%s : %s' % ('assists', sum_assists))
    print ('%s : %s' % ('heals', sum_heals))
    print ('%s : %s' % ('longestKill', sum_longest_kill))
    print ('%s : %s' % ('revives', sum_revives))
    print ('%s : %s' % ('timeSurvived', sum_time_survived))
    print ('%s : %s' % ('avg_damageDealt', round(sum_damage_dealt / count, 2)))
    print ('%s : %s' % ('avg_kills', round(sum_kills / count, 2)))
    print ('%s : %s' % ('avg_headshotKills', round(sum_headshot_kills / count, 2)))
    print ('%s : %s' % ('avg_assists', round(sum_assists / count, 2)))
    print ('%s : %s' % ('avg_heals', round(sum_heals / count, 2)))
    print ('%s : %s' % ('avg_longestKill', round(sum_longest_kill / count, 2)))
    print ('%s : %s' % ('avg_revives', round(sum_revives / count, 2)))
    print ('%s : %s' % ('avg_timeSurvived', round(sum_time_survived / 60 / count, 2)))
    print ('%s : %s' % ('max_damage_dealt', max_damage_dealt))
    print ('%s : %s' % ('max_kills', max_kills))
    print ('%s : %s' % ('max_headshot_kills', max_headshot_kills))
    print ('%s : %s' % ('max_assists', max_assists))
    print ('%s : %s' % ('max_heals', max_heals))
    print ('%s : %s' % ('max_longest_kill', max_longest_kill))
    print ('%s : %s' % ('max_revives', max_revives))
    print ('%s : %s' % ('max_time_survived', max_time_survived))

    
print ('end')








# test_url = 'https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/pc-kakao/2018/07/31/14/00/0eb1d3be-94ca-11e8-be0b-0a5864631c2f-telemetry.json'
# res = requests.get(test_url, headers=headers, verify=False)

# print (res)
# print (res.text)

# curl "https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/pc-kakao/2018/07/31/14/00/0eb1d3be-94ca-11e8-be0b-0a5864631c2f-telemetry.json" \
# -H "Accept: application/vnd.api+json"

# curl "https://telemetry-cdn.pubg.com/pc-kakao/2018/07/31/0/0/0eb1d3be-94ca-11e8-be0b-0a5864631c2f-telemetry.json" \
#       -H "Accept: application/vnd.api+json"

