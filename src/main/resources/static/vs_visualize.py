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
import plotly.subplots as sp

def convert_to_float(lst):
    return [float(x) for x in lst]

def format_values(value):
    if value[0] == '0':
        # 소수점 3자리까지 보이도록 변환
        return f'{float(value):.3f}'
    else:
        # 소수점 2자리까지 보이도록 변환
        return f'{float(value):.2f}'

# 변환된 값을 저장할 새로운 리스트 생성


def visualize(L):
    L = L[1:]


    sc = L
    away_values = sc[:3]
    home_values = sc[3:6]

    home_values = [format_values(value) for value in home_values]
    away_values = [format_values(value) for value in away_values]
    
    
    data_labels = [f'{home_values[0]}     승 률      {away_values[0]} ',
                   f'{home_values[1]}     평균 득점     {away_values[1]} ',
                   f'{home_values[2]}     평균 실점     {away_values[2]} ']
    
    data_labels = [f"<b>{title}</b>" for title in data_labels]
    
    
    away_values = convert_to_float(away_values)
    home_values = convert_to_float(home_values)    

    
    bar_width = 0.25
    
    num_metrics = len(data_labels)
    num_cols = 2

    # Create subplots with the desired number of rows and columns
    fig = sp.make_subplots(rows=num_metrics, cols=num_cols, horizontal_spacing=0.29)

    # Define the bar width
    bar_width = 0.22

    # Loop through the metrics and create the bar graphs
    for i, label in enumerate(data_labels):
        
        # 홈 팀 subplot
        fig.add_trace(
            go.Bar(
                x=[-home_values[i]],
                y=None,
                name='Away Team',
                orientation='h',
                marker=dict(color='skyblue'),
                width=bar_width,
                showlegend=False
            ),
            row=i+1,
            col=1
        )

        # 어웨이 팀 subplot
        fig.add_trace(
            go.Bar(
                x=[away_values[i]],
                y=[label],
                name='Home Team',
                orientation='h',
                marker=dict(color='deeppink'),
                width=bar_width,
                showlegend=False
            ),
            row=i+1,
            col=2
        )
                 
        # 축 조정
        if label == data_labels[0]:  # Check if it's the 5th or 6th column
            fig.update_xaxes(showgrid = False, range=[-1, 0], row=1, col=1, showticklabels=False)  
            fig.update_xaxes(showgrid = False, range=[0, 1], row=1, col=2, showticklabels=False)
            fig.update_yaxes(visible=False, row=i + 1, col=1)  
            fig.update_yaxes(visible=True, row=i + 1, col=2)
        else:
            fig.update_xaxes(showgrid = False, range=[-8, 0], row=2, col=1, showticklabels=False)
            fig.update_xaxes(showgrid = False, range=[0, 8], row=2, col=2, showticklabels=False)
            fig.update_xaxes(showgrid = False, range=[-8, 0], row=3, col=1, showticklabels=False)
            fig.update_xaxes(showgrid = False, range=[0, 8], row=3, col=2, showticklabels=False) 
            fig.update_yaxes(visible=False, row=i + 1, col=1)  
            fig.update_yaxes(visible=True, row=i + 1, col=2)
    

    # Update the layout
    fig.update_layout(
        height=250,
        barmode='group',
        bargap=0.05,
        yaxis=dict(title=''),
        xaxis=dict(),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )
    
    fig.update_traces(hovertemplate=' ')

    return pio.to_json(fig)
    #fig.show()


#sys.argv = ['line_visualize.py', '0.62', '5.40', '4.3', '0.450', '4.19', '4.32']
#visualize(sys.argv)
#print(sys.argv)
print(visualize(sys.argv))