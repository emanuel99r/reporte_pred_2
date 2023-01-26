from dash import Dash, html, dcc, ctx, callback
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import json
import math
import numpy as np
#import matplotlib.pyplot as plt
import time

dash.register_page(__name__, title="Carta Amperimétrica")


Carta = html.Div([
        
        html.Div([
            
            html.Div("Carta Amperimétrica", id="Titulo"),
            html.Div(id="FechaCarta", style={"margin-left":"5px"})
            
                  ], className="CartaTitle"),
        
        html.Div([
            
        html.Div(dcc.RangeSlider(0,1,id="slider", step=None, vertical=True), style={"width":"100px"}),
        html.Div(dcc.Graph(id="GraficoCarta2"), style={"margin-bottom":"15px"})
            
        ], className="CartaHijo")
        

    ], className="CartaPadre")

Cuerpo=html.Div([
    
    Carta
    
])

layout = html.Div([html.Div([Cuerpo], className="ReportMain", id="Report")])

@callback(

    Output('slider', 'value'),

    Input('Titulo', 'children')
    
)
def sliderIni(input):
    
    Data=pd.read_csv("./DataGuardian.csv")
    data=pd.DataFrame()

    data['time']=Data['time']
    data['time']=pd.to_datetime(data['time'], utc=True)
    data=data.set_index(data['time'])
    
    dias=pd.DataFrame()
    diaL=[]

    for d in data['time']:
        diaL.append(d.day) 
    
    dias["Dia"]=diaL
    dias=dias.drop_duplicates(subset=['Dia'])
    d=list(dias["Dia"])
    value=[d[1],d[3]]
    
    return value

@callback(
    
    Output('GraficoCarta2', 'figure'),
    Output('slider', 'marks'),
    Output('slider', 'min'),
    Output('slider', 'max'),
    Output('FechaCarta', 'children'),
    #Output('slider', 'value'),
    
    
    Input('slider', 'value'),
    Input('Titulo', 'children')
    
)
def carta(slider, input):
    
    Data=pd.read_csv("./DataGuardian.csv")
    data=pd.DataFrame()
    
    AMP_MOTOR = (Data["AMPAPQM3_amp"]+Data["AMPBPQM3_amp"]+Data["AMPCPQM3_amp"])/3
    data['time']=Data['time']
    data['AMP_MOTOR']=AMP_MOTOR 
    
    data['time']=pd.to_datetime(data['time'], utc=True)
    data=data.set_index(data['time'])
    
    dias=pd.DataFrame()
    diaL=[]
    fechaL=[]

    for d in data['time']:
        diaL.append(d.day) 
        
        if d.month==1:
            mes="Jan"
        elif d.month==2:
                mes="Feb"
        elif d.month==3:
                mes="Mar"
        elif d.month==4:
                mes="Apr"
        elif d.month==5:
                mes="May"
        elif d.month==6:
                mes="Jun"
        elif d.month==7:
                mes="Jul"
        elif d.month==8:
                mes="Aug"
        elif d.month==9:
                mes="Sep"
        elif d.month==10:
                mes="Oct"
        elif d.month==11:
                mes="Nov"
        elif d.month==12:
                mes="Dec"
                
        fechaL.append(f"{d.day} {mes} {d.year}")
    
    dias["Dia"]=diaL
    dias["Fecha"]=fechaL

    dias=dias.drop_duplicates(subset=['Dia'])
    fecha=list(dias["Fecha"])
    marks={}

    for f,d in enumerate(dias["Dia"]):
        marks[d]=fecha[f]
    
    v=list(marks.keys())
    Min=v[0]
    Max=v[-1]
    
    d=list(marks.values())

    #if slider==None:
    #    data=data.loc[d[0]:d[0]]
    #else:
    
    #data=data.loc[marks[slider]:marks[slider]]
    
    data=data.loc[marks[slider[0]]:marks[slider[1]]]
    
    data['time']=data['time']  
    data['time']=data['time'].dt.strftime('%d %h %Y,%H:%M:%S')
    delta=(2 * np.pi)/len(data)
    rads = np.arange(0, (2 * np.pi), delta)
    rads=pd.DataFrame(rads,columns=['rads'])
    data=data.join(rads)
    data=data.set_index('rads')
    data=data.dropna()

    GraficoCarta2 = go.Figure()
    GraficoCarta2.add_trace(
        go.Scatterpolar(
            r = data['AMP_MOTOR'],
            theta = data['time'],
            mode = 'lines',
            name = 'Figure 8',
            line_color = '#8D10E4'
        ))
    GraficoCarta2.update_layout(
        #title = 'Carta Amperimétrica',
        showlegend = False,
        paper_bgcolor="rgb(248, 251, 254)",
        margin=dict(t=15, b=0, l=0, r=0),
        width=820,
        height=450,
    )
    GraficoCarta2.update_polars(
    
    #      Corrientes
    radialaxis_range=[0.5*data['AMP_MOTOR'].min(),1.1*data['AMP_MOTOR'].max()],
    radialaxis_angle = 45,
    radialaxis_autorange= False,
    #radialaxis_color="#8D10E4",
    
    #       Fechas
    angularaxis_tick0 = 0.1,
    angularaxis_nticks=8,
    angularaxis_tickfont_size=10,
    angularaxis_color="green",
    #angularaxis_linecolor="orange"
    
    )
    
    if slider[0]!=slider[1]:
        FechaCarta=f"{marks[slider[0]]} - {marks[slider[1]]}"
    elif  slider[0]==slider[1]:
        FechaCarta=f"{marks[slider[0]]}"
    
    
    return [GraficoCarta2, marks, Min, Max, FechaCarta]