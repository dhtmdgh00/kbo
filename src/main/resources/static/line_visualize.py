import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import math
import scipy.stats as stats
from math import pi
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import sys
import warnings
from plotly.subplots import make_subplots

warnings.filterwarnings('ignore')

def convert_to_float(lst):
    return [float(x) for x in lst]

def move_item(lst):
    item = lst.pop(5)  # 5번째 항목 추출
    lst.insert(3, item)  # 4번째 자리에 삽입
    
    rest = lst[5:]  # 5번째 항목 이후의 항목 추출
    del lst[5:]  # 추출한 항목들 삭제
    lst.extend(rest)  # 추출한 항목들을 뒤로 이동
    
    return lst

def move_item2(lst):
    item = lst.pop(2)  # 5번째 항목 추출
    lst.insert(1, item)  # 4번째 자리에 삽입

    return lst

def sort_lists(list1, list2):
    sorted_indices = sorted(range(len(list1)), key=lambda x: list1[x])
    sorted_list1 = [list1[i] for i in sorted_indices]
    sorted_list2 = [list2[i] for i in sorted_indices]
    
    return sorted_list1, sorted_list2

def splitargv(L1):
    L2 = []
    for season in L1[2].split('), '):
        line = remove_parentheses_and_brackets(season.split(', '))
        for x in line:
            L2.append(x)
    L3 = []
    seasons = []
    result = L1[:2]
    for i, num  in enumerate(L2):
        if i % 9 in [3,4,5,6,7,8]:
            L3.append(num.split('=')[1])
        if i % 9 in [2]:
            seasons.append(num.split('=')[1])
            
    for i in range(int(len(L3)/6)):
        result.append(L3[i*6 +0 ])
        result.append(L3[i*6 +1 ])
        result.append(L3[i*6 +2 ])
        result.append(L3[i*6 +3 ])
        result.append(L3[i*6 +4 ])
        result.append(L3[i*6 +5 ])
        result.append(seasons[i])

    return result

def remove_parentheses_and_brackets(lst):
    result = []
    for item in lst:
        item_without_parentheses = item.replace(")", "").replace("]", "")
        result.append(item_without_parentheses)
    return result

def visualize(L):
    colors = ['magenta', 'orange', 'skyblue']
    pithit = L[1]
    lenL = int((len(L)-2) / 7)
    inputs = []
    for split in range(lenL):
        smallL = L[2+(split*7):9+(split*7)]
        inputs.append(smallL)

    seasons = []
    sc = []


    for input in inputs:
        sc.append(move_item(convert_to_float(input[:6])))
        seasons.append(input[-1])

    seasons = convert_to_float(seasons)
    
    seasons, sc = sort_lists(seasons, sc)

    

    if not pithit == 'hit': 
        colnames = ['평균자책점', '출루허용률', '삼진/투구수']
        for i, s in enumerate(sc):
            del s[2]
            del s[3]
            del s[3]
            for s in sc:
                s = move_item2(s)

    else:
        colnames = ['타율', '장타율', '출루율' ]
        for i, s in enumerate(sc):
            del s[2]
            del s[3]
            del s[3]
            
            
    fig = go.Figure()

    colnames = [f"<b>{title}</b>" for title in colnames]

    big = 0
    for i in sc:
        for j in i:
            if j > big:
                big = j

    for i in range(len(colnames)):
        col = colnames[i]
        indicator_values = [s[i] for s in sc]
        fig.add_trace(go.Scatter(x=seasons, y=indicator_values, line_color = colors[i], line_width=3.0,
                             mode='lines+markers', name=col, opacity=1))
        
    fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='grey')
    fig.update_yaxes(showgrid=True, gridwidth=1.3, gridcolor='grey', griddash='dot',zeroline = True)

    fig.update_layout(xaxis=dict(
                                range=[min(seasons)-0.5, max(seasons)+0.5],
                                    tickmode='linear',
                                    dtick=1,
                                    color='black',
                                tickfont=dict(
                                    family="bold"  # 볼드 처리
                                )
                                ),
                      
                    barmode='group',
           
                        yaxis=dict(
                            range=[-0.1, big+0.1],
                            color='black'
                        ),
                      
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                      
                    height=100 * len(colnames),
                    showlegend=True,
                      
                     legend=dict(
                    x=1,  # Adjust the x position of the custom legend
                    y=1,  # Adjust the y position of the custom legend
                    font=dict(size=12),  # Adjust the font size of the custom legend
                    xanchor='left',
                    yanchor='top',
                    )
                     )
    fig.add_shape(
                type="line",
                x0=min(seasons)-0.5,
                y0=0,
                x1=max(seasons)+0.5,
                y1=0,
                line=dict(color="grey", width=1.3, dash='dot')
                )
  
    
    return pio.to_json(fig)
    #fig.show()


    
#sys.argv = ['./src/main/resources/static/test.py', 'pit', '[Pit_seasonDTO(idx=445, code=77637, year=2018, era=4.05, kpit=0.052, kbb=3.444, wpa=-0.034, re24=0.74, whip=1.325), Pit_seasonDTO(idx=446, code=77637, year=2019, era=2.29, kpit=0.06, kbb=4.939, wpa=0.181, re24=2.33, whip=1.083), Pit_seasonDTO(idx=447, code=77637, year=2020, era=4.7, kpit=0.051, kbb=2.328, wpa=-0.021, re24=0.89, whip=1.445), Pit_seasonDTO(idx=448, code=77637, year=2022, era=3.85, kpit=0.049, kbb=2.82, wpa=0.063, re24=0.55, whip=1.278), Pit_seasonDTO(idx=449, code=77637, year=2023, era=3.86, kpit=0.053, kbb=3.083, wpa=0.041, re24=0.78, whip=1.515)]']

#visualize(splitargv(sys.argv))
print(visualize(splitargv(sys.argv)))