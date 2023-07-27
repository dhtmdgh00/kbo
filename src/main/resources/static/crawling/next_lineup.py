from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import numpy as np


def reset_crawl():
    global game_dates
    global game_infos

    global teams_hm
    global teams_aw

    global pitcher_hm
    global pitcher_aw
    
    game_dates = []
    game_infos = []

    teams_hm = []
    teams_aw = []

    pitcher_hm = []
    pitcher_aw = []


game_dates = []
game_infos = []

teams_hm = []
teams_aw = []

pitcher_hm = []
pitcher_aw = []

hit_cols = ['hitman_hm_1','hitman_hm_2',
            'hitman_hm_3','hitman_hm_4','hitman_hm_5',
            'hitman_hm_6','hitman_hm_7','hitman_hm_8',
            'hitman_hm_9',
            
            'hitman_aw_1','hitman_aw_2',
            'hitman_aw_3','hitman_aw_4','hitman_aw_5',
            'hitman_aw_6','hitman_aw_7','hitman_aw_8',
            'hitman_aw_9']

home = ['hitman_hm_1','hitman_hm_2',
            'hitman_hm_3','hitman_hm_4','hitman_hm_5',
            'hitman_hm_6','hitman_hm_7','hitman_hm_8',
            'hitman_hm_9']

away = ['hitman_aw_1','hitman_aw_2',
            'hitman_aw_3','hitman_aw_4','hitman_aw_5',
            'hitman_aw_6','hitman_aw_7','hitman_aw_8',
            'hitman_aw_9']

def get_lineup(url):

    lineup_url = 'https://api-gw.sports.naver.com/schedule/games/' + url + '/preview' # 라인업
    result_url = 'https://api-gw.sports.naver.com/schedule/games/' +  url             # 결과

    response = requests.get(lineup_url).json()

    game_date = response['result']['previewData']['gameInfo']['gdate']
    team_hm = response['result']['previewData']['gameInfo']['hFullName']
    team_aw = response['result']['previewData']['gameInfo']['aFullName']
    players_hm = response['result']['previewData']['homeTeamLineUp']['fullLineUp']
    players_aw = response['result']['previewData']['awayTeamLineUp']['fullLineUp']

    game_info = requests.get(result_url).json()['result']['game']

    return game_info, game_date, team_hm, team_aw, players_aw, players_hm


def get_lineup(url):

    lineup_url = 'https://api-gw.sports.naver.com/schedule/games/' + url + '/preview' # 라인업
    result_url = 'https://api-gw.sports.naver.com/schedule/games/' +  url             # 결과

    response = requests.get(lineup_url).json()

    game_date = response['result']['previewData']['gameInfo']['gdate']
    team_hm = response['result']['previewData']['gameInfo']['hCode']
    team_aw = response['result']['previewData']['gameInfo']['aCode']
    pit_hm = response['result']['previewData']['gameInfo']['hPCode']
    pit_aw = response['result']['previewData']['gameInfo']['aPCode']


    return game_date, team_hm, team_aw, pit_hm, pit_aw
    
def start_crawl(urls):

    for url in urls:
        game_date, team_hm, team_aw, pit_hm, pit_aw = get_lineup(url)
    
        game_dates.append(str(game_date))

        teams_hm.append(team_hm)
        teams_aw.append(team_aw)
        
        pitcher_hm.append(str(pit_hm))
        pitcher_aw.append(str(pit_aw))



today_datetime = datetime.now()
today_date = today_datetime.strftime("%Y%m%d")

#today_datetime = (datetime.now() + timedelta(days=30))
#today_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")



today_year = int(today_date[:4])
today_month = int(today_date[4:6])
today_day = int(today_date[6:])

# return할 리스트
urls = []

all_url = f'https://sports.news.naver.com/kbaseball/schedule/index?month={today_month}&year={today_year}&teamCode='

response = requests.get(all_url)
soup = BeautifulSoup(response.text, 'html.parser')
x = soup.find_all('span', class_ = 'td_btn')


for line in x:
    url = line.find('a')['href'][6:-7]

    if int(url[:8]) == int(today_date):
        if not url in urls:
            urls.append(url)



if len(urls) == 0:
    tomorrow = (today_datetime + timedelta(days=1)).strftime("%Y%m%d")
    for line in x:
        url = line.find('a')['href'][6:-7]

        if int(url[:8]) == int(tomorrow):
            if not url in urls:
                urls.append(url)    



if not len(urls) == 0:
    reset_crawl()
    start_crawl(urls)
    
    col_names = ['game_dates', 'teams_hm', 'teams_aw', 'pitcher_hm', 'pitcher_aw']
    
    df = pd.DataFrame(list(zip(game_dates, teams_hm , teams_aw, pitcher_hm, pitcher_aw)),columns = col_names)
    
    for i in hit_cols:
        df[i] = 0
    
    lineup = pd.read_csv('BASE_lineup.csv')
    lineup = lineup.sort_values('game_dates', ascending=False).reset_index()
    
    ALL_TRUE = {'SK' : False, 'LG' : False, 'HH' : False, 'WO' : False, 'SS' : False, 'HT' : False, 'KT' : False, 'LT' : False, 'NC' : False, 'OB' : False}

    i = 0
    
    while True:
        if lineup.iloc[i]['homeTeamCode'] in ALL_TRUE.keys():
            if ALL_TRUE[lineup.iloc[i]['homeTeamCode']] == False:
                
                indices = df.loc[(df['teams_hm'] == lineup.iloc[i]['homeTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], home] = list(lineup.iloc[i]['hitman_hm_1':'hitman_hm_9'])
                    ALL_TRUE[lineup.iloc[i]['homeTeamCode']] = True
        
                indices = df.loc[(df['teams_aw'] == lineup.iloc[i]['homeTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], away] = list(lineup.iloc[i]['hitman_hm_1':'hitman_hm_9'])
                    ALL_TRUE[lineup.iloc[i]['homeTeamCode']] = True
                    
        
        if lineup.iloc[i]['awayTeamCode'] in ALL_TRUE.keys():
            if ALL_TRUE[lineup.iloc[i]['awayTeamCode']] == False:
                
                indices = df.loc[(df['teams_hm'] == lineup.iloc[i]['awayTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], home] = list(lineup.iloc[i]['hitman_aw_1':'hitman_aw_9'])
                    ALL_TRUE[lineup.iloc[i]['awayTeamCode']] = True
    
    
                    
                indices = df.loc[(df['teams_aw'] == lineup.iloc[i]['awayTeamCode'])].index
                if len(indices) == 1:
                    df.loc[indices[0], away] = list(lineup.iloc[i]['hitman_aw_1':'hitman_aw_9'])
                    ALL_TRUE[lineup.iloc[i]['awayTeamCode']] = True
        i += 1
        if len(urls)*2 == list(ALL_TRUE.values()).count(True):
            break
    
    
else:
    df = pd.DataFrame(columns = ['game_dates', 'teams_hm', 'teams_aw', 'pitcher_hm', 'pitcher_aw',
       'hitman_hm_1', 'hitman_hm_2', 'hitman_hm_3', 'hitman_hm_4',
       'hitman_hm_5', 'hitman_hm_6', 'hitman_hm_7', 'hitman_hm_8',
       'hitman_hm_9', 'hitman_aw_1', 'hitman_aw_2', 'hitman_aw_3',
       'hitman_aw_4', 'hitman_aw_5', 'hitman_aw_6', 'hitman_aw_7',
       'hitman_aw_8', 'hitman_aw_9'])



if len(list(df['pitcher_aw'])) == 0:
    df = pd.DataFrame( columns = ['game_dates', 'teams_hm', 'teams_aw', 'pitcher_hm', 'pitcher_aw',
       'hitman_hm_1', 'hitman_hm_2', 'hitman_hm_3', 'hitman_hm_4',
       'hitman_hm_5', 'hitman_hm_6', 'hitman_hm_7', 'hitman_hm_8',
       'hitman_hm_9', 'hitman_aw_1', 'hitman_aw_2', 'hitman_aw_3',
       'hitman_aw_4', 'hitman_aw_5', 'hitman_aw_6', 'hitman_aw_7',
       'hitman_aw_8', 'hitman_aw_9'])


df.to_csv('tomorrow_lineup.csv')
df = pd.read_csv('tomorrow_lineup.csv')
df.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
df['idx'] = df['idx']+1
df['idx'] = df['idx'].apply(lambda x: str(x).zfill(6))
df.to_csv('tomorrow_lineup.csv',index = False)


df = pd.read_csv('tomorrow_lineup.csv')
hit = df[[
       'hitman_hm_1', 'hitman_hm_2', 'hitman_hm_3', 'hitman_hm_4',
       'hitman_hm_5', 'hitman_hm_6', 'hitman_hm_7', 'hitman_hm_8',
       'hitman_hm_9', 'hitman_aw_1', 'hitman_aw_2', 'hitman_aw_3',
       'hitman_aw_4', 'hitman_aw_5', 'hitman_aw_6', 'hitman_aw_7',
       'hitman_aw_8', 'hitman_aw_9']]

pit = df[['pitcher_hm', 'pitcher_aw']]

hit_code = list(set(hit.values.flatten().tolist()))
pit_code = list(set(pit.values.flatten().tolist()))

Basedf_pit = pd.read_csv('DB_pit.csv')
Basedf_hit = pd.read_csv('DB_hit.csv')

Basedf_pit = Basedf_pit.groupby('code').tail(5).reset_index(drop=True)
Basedf_pit = Basedf_pit.groupby('code').filter(lambda x: x['code'].iloc[0] in pit_code)

Basedf_hit = Basedf_hit.groupby('code').tail(5).reset_index(drop=True)
Basedf_hit = Basedf_hit.groupby('code').filter(lambda x: x['code'].iloc[0] in hit_code)

Basedf_pit = Basedf_pit.drop(['idx'], axis = 1)
Basedf_hit = Basedf_hit.drop(['idx'], axis = 1)

Basedf_pit['out'] = Basedf_pit['ip'].apply(int) *3 + (Basedf_pit['ip'] - Basedf_pit['ip'].apply(int))*10

pit_5days = Basedf_pit.groupby(['code']).sum()
pit_5days['count'] = list(Basedf_pit.groupby(['code']).size().reset_index()[0])

pit_5days['bbb'] = pit_5days['bb'].replace(0,1)


pit_5days['era'] = round(pit_5days['er'] * 9 / (pit_5days['out'] / 3), 2)
pit_5days['kpit'] = round(pit_5days['k'] / pit_5days['pit'], 3)
pit_5days['kbb'] = round(pit_5days['k'] / pit_5days['bbb'], 3)
pit_5days['whip'] = round( (pit_5days['hit'] + pit_5days['ibb']+ pit_5days['hbp']+ pit_5days['bb']) /  (pit_5days['out'] / 3),3)
pit_5days['wpa'] = round(Basedf_pit.groupby(['code'])['wpa'].median(), 3)
pit_5days['re24'] = round(Basedf_pit.groupby(['code'])['re24'].median(), 3)

pit_5days = pit_5days.reset_index()
pit_5days = pit_5days[['code','era', 'kpit', 'kbb', 'wpa', 're24', 'whip']]

pit_5days.to_csv('pit_recent.csv')
pit_5days = pd.read_csv('pit_recent.csv')
pit_5days.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
pit_5days['idx'] = pit_5days['idx']+1
pit_5days['idx'] = pit_5days['idx'].apply(lambda x: str(x).zfill(6))
pit_5days.to_csv('pit_recent.csv',index = False)

hit_5days = Basedf_hit.groupby(['code']).sum()
hit_5days['count'] = list(Basedf_hit.groupby(['code']).size().reset_index()[0])

hit_5days['ab'] = hit_5days['pa']
hit_5days['pa'] = hit_5days['ab'] + hit_5days['bb'] + hit_5days['hbp'] + hit_5days['ibb'] + hit_5days['sh'] + hit_5days['sf']
hit_5days['kk'] = hit_5days['k'].replace(0,1)


hit_5days['avg'] = round(hit_5days['hit'] / hit_5days['ab'], 3)
hit_5days['slg'] = round( (hit_5days['hit'] + hit_5days['second'] + hit_5days['third']*2 +hit_5days['homerun']*3) / hit_5days['ab'], 3)
hit_5days['obp'] = round( ( (hit_5days['hit'] + hit_5days['bb'] + hit_5days['ibb'] + hit_5days['hbp']) / hit_5days['pa'] ), 3)
hit_5days['bbk'] = round( hit_5days['bb'] / hit_5days['kk'] , 3)
hit_5days['wpa'] = round(Basedf_hit.groupby(['code'])['wpa'].median(), 3)
hit_5days['re24'] = round(Basedf_hit.groupby(['code'])['re24'].median(), 3)

hit_5days = hit_5days.reset_index()
hit_5days = hit_5days[['code','avg', 'slg', 'bbk', 'wpa', 're24', 'obp']]

hit_5days.to_csv('hit_recent.csv')
hit_5days = pd.read_csv('hit_recent.csv')
hit_5days.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
hit_5days['idx'] = hit_5days['idx']+1
hit_5days['idx'] = hit_5days['idx'].apply(lambda x: str(x).zfill(6))
hit_5days.to_csv('hit_recent.csv',index = False)

def total_score(code):
    global DB

    L = list(DB[DB['code'] == code].reset_index().iloc[0])[3:]
    
    max = [ 0.300, 0.478, 0.780, 0, 0, 0.376]
    min = [ 0.214, 0.288, 0.242, -0.013, -0.245, 0.272]
        
    sc = []
        
    for i, n in enumerate(L):
        if n < min[i]:
            n = min[i]
        elif n > max[i]:
            n = max[i]
        
        x = round((n- min[i]) * (8 / (max[i] - min[i])) + 1, 2)
        sc.append(x)
    return sum(sc)
    
df = pd.read_csv('tomorrow_lineup.csv')
DB = pd.read_csv('hit_recent.csv')
DB['score'] = DB['code'].apply(total_score)

key_hm = []
key_aw = []

key_hm_avg = []
key_aw_avg = []

key_hm_slg = []
key_aw_slg = []

key_hm_obp = []
key_aw_obp = []



for i in range(len(df)):
    hm = list(df.iloc[i])[6:15]
    aw = list(df.iloc[i])[15:]

    for j, players in enumerate([hm, aw]):
        num = 0
        for player in players:
            x = DB[DB['code'] == player]['score'].values[0]
            if x > num:
                keyplayer = player
                num = x
            elif x == num:
                if  x> DB[DB['code'] == keyplayer]['avg'].values[0]:
                    keyplayer = player
                    
                
        if j == 0:
            key_hm.append(keyplayer)
            key_hm_avg.append(DB[DB['code'] == keyplayer]['avg'].values[0])
            key_hm_slg.append(DB[DB['code'] == keyplayer]['slg'].values[0])
            key_hm_obp.append(DB[DB['code'] == keyplayer]['obp'].values[0])
            
        else:
            key_aw.append(keyplayer)
            key_aw_avg.append(DB[DB['code'] == keyplayer]['avg'].values[0])
            key_aw_slg.append(DB[DB['code'] == keyplayer]['slg'].values[0])
            key_aw_obp.append(DB[DB['code'] == keyplayer]['obp'].values[0])


df['key_hm'] = key_hm
df['key_hm_avg'] = key_hm_avg
df['key_hm_slg'] = key_hm_slg
df['key_hm_obp'] =key_hm_obp
df['key_aw'] = key_aw
df['key_aw_avg'] =  key_aw_avg
df['key_aw_slg'] = key_aw_slg
df['key_aw_obp'] = key_aw_obp   



teamswins={
    'SK_winlose' : '',
'LG_winlose' : '',
'HH_winlose'  : '',
'WO_winlose'  : '',
'SS_winlose'  : '',
'HT_winlose'  : '',
'KT_winlose'  : '',
'LT_winlose'  : '',
'NC_winlose'  : '',
'OB_winlose'  : ''}

teams = []

for i in range(len(df)):
    teams.append(df.iloc[i]['teams_hm'])
    teams.append(df.iloc[i]['teams_aw'])

lineup = pd.read_csv('BASE_lineup.csv')
lineup = lineup.sort_values('game_dates', ascending=False).reset_index()
lineup['win'] = np.where(lineup['hm_R'] > lineup['aw_R'], 'home', np.where(lineup['hm_R'] < lineup['aw_R'], 'away', 'draw'))

for teamcode in teams:
    teamrecode = lineup[(lineup['homeTeamCode'] == teamcode) | (lineup['awayTeamCode'] == teamcode)].reset_index(drop =True)[:5][['homeTeamCode','awayTeamCode','hm_R','aw_R','win']]
    for i in range(len(teamrecode)):
        if teamrecode.iloc[i]['homeTeamCode'] == teamcode:
            if teamrecode.iloc[i]['win'] == 'home':       
                teamswins[f'{teamcode}_winlose'] += 'W'
            elif teamrecode.iloc[i]['win'] == 'draw':       
                teamswins[f'{teamcode}_winlose'] += 'D'
                
            else:
                teamswins[f'{teamcode}_winlose'] += 'L'
        else:
            if teamrecode.iloc[i]['win'] == 'away':
                teamswins[f'{teamcode}_winlose'] += 'W'
            elif teamrecode.iloc[i]['win'] == 'draw':       
                teamswins[f'{teamcode}_winlose'] += 'D'
            else:
                teamswins[f'{teamcode}_winlose'] += 'L'


df['idx'] = df['idx'].apply(lambda x: str(x).zfill(6))


lineup['game_dates'] = lineup['game_dates'].astype(str)
present = lineup[lineup['game_dates'].str[:4] == str(today_year)]

teaminfo = {}
for i in range(len(df)):
    hmcode = df.iloc[i]['teams_hm'] 
    awcode = df.iloc[i]['teams_aw'] 

    teaminfo[f'{hmcode}'] = {}
    teaminfo[f'{awcode}'] = {}

for teamcode in teaminfo.keys():
    
    team_present = present[(present['awayTeamCode'] == teamcode) | (present['homeTeamCode'] == teamcode)].reset_index(drop= True)
    
    득점 = 0
    실점 = 0
    승수 = 0
    무승부 = 0
    경기수 = len(team_present)
    
    for i in range(len(team_present)):
        if team_present.iloc[i]['awayTeamCode'] == teamcode:
            득점 += team_present.iloc[i]['aw_R']
            실점 += team_present.iloc[i]['hm_R']
            if team_present.iloc[i]['win'] == 'away':
                승수 += 1
            elif team_present.iloc[i]['win'] == 'draw':
                경기수 -= 1
                무승부 +=1
        else :
            득점 += team_present.iloc[i]['hm_R']
            실점 += team_present.iloc[i]['aw_R']
            if team_present.iloc[i]['win'] == 'home':
                승수 += 1
            elif team_present.iloc[i]['win'] == 'draw':
                경기수 -= 1        
                무승부 += 1
        
    teaminfo[f'{teamcode}']['odds'] = round(승수/경기수,3)
    teaminfo[f'{teamcode}']['win'] = 승수
    teaminfo[f'{teamcode}']['draw'] = 무승부
    teaminfo[f'{teamcode}']['lose'] = 경기수-승수
    teaminfo[f'{teamcode}']['getscore'] = round(득점/len(team_present),2)
    teaminfo[f'{teamcode}']['conceded'] = round(실점/len(team_present),2)

for i in range(len(df)):
    hmcode = df.iloc[i]['teams_hm']
    awcode = df.iloc[i]['teams_aw']
    
    홈승 = 0
    홈패 = 0
    무 = 0
    
    vs_present = present[((present['awayTeamCode'] == hmcode) & (present['homeTeamCode'] == awcode)) |  ((present['awayTeamCode'] == awcode) & (present['homeTeamCode'] == hmcode))].reset_index(drop= True)
    
    for i in range(len(vs_present)):
        if vs_present.iloc[i]['awayTeamCode'] == hmcode:
            if vs_present.iloc[i]['win'] == 'away':
                홈승 += 1
            elif vs_present.iloc[i]['win'] == 'draw':
                무 += 1
            else:
                홈패 += 1
        else:
            if vs_present.iloc[i]['win'] == 'home':
                홈승 += 1
            elif vs_present.iloc[i]['win'] == 'draw':
                무 += 1
            else:
                홈패 += 1
                
    teaminfo[f'{hmcode}']['versus'] = str(홈승)+'W '+str(무)+'D '+str(홈패)+'L'
    teaminfo[f'{awcode}']['versus'] = str(홈패)+'W '+str(무)+'D '+str(홈승)+'L'


hm_odds = []
hm_getscore = []
hm_conceded = []
hm_versus = []

aw_odds = []
aw_getscore = []
aw_conceded = []
aw_versus = []

hm_winlose = []
aw_winlose = []

hm_win = []
hm_draw = []
hm_lose = []

aw_win = []
aw_draw = []
aw_lose = []

for i in range(len(df)):
    hmcode = df.iloc[i]['teams_hm']
    awcode = df.iloc[i]['teams_aw']
    hm_WL = teamswins[f'{hmcode}_winlose']
    aw_WL = teamswins[f'{awcode}_winlose']
    hm_winlose.append(hm_WL)
    aw_winlose.append(aw_WL)

for i in range(len(df)):
    hmcode = df.iloc[i]['teams_hm']
    awcode = df.iloc[i]['teams_aw']

    hm_odds.append(teaminfo[f'{hmcode}']['odds'])
    hm_getscore.append(teaminfo[f'{hmcode}']['getscore'])
    hm_conceded.append(teaminfo[f'{hmcode}']['conceded'])
    hm_versus.append(teaminfo[f'{hmcode}']['versus'])

    hm_win.append(teaminfo[f'{hmcode}']['win'])
    hm_draw.append(teaminfo[f'{hmcode}']['draw'])
    hm_lose.append(teaminfo[f'{hmcode}']['lose'])
    
    aw_odds.append(teaminfo[f'{awcode}']['odds'])
    aw_getscore.append(teaminfo[f'{awcode}']['getscore'])
    aw_conceded.append(teaminfo[f'{awcode}']['conceded'])
    aw_versus.append(teaminfo[f'{awcode}']['versus'])

    aw_win.append(teaminfo[f'{awcode}']['win'])
    aw_draw.append(teaminfo[f'{awcode}']['draw'])
    aw_lose.append(teaminfo[f'{awcode}']['lose'])

df['hm_winlose'] = hm_winlose
df['hm_versus'] = hm_versus
df['hm_win'] = hm_win
df['hm_draw'] = hm_draw
df['hm_lose'] = hm_lose

df['aw_winlose'] = aw_winlose
df['aw_versus'] = aw_versus
df['aw_win'] =  aw_win
df['aw_draw'] = aw_draw
df['aw_lose'] = aw_lose

df['hm_odds'] = hm_odds
df['hm_getscore'] = hm_getscore
df['hm_conceded'] = hm_conceded

df['aw_odds'] = aw_odds
df['aw_getscore'] = aw_getscore
df['aw_conceded'] = aw_conceded

df['idx'] = df['idx'].apply(lambda x: str(x).zfill(6))

df.to_csv('tomorrow_lineup.csv',index = False)
