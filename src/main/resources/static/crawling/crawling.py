### import Library ###
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')


### 크롤링 리셋 ###
game_dates = []
game_infos = []

teams_hm = []
teams_aw = []

pitcher_hm = []
pitcher_aw = []

hitman_hm_1 = []
hitman_hm_2 = []
hitman_hm_3 = []
hitman_hm_4 = []
hitman_hm_5 = []
hitman_hm_6 = []
hitman_hm_7 = []
hitman_hm_8 = []
hitman_hm_9 = []

hitman_aw_1 = []
hitman_aw_2 = []
hitman_aw_3 = []
hitman_aw_4 = []
hitman_aw_5 = []
hitman_aw_6 = []
hitman_aw_7 = []
hitman_aw_8 = []
hitman_aw_9 = []

invalid_urls = []

player_Id = []

urls_hits = []
urls_pits = []

cnt = 0

player_info = {}

def reset_crawl():
    global game_dates
    global game_infos

    global teams_hm
    global teams_aw

    global pitcher_hm
    global pitcher_aw

    global hitman_hm_1
    global hitman_hm_2
    global hitman_hm_3
    global hitman_hm_4
    global hitman_hm_5
    global hitman_hm_6
    global hitman_hm_7
    global hitman_hm_8
    global hitman_hm_9

    global hitman_aw_1
    global hitman_aw_2
    global hitman_aw_3
    global hitman_aw_4
    global hitman_aw_5
    global hitman_aw_6
    global hitman_aw_7
    global hitman_aw_8
    global hitman_aw_9

    global invalid_urls
    global player_Id
    global urls_hits
    global urls_pits

    global cnt

    game_dates = []
    game_infos = []

    teams_hm = []
    teams_aw = []

    pitcher_hm = []
    pitcher_aw = []

    hitman_hm_1 = []
    hitman_hm_2 = []
    hitman_hm_3 = []
    hitman_hm_4 = []
    hitman_hm_5 = []
    hitman_hm_6 = []
    hitman_hm_7 = []
    hitman_hm_8 = []
    hitman_hm_9 = []

    hitman_aw_1 = []
    hitman_aw_2 = []
    hitman_aw_3 = []
    hitman_aw_4 = []
    hitman_aw_5 = []
    hitman_aw_6 = []
    hitman_aw_7 = []
    hitman_aw_8 = []
    hitman_aw_9 = []

    player_Id = []
    urls_hits = []
    urls_pits = []

    invalid_urls=[]

    cnt = 0


### 예외처리 dict
code_birth = {
    ### 네이버 - birth가 누락
    '64153' : '19910715', # '양석환'
    '69366' : '20000103', # '이명기'
    '65357' : '19960829', # '송성문'
    '53404' : '20041011', # '류승민'
    '66606' : '19970323', # '최원준'
    '69745' : '20000915', # 김도현

    ### 네이버 - birth가 실제로 다름
    '52405' : '20031002',  # '조민성'
    '69640' : '19920521',  # '터너'
    '50558' : '19881201',  # '스트레일리'
    '52720' : '19900225',   # '페냐'
    '53716' : '19930908' # 윌리엄스
    
    }

code_back = {
    '53716' : 3 # 윌리엄스
}

code_name = {
    ### 개명자 명단
    '62895' : '한유섬', # '한동민'
    '67539' : '나균안', # '나종덕'
    '64717' : '지시완', # '지성준'
    '63559' : '백동훈', # '백민기'
    '66702' : '이시원', # '이동훈'
    '63905' : '윤형준', # '윤대영'
    '67207' : '이유찬', # '이병휘'
    '69702' : '김건',   # 김현민
    '62920' : '노건우', # '노성호'
    '62360' : '김태훈', # '김동준'
    '64768' : '조이현', # '조영우'
    '50815' : '킹엄',  # '킹험'
    '63894' : '김사윤', # '김정빈'
    '63292' : '박종기', # '박소준'
    '69745' : '김도현',  # '김이환'
    '78753' : '김사연',  # 김지열
    '77462' : '김동명',  #'김동욱'
    '60100' : '백진우'   #'백창수
    }

### 타자,투수 열 이름
cols_hit = ['name', 'code', 'year', 'date', 'vs', 'result', 'h_order', 'position',
            'startup', 'pa', 'run', 'hit', 'second', 'third', 'homerun',
            'luta', 'rbi', 'sb_s', 'sb_f', 'bb', 'hbp', 'ibb', 'k', 'dp',
            'sh', 'sf', 'avg', 'obp', 'slg', 'ops', 'pit', 'avli', 're24', 'wpa']

cols_pit =['name', 'code', 'year', 'date', 'vs', 'result', 'startup', 'ip', 'run', 
                   'er', 'bf', 'ab', 'hit','second', 'third', 'homerun', 'bb',
                   'ibb', 'hbp', 'k', 'pit' ,'whip','avg', 'obp', 'ops', 'era', 
                   'avli', 're24', 'wpa', 'gsc', 'decision', 'itv']




### 어제날짜로 라인업 url 가져오기
def get_update_lineup_urls(update_date):

    #### 업데이트 날짜, 오늘날짜 가져오기 ####
    today = datetime.now().strftime("%Y%m%d")

    today_year = int(today[:4])
    today_month = int(today[4:6])
    today_day = int(today[6:])

    update_year = int(update_date[:4])
    update_month = int(update_date[4:6])
    update_day = int(update_date[6:])

    # return할 리스트
    urls = []

    #### 업데이트 날짜가 올해면, 업뎃 month ~ 오늘 month ####
    #### 업데이트 날짜가 올해가 아니면, 일단 1월부터 12월까지 전부 가져오기 ####
    for year in range(update_year,today_year+1):
        rangemonth_start = 1
        rangemonth_end = 13
        
        if update_year == today_year:
            rangemonth_start = update_month
            rangemonth_end = today_month+1
            

    #### year, month당 for문으로 라인업 링크 크롤링 ####
        for month in range(rangemonth_start,rangemonth_end):
            all_url = f'https://sports.news.naver.com/kbaseball/schedule/index?month={month}&year={year}&teamCode='

            response = requests.get(all_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            x = soup.find_all('span', class_ = 'td_btn')

            for line in x:
                url = line.find('a')['href'][6:-7]

                ### 업데이트를 17일 12시에 했으면 16일 경기까지 있을테니,
                ### 17일경기는 추가해야함 ( <= )사용
                ### 오늘경기는 시작전이니 ( < )사용

                if  int(update_date) <= int(url[:8]) < int(today):
                    if not url in urls:
                        urls.append(url)

        time.sleep(1)
    ###################################
    return urls

### 라인업 url에서 라인업/결과 데이터 크롤링하는 코드
### 리턴은 game_info['seasonYear'] = season =! 0 이어야하고,
### game_date, team_hm, team_aw, players_aw, players_hm 리턴
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





### 플레이어 정보 딕셔너리로

def get_player_info(dict):
    global player_info
    
    dcode = dict['playerCode']
    dbacknum = dict['backnum']
    dname = dict['playerName']
    dbirth = dict['birth']

    if dcode in code_birth.keys():
        dbirth = code_birth[dcode]

    if dcode in code_name.keys():
        dname = code_name[dcode]

    if dcode in code_back.keys():
        dbacknum = code_back[dcode]
    

    player_info[dcode] = [dbacknum,dname,dcode, dbirth,'-']



    

### 라인업 크롤링 시작하는 코드
def start_crawl(urls):

    reset_crawl()

    for url in urls:
        game_info, game_date, team_hm, team_aw, players_aw, players_hm = get_lineup(url)

        for playerdict in players_aw:
            get_player_info(playerdict)
            
        for playerdict in players_hm:
            get_player_info(playerdict)
            

        if not game_info['seasonYear'] == 0 : ## season 코드
            if len(players_hm) == 10 & len(players_aw) == 10:
                game_dates.append(str(game_date))
                game_infos.append(game_info)

                teams_hm.append(team_hm)
                teams_aw.append(team_aw)

                pitcher_hm.append(str(players_hm[0]['playerCode']))
                pitcher_aw.append(str(players_aw[0]['playerCode']))

                hitman_hm_1.append(str(players_hm[1]['playerCode']))
                hitman_hm_2.append(str(players_hm[2]['playerCode']))
                hitman_hm_3.append(str(players_hm[3]['playerCode']))
                hitman_hm_4.append(str(players_hm[4]['playerCode']))
                hitman_hm_5.append(str(players_hm[5]['playerCode']))
                hitman_hm_6.append(str(players_hm[6]['playerCode']))
                hitman_hm_7.append(str(players_hm[7]['playerCode']))
                hitman_hm_8.append(str(players_hm[8]['playerCode']))
                hitman_hm_9.append(str(players_hm[9]['playerCode']))

                hitman_aw_1.append(str(players_aw[1]['playerCode']))
                hitman_aw_2.append(str(players_aw[2]['playerCode']))
                hitman_aw_3.append(str(players_aw[3]['playerCode']))
                hitman_aw_4.append(str(players_aw[4]['playerCode']))
                hitman_aw_5.append(str(players_aw[5]['playerCode']))
                hitman_aw_6.append(str(players_aw[6]['playerCode']))
                hitman_aw_7.append(str(players_aw[7]['playerCode']))
                hitman_aw_8.append(str(players_aw[8]['playerCode']))
                hitman_aw_9.append(str(players_aw[9]['playerCode']))
            else:
                invalid_urls.append(f'https://m.sports.naver.com/game/{url}/record')

        if cnt % 50 == 49:
            time.sleep(5)


    return [game_dates,game_infos,teams_hm,teams_aw,pitcher_hm,pitcher_aw,hitman_hm_1,hitman_hm_2,hitman_hm_3,hitman_hm_4,hitman_hm_5,hitman_hm_6,hitman_hm_7,hitman_hm_8,hitman_hm_9,hitman_aw_1,hitman_aw_2,hitman_aw_3,hitman_aw_4,hitman_aw_5,hitman_aw_6,hitman_aw_7,hitman_aw_8,hitman_aw_9]




### 라인업 DF 만드는 코드
def make_df(data):
    game_dates = data[0]
    game_infos = data[1]
    teams_hm = data[2]
    teams_aw = data[3]
    pitcher_hm = data[4]
    pitcher_aw = data[5]
    hitman_hm_1 = data[6]
    hitman_hm_2 = data[7]
    hitman_hm_3 = data[8]
    hitman_hm_4 = data[9]
    hitman_hm_5 = data[10]
    hitman_hm_6 = data[11]
    hitman_hm_7 = data[12]
    hitman_hm_8 = data[13]
    hitman_hm_9 = data[14]
    hitman_aw_1 = data[15]
    hitman_aw_2 = data[16]
    hitman_aw_3 = data[17]
    hitman_aw_4 = data[18]
    hitman_aw_5 = data[19]
    hitman_aw_6 = data[20]
    hitman_aw_7 = data[21]
    hitman_aw_8 = data[22]
    hitman_aw_9 = data[23]

    col_names = ['game_dates','game_infos', 'teams_hm','teams_aw','pitcher_hm',
            'pitcher_aw','hitman_hm_1','hitman_hm_2',
            'hitman_hm_3','hitman_hm_4','hitman_hm_5',
            'hitman_hm_6','hitman_hm_7','hitman_hm_8',
            'hitman_hm_9','hitman_aw_1','hitman_aw_2',
            'hitman_aw_3','hitman_aw_4','hitman_aw_5',
            'hitman_aw_6','hitman_aw_7','hitman_aw_8',
            'hitman_aw_9']

    df = pd.DataFrame(list(zip(game_dates,game_infos,teams_hm,teams_aw,pitcher_hm,pitcher_aw,
                                         hitman_hm_1,hitman_hm_2,hitman_hm_3,hitman_hm_4,
                                         hitman_hm_5,hitman_hm_6,hitman_hm_7,hitman_hm_8,
                                         hitman_hm_9,hitman_aw_1,hitman_aw_2,hitman_aw_3,
                                         hitman_aw_4,hitman_aw_5,hitman_aw_6,hitman_aw_7,
                                         hitman_aw_8,hitman_aw_9)),
                  columns = col_names)
    return df



### 타자 날짜별 정보 크롤링
def get_hits_info(urls_hit):
    global update_date
    global cols_hit

    try:
        code = urls_hit[0]
        name = urls_hit[1]
        year = urls_hit[2]
        url = urls_hit[3]

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        x = soup.find_all('div', class_ = 'box')[2].find_all('td')

        update_year = int(update_date[:4])
        update_month = int(update_date[4:6])
        update_day = int(update_date[6:])

        L = []
        for i in range(34):
            L.append([])

        for i in range(int(len(x)/31)):
            L[0].append(name)
            L[1].append(code)
            L[2].append(year)
            for j in range(0,31):
                L[j+3].append(x[i*31+j].get_text())

        dfL = pd.DataFrame(L).transpose()


    except:
        print(urls_hit)
        dfL = pd.DataFrame(columns=range(34))


    dfL.columns = cols_hit

    try:
        dfL['filter'] = pd.to_datetime((dfL['year']+ '-' + dfL['date']), format='%Y-%m-%d')
        dfL = dfL[dfL['filter'] >= datetime.strptime(update_date, '%Y%m%d')].drop('filter', axis=1)
    except:
        pass


    return dfL




### 투수 날짜별 정보 크롤링
def get_pits_info(urls_pit):
    global update_date
    global cols_pit

    try:
        code = urls_pit[0]
        name = urls_pit[1]
        year = urls_pit[2]
        url = urls_pit[3]

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        x = soup.find_all('div', class_ = 'box')[2].find_all('td')

        update_year = int(update_date[:4])
        update_month = int(update_date[4:6])
        update_day = int(update_date[6:])

        L = []
        for i in range(32):
            L.append([])

        for i in range(int(len(x)/29)):
            L[0].append(name)
            L[1].append(code)
            L[2].append(year)
            for j in range(0,29):
                L[j+3].append(x[i*29+j].get_text())

        dfL = pd.DataFrame(L).transpose()


    except:
        print(urls_pit)
        dfL = pd.DataFrame(columns=range(34))


    dfL.columns = cols_pit

    try:
        dfL['filter'] = pd.to_datetime((dfL['year']+ '-' + dfL['date']), format='%Y-%m-%d')
        dfL = dfL[dfL['filter'] >= datetime.strptime(update_date, '%Y%m%d')].drop('filter', axis=1)
    except:
        pass

    return dfL


### 개인별 url 가져오기
def get_personal_urls(df):
    global urls_pits
    global urls_hits
    global code_birth
    global code_name
    global invalid_urls
    global players_info_summary

    for i in range(len(df)):
        for j in range(1, 3):
            try:
                code = str(df.iloc[i][j])
                birth = players_info_summary[code][2]

                if code in code_birth.keys():
                    birth = code_birth[code]

                year = str(df.iloc[i][0])

                name = players_info_summary[code][1]
                if code in code_name.keys():
                    name = code_name[code]



                url = f'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name={name}&birth={birth[:4]}-{birth[4:6]}-{birth[6:8]}&re=1&se=&da=&year={year[:4]}&cv='
                if not (code,name,year[:4],url) in urls_pits:
                    urls_pits.append((code,name,year[:4],url))
            except:
                invalid_urls.append((code,name, birth, year[:4]))



        for j in range(3, 21):
            try:
                code = str(df.iloc[i][j])
                birth = players_info_summary[code][2]
                if code in code_birth.keys():
                    birth = code_birth[code]

                year = str(df.iloc[i][0])

                name = players_info_summary[code][1]
                if code in code_name.keys():
                    name = code_name[code]



                url = f'http://www.statiz.co.kr/player.php?opt=3&sopt=0&name={name}&birth={birth[:4]}-{birth[4:6]}-{birth[6:8]}&re=0&se=&da=&year={year[:4]}&cv='
                if not (code,name,year[:4],url) in urls_hits:
                    urls_hits.append((code,name,year[:4],url))

            except:
                invalid_urls.append((code,name, birth, year[:4]))






reset_crawl()

file_path = './update_date.txt'

with open(file_path, 'r') as file:
    line = file.readlines()

file.close()

update_date = line[0]

### 시작
lineup_df = make_df(start_crawl(get_update_lineup_urls(update_date)))


gameinfo = pd.DataFrame(lineup_df['game_infos'].tolist())
gameinfo_key_list = list(lineup_df['game_infos'][0].keys())
gameinfo = gameinfo[['winner', 'gameId', 'homeTeamCode', 'awayTeamCode', 'homeTeamRheb', 'awayTeamRheb']]
gameinfo_Rheb_hm = gameinfo['homeTeamRheb'].apply(pd.Series)
gameinfo_Rheb_hm.columns = ['hm_R', 'hm_h', 'hm_e', 'hm_b']
gameinfo_Rheb_aw = gameinfo['awayTeamRheb'].apply(pd.Series)
gameinfo_Rheb_aw.columns = ['aw_R', 'aw_h', 'aw_e', 'aw_b']
gameinfo = pd.concat([gameinfo.drop('homeTeamRheb', axis=1), gameinfo_Rheb_hm], axis=1)
gameinfo = pd.concat([gameinfo.drop('awayTeamRheb', axis=1), gameinfo_Rheb_aw], axis=1)
lineup_df = pd.concat([lineup_df.drop(['game_infos','teams_hm','teams_aw'], axis=1), gameinfo], axis=1)




for i in invalid_urls:
    print(f'https://m.sports.naver.com/game/{i}/record')
    print(i)




player_info_df = pd.DataFrame.from_dict(player_info, orient='index')
player_info_df.columns = ['backnum', 'playerName','playerCode', 'birth','info']
player_info_df = player_info_df.reset_index(drop=True)



players_info_summary = player_info_df.set_index('playerCode').T.to_dict('list')

df = lineup_df.loc[:, ['game_dates'] + list(lineup_df.loc[:, 'pitcher_hm':'hitman_aw_9'])]
get_personal_urls(df)



DF_PITS = pd.DataFrame(columns=range(32))
DF_PITS.columns = cols_pit

for i, url_pit in enumerate(urls_pits):
    pit_df = get_pits_info(url_pit)
    DF_PITS = pd.merge(DF_PITS, pit_df, how = 'outer')

    if i % 50 == 49:
        time.sleep(5)


DF_PITS = DF_PITS.drop(['name','vs'], axis=1)
DF_PITS['itv'] = DF_PITS['itv'].str.replace('일', '')




DF_HITS = pd.DataFrame(columns=range(34))
DF_HITS.columns = cols_hit

for i, url_hit in enumerate(urls_hits):
    hit_df = get_hits_info(url_hit)
    DF_HITS = pd.merge(DF_HITS, hit_df, how = 'outer')

    if i % 50 == 49:
        time.sleep(5)
        
DF_HITS = DF_HITS.drop(['name','vs'], axis=1)

lineup_df.to_csv('UPDATE_lineup.csv',index = False,encoding = 'utf-8')
player_info_df.to_csv('UPDATE_player.csv',index = False,encoding = 'utf-8')
DF_PITS.to_csv('UPDATE_pit.csv',index = False,encoding = 'utf-8')
DF_HITS.to_csv('UPDATE_hit.csv',index = False,encoding = 'utf-8')



print('게임갯수 : ', len(lineup_df))
print('타자갯수 : ', len(DF_HITS))
print('투수갯수 : ', len(DF_PITS))
print('인포갯수 : ', len(player_info_df))

print('UPDATE_.CSV 저장완료')





file_path = './update_date.txt'

with open(file_path, 'r') as file:
    line = file.readlines()

file.close()

update_date = line[0]

Basedf_lineup = pd.read_csv('BASE_lineup.csv',encoding='utf-8')
len_Basedf_lineup = len(Basedf_lineup)

lineup_df = pd.read_csv('UPDATE_lineup.csv',encoding='utf-8')
Basedf_lineup = pd.concat([Basedf_lineup, lineup_df], axis=0)
Basedf_lineup = Basedf_lineup.drop_duplicates()
Basedf_lineup = Basedf_lineup.reset_index(drop=True)
len_Basedf_lineup2 = len(Basedf_lineup)

Basedf_hit = pd.read_csv('BASE_hit.csv',encoding='utf-8')
len_Basedf_hit = len(Basedf_hit)
DF_HITS = pd.read_csv('UPDATE_hit.csv',encoding='utf-8')
Basedf_hit = pd.concat([Basedf_hit, DF_HITS], axis=0).drop_duplicates()
Basedf_hit = Basedf_hit.reset_index(drop=True)
len_Basedf_hit2 = len(Basedf_hit)

Basedf_pit = pd.read_csv('BASE_pit.csv', encoding='utf-8')
len_Basedf_pit = len(Basedf_pit)
DF_PITS = pd.read_csv('UPDATE_pit.csv',encoding='utf-8')
Basedf_pit = pd.concat([Basedf_pit, DF_PITS], axis=0).drop_duplicates()
Basedf_pit = Basedf_pit.reset_index(drop=True)
len_Basedf_pit2 = len(Basedf_pit)




Basedf_player = pd.read_csv('BASE_player.csv',encoding='utf-8')
len_Basedf_player = len(Basedf_player)
player_info_df = pd.read_csv('UPDATE_player.csv',encoding='utf-8')
Basedf_player = pd.concat([Basedf_player, player_info_df], axis=0).drop_duplicates('playerCode', keep='last')
Basedf_player = Basedf_player.reset_index(drop=True)
len_Basedf_player2 = len(Basedf_player)





print(f'{len_Basedf_lineup2 - len_Basedf_lineup} 개의 경기 데이터 업데이트 완료!')
print(f'{len_Basedf_hit2 - len_Basedf_hit} 개의 타자 데이터 업데이트 완료!')
print(f'{len_Basedf_pit2 - len_Basedf_pit } 개의 투수 데이터 업데이트 완료!')
print(f'{len_Basedf_player2 - len_Basedf_player } 개의 선수 정보 업데이트 완료!')

Basedf_lineup.to_csv('BASE_lineup.csv', index = False, encoding='utf-8')
Basedf_hit.to_csv('BASE_hit.csv', index = False, encoding='utf-8')
Basedf_pit.to_csv('BASE_pit.csv', index = False, encoding='utf-8')
Basedf_player.to_csv('BASE_player.csv', index = False, encoding='utf-8')


# 현재 날짜 계산
today = datetime.today()

# 1년 전의 날짜 계산
one_year_ago = today - timedelta(days=365)

# 조건을 만족하는 행 제거
lineupdf = pd.read_csv('BASE_lineup.csv')
lineupdf['game_dates'] = pd.to_datetime(lineupdf['game_dates'], format='%Y%m%d')
lineupdf = lineupdf[lineupdf['game_dates'] >= one_year_ago.strftime('%Y%m%d')]


playerdf = pd.read_csv('BASE_player.csv')
playerdf['info'] = '-'

pits_dict = {}
hits_dict = {}


for i in range(len(lineupdf)):
    code = lineupdf['pitcher_hm'].iloc[i]
    pits_dict[code] = lineupdf['homeTeamCode'].iloc[i]
    code = lineupdf['pitcher_aw'].iloc[i]
    pits_dict[code] = lineupdf['awayTeamCode'].iloc[i]

    for j in ['hm', 'aw']:
        for k in range(1,10):
            code = lineupdf[f'hitman_{j}_{k}'].iloc[i]

            if j == 'hm':
                hits_dict[code] = lineupdf['homeTeamCode'].iloc[i]
            else:
                hits_dict[code] = lineupdf['awayTeamCode'].iloc[i]

for i in range(len(playerdf)):
    code = playerdf['playerCode'][i]
    if code in pits_dict.keys():
        playerdf['info'][i] = 'P_' + pits_dict[code]
    elif code in hits_dict.keys():
        playerdf['info'][i] = 'H_' + hits_dict[code]


playerdf.to_csv('BASE_player.csv',index = False)






file_paths = ['UPDATE_hit.csv', 'UPDATE_lineup.csv', 'UPDATE_pit.csv', 'UPDATE_player.csv']

for file_path in file_paths:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} 파일이 성공적으로 삭제되었습니다.")
    else:
        print(f"{file_path} 파일이 존재하지 않습니다.")






# 텍스트 파일 쓰기 (덮어쓰기)

file_path = './update_date.txt'

with open(file_path, 'w') as file:
    file.writelines(datetime.now().strftime("%Y%m%d"))
file.close()

print(f'{line[0]} 부터 {datetime.now().strftime("%Y%m%d")} 까지 업데이트 완료!')
print(f'update_date.txt = \'{datetime.now().strftime("%Y%m%d")}\'')

