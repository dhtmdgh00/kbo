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

def visualize(L):
    global indices
    colors = ['Green', 'Red', 'blue']
    pithit = L[1]
    lenL = int((len(L)-2) / 7)
    inputs = []
    for split in range(lenL):
        smallL = L[2+(split*7):9+(split*7)]
        inputs.append(smallL)
    
    names = []
    sc = []
    for input in inputs:
        sc.append(move_item(convert_to_float(input[:6])))
        names.append(input[-1])
    
    if not pithit == 'hit': 
        colnames = ['평균자책점', '구위력', '제구력', '출루허용률', '게임기여도', '득점기대' ]

    else:
        colnames = ['타율', '장타율', '선구안', '출루율', '게임기여도', '득점기대' ]
    
    subplot_titles = [f"<b>{title}</b>" for title in colnames]
    names = [f"<b>{title}</b>" for title in names]
    fig = make_subplots(rows=len(colnames), cols=1, subplot_titles=subplot_titles, vertical_spacing = 0.13)
    

    bar_width = 0.22
   
    for i, col in enumerate(colnames):
        col = colnames[i]
        for j in range(len(sc)-1, -1, -1):
            player = sc[j]
            if i == 4 or i == 5:  # Check if it's the 5th or 6th column
                fig.add_trace(go.Bar(
                    x=[sc[j][i]],
                    y=[-1],  # Set the y-value to -1 to position the bar above the other bars
                    name=names[j],
                    orientation='h',
                    width=bar_width,
                    showlegend=False,
                    opacity=1 / (len(sc)),
                    marker=dict(color=colors[j], line=dict(color='gray', width=bar_width))
                ), row=i + 1, col=1)
            else:
                fig.add_trace(go.Bar(
                    x=[sc[j][i]],
                    name=names[j],
                    orientation='h',
                    width=bar_width,
                    showlegend=False,
                    opacity=1 / (len(sc)),
                    marker=dict(color=colors[j], line=dict(color='gray', width=bar_width))
                ), row=i + 1, col=1)
    
            fig.update_yaxes(visible=False, row=i + 1, col=1)
    
            if i == 4 or i == 5:  # Check if it's the 5th or 6th column
                sc_values = [item[i] for item in sc]  # Extract the values from the specific column
                max_value = max(abs(value) for value in sc_values)  # Find the maximum absolute value
                fig.update_xaxes(showgrid = False, range=[-max_value, max_value], row=i + 1, col=1)  # Set x-axis range to -max to max
            else:
                fig.update_xaxes(showgrid = False, visible=True, row=i + 1, col=1)  # Keep the default x-axis range

    if pithit == 'hit':
        fig.update_layout(
            barmode='group',
            xaxis=dict(
                tickmode='linear',
                dtick=0.05
                #color='grey'
            ),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            height=100 * len(colnames),
            showlegend=False
        )
    else:
        fig.update_layout(
            barmode='group',
            xaxis=dict(
                tickmode='linear'
                #dtick=0.05
                #color='grey'
            ),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            height=100 * len(colnames),
            showlegend=False
        )
    
    fig.update_traces(hovertemplate='%{x:.3f}')
    
      # Create custom legend
    legend_labels = names
    legend_colors = colors[:len(names)]
    custom_legend = [go.Scatter(
            x=[None], y=[None],  # Use dummy values
            mode='markers',
            marker=dict(
            color=color,
            opacity=1/(len(sc)),
            size=10,
            line=dict(color='gray', width=1)
        ),
        name=label
    ) for color, label in zip(legend_colors, legend_labels)]

    fig.add_traces(custom_legend)

    fig.update_layout(
        showlegend=True,  # Show the custom legend
        legend=dict(
            x=1,  # Adjust the x position of the custom legend
            y=1,  # Adjust the y position of the custom legend
            font=dict(size=12),  # Adjust the font size of the custom legend
            xanchor='left',
            yanchor='auto',
        )
    )


    
    
    #fig.show()
    return pio.to_json(fig)


# python3 hex_visualize.py hit 0.290 0.450 0.680 0 -0.001 0.374 A 0.320 0.550 0.380 -0.02 +0.004 0.194 B 0.310 0.310 0.340 0 +0.001 0.764 C
#visualize(sys.argv)
#print(sys.argv)
sys.argv = [item for item in sys.argv if item != '']
print(visualize(sys.argv))

