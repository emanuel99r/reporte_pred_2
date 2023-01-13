from dash import Dash, html, dcc, ctx, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import json
import math
import dash


dash.register_page(__name__, title="Reporte Desempeño")

Encabezado = html.Div([
    
    html.Div(html.Img(src="/assets/Iguana.png",className="iconoECP")),
    
    html.Div([
        html.Div(id="nombre_pozo2", className="Titulo"),
        html.Div(id="nombre_gerencia2", className="SubTitulo") 
    ]),
    
    html.Div(html.Img(src="/assets/E2-logo.png",className="iconoE2"))
    
    ],className="TituloBox")
Nominales = html.Div([

        html.Div("Valores Nóminales", className="TituloNominales"),
        html.Div([html.Div("Variador de Frecuencia",className="TituloTabla"),dcc.Graph(id='TablaVFD2')], style={"margin-bottom":"10px"}),
        html.Div([html.Div("Transformador",className="TituloTabla"),dcc.Graph(id='TablaSUT2')]),
        html.Div([html.Div("Cable de Potencia",className="TituloTabla"),dcc.Graph(id='TablaCABLE2')]),
        html.Div([html.Div("Motor",className="TituloTabla"),dcc.Graph(id='TablaMOTOR2')]),
        html.Div([html.Div("Bomba",className="TituloTabla"),dcc.Graph(id='TablaBOMBA2')]),
     
], className="TablasNominales")
PeriodoReporte = html.Div([
    html.Div("Periodo del Reporte", className="TitlePeriodo"),
        html.Div([html.Div("Fecha Inicio: ", className="ItemOp"), html.Div("--", className="ItemOpR", id="fechaIni2")], className="Item"),
        html.Div([html.Div("Fecha Fin: ",    className="ItemOp"), html.Div("--", className="ItemOpR", id="fechaFin2")], className="Item"),
        ], className="PeriodoReporte")

Encabezado2 = html.Div([
    
    
    html.Div("RESUMEN",className="TituloResumen"),
    

    html.Div([
        html.Div([html.Img(src="/assets/Energia.svg", id="energiasvg"),html.Div("Energia",id="Energiatext",className="text"),html.Div("--",id="EnergiaValue",className="TextValue")]),
        html.Div([html.Img(src="/assets/Produccion.png" ,className="img"),html.Div("Produccion",id="Producciontext",className="text"),html.Div("--",id="ProduccionValue",className="TextValue")]),
        html.Div([html.Img(src="/assets/DesEne.svg", className="img"),html.Div("D. Energético",id="Energeticotext",className="text"),html.Div("--",id="D.EnergeticoValue",className="TextValue")]),
        html.Div([html.Img(src="/assets/DesAmb.png", className="img"),html.Div("D. Ambiental",id="Ambientaltext",className="text"),html.Div("--",id="D.AmbientalValue",className="TextValue")]),
        html.Div([html.Img(src="/assets/DesEco.png", className="img"),html.Div("D. Economico",id="Económicotext",className="text"),html.Div("--",id="D.EconomicoValue",className="TextValue")])
        
    ],className="iconos")

    
    ],className="TituloBox2")

Operatividad=html.Div([
    
    html.Div([
        
        html.Div([
        html.Div("Operatividad", className="TitleOpe"),
        html.Div(dcc.Graph(id='GraficoTorta2', className="GraficoTorta"))
                ]),
       
        html.Div([
        html.Div("Identificación Sistema - Bomba",   className="TitleSistema"),
        html.Div([html.Div("Mod. Operación: ",    className="ItemOp"), html.Div("Frecuencia", className="ItemOpR")], className="Item"),
        html.Div([html.Div("Frecuencia Base: ",      className="ItemOp"), html.Div("60"+" Hz",   className="ItemOpR")], className="Item")
        ], className="IdenSistema")
    
    ],className="OperatividadPadre")
])
GraficaCumpDea=html.Div([
    
    html.Div([
        html.Div("Cumplimiento",id="CumplimientoTitulo",className="Titulo1"),
        html.Div("[Energia Base / Energia Real]",id="CumplimientoTitulo2",className="Titulo1"),
        dcc.Graph(id="GraficoCumplimiento",className="Grafico")
    ],className="leftPanel"),
    
    html.Div([
        html.Div("Tendencia Acumulada del Desempeño Enérgetico",id="TituloDEA",className="Titulo"),
        # Se va modificar el grafico posteriormente
        html.Div(dcc.Graph(id="GraficoDEA"), className="Grafico"),
        html.Div("Cumplimiento: Es el consumo base dividido entre el consumo real (IB100). Desempeño: Resultado de la diferencia entre el consumo real y el consumo base multiplicado por la tarifa de enérgia. (-) indica ahorros (+) Indica sobreconsumos. GEI: Emisiones de Gases de efecto Invernadero, COP= Cifra expresada en millones de pesos colombianos.",id="CumplTXT",className="DEAtxt")
    ])


],className="GraficosCumpDea")


Cuerpo= html.Div([

    Encabezado,
    PeriodoReporte,
    Encabezado2,
    Nominales,
    Operatividad,
    GraficaCumpDea
    

    
],className="Cuerpo")

layout = dbc.Container([Cuerpo], class_name="ReportMain")


#Actualización de Variables
@callback(
    Output('GraficoTorta2','figure'),

    #Encabezado 1
    Output('nombre_pozo2', 'children'),
    Output('nombre_gerencia2', 'children'),

    #Encabezado 2
    
    #Operatividad
    Output('fechaIni2', 'children'),
    Output('fechaFin2', 'children'),
    Output('GraficoDEA','figure'),
    Output('GraficoCumplimiento','figure'),
    
    #Nominales
    Output('TablaVFD2', 'figure'),
    Output('TablaSUT2', 'figure'),
    Output('TablaCABLE2', 'figure'),
    Output('TablaMOTOR2', 'figure'),
    Output('TablaBOMBA2', 'figure'),

    Input('fechaIni2', 'children')

)
def actualizar_vars(var):
    
    Data=pd.read_csv("./DataGuardian.csv")
    Data2=pd.read_csv('./Iden.csv')
    f = open('./pozo.json')
    pozo = json.load(f)

    #-----------Operatividad----------------------------------------------
    nombre_pozo = "REPORTE DE DESEMPEÑO POZO "+pozo["Pozo"]
    nombre_gerencia = "GERENCIA DE "+pozo["Gerencia"]
    
    FECHAINI=Data["time"].iloc[0][0:10]
    FECHAFIN=Data["time"].iloc[-1][0:10]
    HORASON=Data["HORAS_ON"].sum()
    HORASOFF=Data["HORAS_OFF"].sum()

    labels = ['ON','OFF']
    values = [round(HORASON,1),round(HORASOFF,1)]  #Variables de Entrada Torta

    figTorta = go.Figure(data=[go.Pie(labels=labels, values=values)])
    figTorta.update_layout(

            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=25, r=25),
            annotations=[
            {
                "font": {
                "size": 10
                },
                "showarrow": False,
                "text": str(round(sum(values),1))+" Hrs",
                "x": 0.5,
                "y": 0.48
            },
            {
                "font": {
                "size": 10
                },
                "showarrow": False,
                "text": '<b>TOTAL</b>',
                "x": 0.5,
                "y": 0.55
            }]
                
    )
    figTorta.update_traces(
        hoverinfo='value',
        textinfo='label+percent',
        textfont_size=10,
        hole=.4,
        marker=dict(colors=["#108DE4", "#FF003D"])
        )
    
    #Grafico Desempeño energetico
   
    GraficoDEA=go.Figure()
    GraficoDEA.add_trace(go.Line(x=Data2["time"],
                                 y=Data2["Cusum"],
                                 line = dict(dash="dot", color="grey"),
                                 marker=dict(color="Red", size=5, symbol="square"),
                                 type="scatter", name="Cusum", mode="lines+markers",
                                 #fill='tonext',
                                 #fillcolor="rgb(248, 251, 254)"

                                 )
                                
                                 )
    '''print(Data2.shape)

    lista=[]
    for i in range(1,29):
        lista.append(30000)
    print(len(lista))'''

    GraficoDEA.add_trace(go.Line(x=Data2['time'],y=Data2["Cusum"]+1000000,
                                line = dict(dash="dot", color="gray"),
                                type="scatter",
                                fill='tonexty',
                                fillcolor="rgba(180,180,180,0.6)",
                                mode='lines'))
    
    GraficoDEA.update_layout(
            
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            plot_bgcolor='rgba(255, 255,255,0.6)',
            yaxis_title="Desviación del consumo de Energia [ kWh ]",
            yaxis_range=[Data2["Cusum"].min(),Data2["Cusum"].max()],
            xaxis_range=[Data2["time"].min(),Data2["time"].max()],
            width=500,
            height=500,
           
            )

    #Grafico Cumplimiento Indice Base 100
    Data3=pd.read_csv('Iden.csv')


    figCumplimiento=go.Figure(go.Indicator(
    mode = "gauge+number",
    value = Data3['IB100'].mean(),
    domain = {'x': [0, 1], 'y': [0, 1]},
    #title = {'text': "Cumplimiento", 'font': {'size': 24}},
    gauge = {
        'axis': {'range': [80,120], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "White"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [80, 100], 'color':'#FF0038'},
            {'range': [100, 120], 'color': 'green'}],
        'threshold': {
            'line': {'color': "black", 'width': 2},
            'thickness': 0.75,
            'value': 110}},
    title={'text':"Indice Base 100"},
    number={'suffix':"%"}
    #="bottom center"
    ))
    #figCumplimiento.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
    figCumplimiento.update_layout(
            
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=5),
            width=250,
            height=250,
            font_size=17
            )
    
    
    figVFD = go.Figure()
    Nominal=list(pozo["Nominales"]["VFD"].keys())
    Valor=[x[1][0] for x in pozo["Nominales"]["VFD"].items()]
    Unidad=[]
    for x in pozo["Nominales"]["VFD"].items():
        if len(x[1])==1:
            Unidad.append("-")
        else:
            Unidad.append(x[1][1])
    figVFD.add_trace(go.Table(
            header=dict(values=['<b>Nominal</b>', '<b>Valor</b>', '<b>Unidad</b>']),
            cells=dict(values=[Nominal,Valor,Unidad]),
            columnwidth = [90,90,90]
            ))
    figVFD.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=250,
            height=225,
            font_size=10
            )

    figSUT = go.Figure()
    Nominal=list(pozo["Nominales"]["SUT"].keys())
    Valor=[x[1][0] for x in pozo["Nominales"]["SUT"].items()]
    Unidad=[]
    for x in pozo["Nominales"]["SUT"].items():
        if len(x[1])==1:
            Unidad.append("-")
        else:
            Unidad.append(x[1][1])
    figSUT.add_trace(go.Table(
            header=dict(values=['<b>Nominal</b>', '<b>Valor</b>', '<b>Unidad</b>']),
            cells=dict(values=[Nominal,Valor,Unidad]),
            columnwidth = [90,90,90]
            ))
    figSUT.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=250,
            height=225,
            font_size=10
            )

    figCABLE = go.Figure()
    Nominal=list(pozo["Nominales"]["CABLE DE POTENCIA"].keys())
    Valor=[x[1][0] for x in pozo["Nominales"]["CABLE DE POTENCIA"].items()]
    Unidad=[]
    for x in pozo["Nominales"]["CABLE DE POTENCIA"].items():
        if len(x[1])==1:
            Unidad.append("-")
        else:
            Unidad.append(x[1][1])
    
    figCABLE.add_trace(go.Table(
            header=dict(values=['<b>Nominal</b>', '<b>Valor</b>', '<b>Unidad</b>']),
            cells=dict(values=[Nominal,Valor,Unidad]),
            columnwidth = [90,90,90]
            ))
    figCABLE.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=250,
            height=225,
            font_size=10
            )

    figMOTOR = go.Figure()
    Nominal=list(pozo["Nominales"]["Motor"].keys())
    Valor=[x[1][0] for x in pozo["Nominales"]["Motor"].items()]
    Unidad=[]
    for x in pozo["Nominales"]["Motor"].items():
        if len(x[1])==1:
            Unidad.append("-")
        else:
            Unidad.append(x[1][1])
    figMOTOR.add_trace(go.Table(
            header=dict(values=['<b>Nominal</b>', '<b>Valor</b>', '<b>Unidad</b>']),
            cells=dict(values=[Nominal,Valor,Unidad]),
            columnwidth = [90,90,90]
            ))
    figMOTOR.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=250,
            height=225,
            font_size=10
            )

    figBOMBA = go.Figure()
    Nominal=list(pozo["Nominales"]["BOMBA"].keys())
    Valor=[x[1][0] for x in pozo["Nominales"]["BOMBA"].items()]
    Unidad=[]
    for x in pozo["Nominales"]["BOMBA"].items():
        if len(x[1])==1:
            Unidad.append("-")
        else:
            Unidad.append(x[1][1])
    figBOMBA.add_trace(go.Table(
            header=dict(values=['<b>Nominal</b>', '<b>Valor</b>', '<b>Unidad</b>']),
            cells=dict(values=[Nominal,Valor,Unidad]),
            columnwidth = [90,90,90]
            ))
    figBOMBA.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=250,
            height=225,
            font_size=10
            )

    
    return[figTorta, nombre_pozo, nombre_gerencia, FECHAINI, FECHAFIN, GraficoDEA, figCumplimiento, 
           
           figVFD, figSUT, figCABLE, figMOTOR, figBOMBA]
