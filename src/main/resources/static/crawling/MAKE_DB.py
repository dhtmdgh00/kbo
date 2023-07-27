import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import warnings
import numpy as np
warnings.filterwarnings('ignore')

import mysql.connector

Basedf_pit = pd.read_csv('BASE_pit.csv')
Basedf_hit = pd.read_csv('BASE_hit.csv')

Basedf_pit = Basedf_pit.drop(['filter'], axis = 1)
Basedf_hit = Basedf_hit.drop(['filter'], axis = 1)

Basedf_pit['whip'] = round(Basedf_pit['whip'], 3)
Basedf_pit['avg'] = round(Basedf_pit['avg'], 3) 
Basedf_pit['obp'] = round(Basedf_pit['obp'], 2)
Basedf_pit['ops'] = round(Basedf_pit['ops'], 2)
Basedf_pit['era'] = round(Basedf_pit['era'],2)
Basedf_pit['avli'] = round(Basedf_pit['avli'], 3) 
Basedf_pit['re24'] = round(Basedf_pit['re24'], 3) 
Basedf_pit['wpa'] = round(Basedf_pit['wpa'], 3)

Basedf_hit['wpa'] = round(Basedf_hit['wpa'], 3)
Basedf_hit['avg'] = round(Basedf_hit['avg'], 3)
Basedf_hit['obp'] = round(Basedf_hit['obp'], 3)
Basedf_hit['ops'] = round(Basedf_hit['ops'], 3)
Basedf_hit['avli'] = round(Basedf_hit['avli'], 3)
Basedf_hit['re24'] = round(Basedf_hit['re24'], 3)
Basedf_hit['slg'] = round(Basedf_hit['slg'], 3)

Basedf_pit['gsc'] = Basedf_pit['gsc'].fillna('-')
Basedf_pit['decision'] = Basedf_pit['decision'].fillna('-')


Basedf_hit.astype(str).applymap(lambda x: f"{x}").to_csv('DB_hit.csv',index = True)
Basedf_pit.astype(str).applymap(lambda x: f"{x}").to_csv('DB_pit.csv',index = True)
Basedf_pit = pd.read_csv('DB_pit.csv').drop_duplicates()
Basedf_hit = pd.read_csv('DB_hit.csv').drop_duplicates()


Basedf_pit = Basedf_pit.replace(np.inf, 99.99)
Basedf_hit = Basedf_hit.replace(np.inf, 99.99)

Basedf_pit.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
Basedf_pit['idx'] = Basedf_pit['idx']+1
Basedf_pit['idx'] = Basedf_pit['idx'].apply(lambda x: str(x).zfill(6))
Basedf_pit = Basedf_pit.astype(str)
Basedf_pit.to_csv('DB_pit.csv',index = False)

Basedf_hit.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
Basedf_hit['idx'] = Basedf_hit['idx']+1
Basedf_hit['idx'] = Basedf_hit['idx'].apply(lambda x: str(x).zfill(6))
Basedf_hit = Basedf_hit.astype(str)
Basedf_hit.to_csv('DB_hit.csv',index = False)




Basedf_pit = pd.read_csv('DB_pit.csv')
Basedf_hit = pd.read_csv('DB_hit.csv')

Basedf_pit = Basedf_pit.drop(['idx'], axis = 1)
Basedf_hit = Basedf_hit.drop(['idx'], axis = 1)

Basedf_pit['out'] = Basedf_pit['ip'].apply(int) *3 + (Basedf_pit['ip'] - Basedf_pit['ip'].apply(int))*10

season = Basedf_pit.groupby(['code','year']).sum()
season['count'] = list(Basedf_pit.groupby(['code','year']).size().reset_index()[0])
season = season[season['out'] >= 90][['count','er','out','pit','k','bb','re24','wpa','hit','ibb','hbp','whip']]
total = season[season['out'] >= 90][['count','er','out','pit','k','bb','re24','wpa','hit','ibb','hbp','whip']].reset_index().groupby(['code']).sum()[['count','er','out','pit','k','bb','re24','wpa','hit','ibb','hbp','whip']]

season['era'] = round(season['er'] * 9 / (season['out'] / 3), 2)
season['kpit'] = round(season['k'] / season['pit'], 3)
season['kbb'] = round(season['k'] / season['bb'], 3)
season['whip'] = round( (season['hit'] + season['ibb']+ season['hbp']+ season['bb']) / (season['out'] / 3),3)
season['wpa'] = round(Basedf_pit.groupby(['code','year'])['wpa'].median(), 3)
season['re24'] = round(Basedf_pit.groupby(['code','year'])['re24'].median(), 3)

season = season.drop(['count', 'er', 'out', 'pit', 'k', 'bb', 'hit', 'ibb', 'hbp'], axis = 1)
season = season.reset_index()
season = season.astype(str)
season = season.reindex(columns=['code','year', 'era', 'kpit', 'kbb', 'wpa', 're24', 'whip'])
season.to_csv('pit_season.csv')
season = pd.read_csv('pit_season.csv')
season.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
season['idx'] = season['idx']+1
season['idx'] = season['idx'].apply(lambda x: str(x).zfill(6))
season = season.astype(str)
season.to_csv('pit_season.csv',index = False)


total['era'] = round(total['er'] * 9 / (total['out'] / 3), 2)
total['kpit'] = round(total['k'] / total['pit'], 3)
total['kbb'] = round(total['k'] / total['bb'], 3)
total['whip'] = round( (total['hit'] + total['ibb']+ total['hbp']+ total['bb']) /  (total['out'] / 3),3)
total['wpa'] = round(Basedf_pit.groupby(['code'])['wpa'].median(), 3)
total['re24'] = round(Basedf_pit.groupby(['code'])['re24'].median(), 3)


total = total.drop(['count', 'er', 'out', 'pit', 'k', 'bb', 'hit', 'ibb', 'hbp'], axis = 1)
total = total.reset_index()
total = total.astype(str)
total = total.reindex(columns=['code','era', 'kpit', 'kbb', 'wpa', 're24', 'whip'])
total.to_csv('pit_total.csv')
total = pd.read_csv('pit_total.csv')
total.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
total['idx'] = total['idx']+1
total['idx'] = total['idx'].apply(lambda x: str(x).zfill(6))
total = total.astype(str)
total.to_csv('pit_total.csv',index = False)

season = Basedf_hit.groupby(['code','year']).sum()
season['count'] = list(Basedf_hit.groupby(['code','year']).size().reset_index()[0])

season['ab'] = season['pa']
season['pa'] = season['ab'] + season['bb'] + season['hbp'] + season['ibb'] + season['sh'] + season['sf']


season = season[season['ab']  >= 90][['ab','pa','hit','second', 'third', 'homerun', 'bb', 'hbp', 'ibb', 'k', 'sh', 'sf', 're24', 'wpa', 'count']]
total = season[season['ab'] >= 90][['ab','pa','hit','second', 'third', 'homerun', 'bb', 'hbp', 'ibb', 'k', 'sh', 'sf', 're24', 'wpa', 'count']].reset_index().groupby(['code']).sum()[['ab','pa','hit','second', 'third', 'homerun', 'bb', 'hbp', 'ibb', 'k', 'sh', 'sf', 're24', 'wpa', 'count']]

season['avg'] = round(season['hit'] / season['ab'], 3)
season['slg'] = round( (season['hit'] + season['second'] + season['third']*2 +season['homerun']*3) / season['ab'], 3)
season['obp'] = round( ( (season['hit'] + season['bb'] + season['ibb'] + season['hbp']) / season['pa'] ), 3)
season['bbk'] = round( season['bb'] / season['k'] , 3)
season['wpa'] = round(Basedf_hit.groupby(['code','year'])['wpa'].median(),3)
season['re24'] = round(Basedf_hit.groupby(['code','year'])['re24'].median(),3)

season = season.drop(['ab', 'pa', 'hit','second', 'third', 'homerun', 'bb', 'hbp', 'ibb', 'k', 'sh', 'sf', 'count'], axis = 1)
season = season.reset_index()
season = season.astype(str)
season = season.reindex(columns=['code','year','avg', 'slg', 'bbk', 'wpa', 're24', 'obp'])
season.to_csv('hit_season.csv')
season = pd.read_csv('hit_season.csv')
season.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
season['idx'] = season['idx']+1
season['idx'] = season['idx'].apply(lambda x: str(x).zfill(6))
season = season.astype(str)
season.to_csv('hit_season.csv',index = False)


total['avg'] = round(total['hit'] / total['ab'], 3)
total['slg'] = round( (total['hit'] + total['second'] + total['third']*2 +total['homerun']*3) / total['ab'], 3)
total['obp'] = round( ( (total['hit'] + total['bb'] + total['ibb'] + total['hbp']) / total['pa'] ), 3)
total['bbk'] = round( total['bb'] / total['k'] , 3)
total['wpa'] = round(Basedf_hit.groupby(['code'])['wpa'].median(),3)
total['re24'] = round(Basedf_hit.groupby(['code'])['re24'].median(),3)

total = total.drop(['ab', 'pa', 'hit','second', 'third', 'homerun', 'bb', 'hbp', 'ibb', 'k', 'sh', 'sf', 'count'], axis = 1)
total = total.reset_index()
total = total.astype(str)
total = total.reindex(columns=['code','avg', 'slg', 'bbk', 'wpa', 're24', 'obp'])
total.to_csv('hit_total.csv')
total = pd.read_csv('hit_total.csv')
total.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
total['idx'] = total['idx']+1
total['idx'] = total['idx'].apply(lambda x: str(x).zfill(6))
total = total.astype(str)
total.to_csv('hit_total.csv',index = False)


playerdf = pd.read_csv('BASE_player.csv')
playerdf = playerdf[['playerName','playerCode']]
playerdf.rename(columns={'playerName': 'name'}, inplace=True)
playerdf.rename(columns={'playerCode': 'code'}, inplace=True)
playerdf = playerdf[['code','name']]

position = []
codelist = list(playerdf['code'])
for code in codelist: 
    pit_TF = Basedf_pit[Basedf_pit['code'] == code]
    hit_TF = Basedf_hit[Basedf_hit['code'] == code]
    if len(pit_TF) > len(hit_TF):
        position.append('pit')
    else:
        position.append('hit')
playerdf['position'] = position     


playerdf.to_csv('DB_player.csv')
playerdf = pd.read_csv('DB_player.csv')
playerdf.rename(columns={'Unnamed: 0': 'idx'}, inplace=True)
playerdf['idx'] = playerdf['idx']+1
playerdf['idx'] = playerdf['idx'].apply(lambda x: str(x).zfill(6))
playerdf = playerdf.astype(str)
playerdf.to_csv('DB_player.csv',index = False)