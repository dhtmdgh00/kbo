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
warnings.filterwarnings('ignore')

def convert_to_float(lst):
    return [float(x) for x in lst]

def visualize(L):
    pithit = L[1]
    lenL = int((len(L)-2) / 7)
    inputs = []
    for split in range(lenL):
        smallL = L[2+(split*7):9+(split*7)]
        inputs.append(smallL)
    
    names = []
    
    if pithit == 'hit':
        max = [ 0.300, 0.478, 0.780, 0, 0, 0.376]
        min = [ 0.214, 0.288, 0.242, -0.013, -0.245, 0.272]
        
        sc = []
        
        for playerinput in inputs:
            playerlist = convert_to_float(playerinput[:6])
            name = playerinput[6]
            for i, n in enumerate(playerlist):
                if n < min[i]:
                    n = min[i]
                elif n > max[i]:
                    n = max[i]
                
                x = round((n- min[i]) * (8 / (max[i] - min[i])) + 1, 2)
                sc.append(x)
            names.append(name)
    #######################################
    else:
        
        max = [ 6.409 , 0.056, 3.434, 0.0743, 1.33, 1.8138]
        min = [ 3.156, 0.032, 1.12, -0.0839, -0.495, 1.2461]
        
        sc = []
        
        for playerinput in inputs:
            playerlist = convert_to_float(playerinput[:6])
            name = playerinput[6]
            for i, n in enumerate(playerlist):
                if n < min[i]:
                    n = min[i]
                elif n > max[i]:
                    n = max[i]
                
                x = round((n- min[i]) * (8 / (max[i] - min[i])) + 1, 2)
                sc.append(x)
            names.append(name)
    #######################################
    
    numsc = int(len(sc) / 6)
    if pithit == 'pit':    
        for num in range(numsc):
            sc[num*6]  =  10 - sc[num*6]
            sc[5+num*6]  =  10 - sc[5+num*6]
    
    #######################################
    
    if not pithit == 'hit': 
        colnames = ['평균자책점', '구위력', '제구력', '게임기여', '득점기대', '출루허용률']
        #['era', 'kpit', 'kbb', 'wpa', 're24', 'whip']
    else:
        colnames = ['타율', '장타율', '선구안', '게임기여', '득점기대', '출루율']
        #['avg', 'slg', 'bbk', 'wpa', 're24', 'obp']

    colnames = [f"<b>{title}</b>" for title in colnames]
    names = [f"<b>{title}</b>" for title in names]
   
    
    fig = px.line_polar(r = sc[:6], 
                       theta = colnames,
                        
                       template = 'presentation', # presentation, gridon
                       color_discrete_sequence=['Green'],
                      range_r = [0, 10],
                       line_close = True,     
                    )
    
    fig.update_traces(fill='toself',
                      opacity=1/(numsc),
                     visible=True,
                      name=names[0],showlegend=True

                     )
    
    
    colors = ['Red','blue']

    if numsc > 1:
        for i in range(1, numsc):
            fig2 = px.line_polar(r = sc[i*6:(i+1)*6], 
                           theta = colnames,
                          
                           template = 'presentation', 
                           color_discrete_sequence=[colors[i-1]], #Plasma_r,
                           range_r = [0, 10],
                           line_close = True,
                                )
            
            fig2.update_traces(fill='toself',opacity=1/(numsc),name=names[i],showlegend=True)
            
            fig.add_traces(fig2.data)
    
    fig.update_layout(
        polar=dict(
        radialaxis_showticklabels=False,
        radialaxis=dict(visible = True, showticklabels = False)
        #radialaxis_visible=False,  # 반지름 축 보이기 
        #angularaxis=dict(visible=False)  # 각도 축 숨기기
        ),
        showlegend=True,  # 범례 숨기기
        legend=dict(x=0.8, y=0.7, font=dict(size=13, color='black')),

        paper_bgcolor='rgba(0, 0, 0, 0)',  # 종이 배경 색상 설정 (투명)
        width=600,
        height=300
        )

    fig.update_layout(
        showlegend=True,  # Show the custom legend
        legend=dict(
            x=1,  # Adjust the x position of the custom legend
            y=1,  # Adjust the y position of the custom legend
            font=dict(size=12),  # Adjust the font size of the custom legend
            xanchor='left',
            yanchor='top',
        )
    )


    
    return pio.to_json(fig)
    #fig.show()




sys.argv = [item for item in sys.argv if item != '']

#visualize(sys.argv)
#print(sys.argv)
print(visualize(sys.argv))