from dash import Dash, html, dcc, ctx, callback
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import json
import math
import numpy as np
import matplotlib.pyplot as plt

#app = Dash(__name__, assets_folder="assetsP", title="Reporte Predictivo")

dash.register_page(__name__, title="Reporte Predictivo")


listM1=[]
listM2=[]
listM3=[]
listOtros=[]
listTHDV=[]
listTHDI=[]
listFactores=[]

# ---------------- VARIABLES (Querys, csv, excel, json...)-------

Data=pd.read_csv("./DataGuardian.csv") #Se peude mover, solo invoca el item del DropDown...
Data.rename(
    columns={
        
        'THDVTPQM1T':'Arm. Total de Voltaje'
        
        }, inplace=True)

#Renombrar el resto..

for i,var in enumerate(Data.columns): 
    
    if  var!="time" and Data[var].sum()!=0:
        if "FPT" in var:
            listFactores.append(Data.columns[i]) 
        elif "M1" in var:
            listM1.append(Data.columns[i])
            if "THDV" in var:
                listTHDV.append(Data.columns[i])
            elif "THDI" in var and var!="THDITPQM1":
                listTHDI.append(Data.columns[i])
        elif "M2" in var:
            listM2.append(Data.columns[i])  
        elif "M3" in var:
            listM3.append(Data.columns[i])   
        else:
            listOtros.append(Data.columns[i])

#Guardar Gráficos (Prueba...)

#io.write_image(fig=figTorta,file="./img.jpg", format="jpeg",scale=None, width=None, height=None)
# pip install -U kaleido

#-------------------------------

Encabezado = html.Div([
    
    html.Div(html.Img(src="/assets/Iguana.png",className="iconoECP")),
    
    html.Div([
        html.Div(id="nombre_pozo", className="Titulo"),
        html.Div(id="nombre_gerencia", className="SubTitulo") 
    ]),
    
    html.Div(html.Img(src="/assets/E2-logo.png",className="iconoE2"))
    
    ],className="TituloBox")
Nominales = html.Div([

        html.Div("Valores Nóminales", className="TituloNominales"),
        html.Div([html.Div("Variador de Frecuencia",className="TituloTabla"),dcc.Graph(id='TablaVFD')], style={"margin-bottom":"10px"}),
        html.Div([html.Div("Transformador",className="TituloTabla"),dcc.Graph(id='TablaSUT')]),
        html.Div([html.Div("Cable de Potencia",className="TituloTabla"),dcc.Graph(id='TablaCABLE')]),
        html.Div([html.Div("Motor",className="TituloTabla"),dcc.Graph(id='TablaMOTOR')]),
        html.Div([html.Div("Bomba",className="TituloTabla"),dcc.Graph(id='TablaBOMBA')]),
     
], className="TablasNominales")
Operatividad=html.Div([
    
    html.Div([
        html.Div("Periodo del Reporte", className="TitlePeriodo"),
        html.Div([html.Div("Fecha Inicio: ", className="ItemOp"), html.Div("--", className="ItemOpR", id="fechaIni")], className="Item"),
        html.Div([html.Div("Fecha Fin: ",    className="ItemOp"), html.Div("--", className="ItemOpR", id="fechaFin")], className="Item"),
        ], className="Periodo"),
        
        html.Div([
        html.Div("Operatividad", className="TitleOpe"),
        html.Div(dcc.Graph(id='GraficoTorta', className="GraficoTorta"))
                ]),
       
        html.Div([
        html.Div("Identificación Sistema - Bomba",   className="TitleSistema"),
        html.Div([html.Div("Mod. Operación: ",    className="ItemOp"), html.Div("Frecuencia", className="ItemOpR")], className="Item"),
        html.Div([html.Div("Frecuencia Base: ",      className="ItemOp"), html.Div("60"+" Hz",   className="ItemOpR")], className="Item")
        ], className="IdenSistema")
    
    ],className="OperatividadPadre")
Diagrama = html.Div(
                [
                html.Div("",className="DiagramaECP"),

                html.Div(html.Div("VFD"),           className="CajaM", style={"top":"20px", "left":"415px"}),
                html.Div(html.Div("SUT"),           className="CajaM", style={"top":"20px", "left":"600px"}),
                html.Div(html.Div("MOTOR - BOMBA"), className="CajaM", style={"top":"20px", "left":"790px"}),
                
                html.Div(
                    [
                        html.Div("--"+" %",    id="EFIVFD",  className="CajaHijoVar"),
                        html.Div("--"+" %",    id="PCARGAVFD",     className="CajaHijoVar")
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"390px"}),
                
                html.Div(
                    [
                        html.Div("--"+" %",    id="EFISUT",  className="CajaHijoVar"),
                        html.Div("--"+" %",    id="PCARGASUT",     className="CajaHijoVar")
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"575px"}),
                
                html.Div(
                    [
                        html.Div("--"+" %",    id="EFIMB",     className="CajaHijoVar")
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"810px"}),
                
                html.Div(
                    [
                        html.Div(html.Div("Eficiencia")),
                        html.Div(html.Div("Porcentaje de Carga", style={"text-align": "right", "margin-top":"5px"}))
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"200px"}),
                
                html.Div(
                    [
                        html.Div([html.Div("Potencia Hidráulica"),      html.Div("--"+" kWhid", id="PotHid", className="CajaHijoVar",  style={"margin-bottom":"15px", "margin-left":"15px"})]),
                        html.Div([html.Div("Eficiencia del Sistema"),   html.Div("--"+" %", id="EfiSis", className="CajaHijoVar",      style={"margin-bottom":"15px", "margin-left":"18px"})])
                    ]
                         ,className="CajaM", style={"top":"350px", "left":"60px"}),
                
                
                html.Div(
                    [
                        html.Div([html.Div("Freq ",   className="CajaHijoName"),  html.Div("--"+" Hz",   id="FREQ_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Iin ",    className="CajaHijoName"),  html.Div("--"+" A",    id="AMP_M1",   className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Vin ",    className="CajaHijoName"),  html.Div("--"+" V",    id="VRMS_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("P. Ac ",  className="CajaHijoName"),  html.Div("--"+" kW",   id="POATC_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("P. Ap ",  className="CajaHijoName"),  html.Div("--"+" kVA",  id="POAPC_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("P. Re ",  className="CajaHijoName"),  html.Div("--"+" kVAr", id="POREC_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("FPin ",   className="CajaHijoName"),  html.Div("--"+" %",    id="FPOT_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Desv I ", className="CajaHijoName"),  html.Div("--"+" %",    id="DESVI_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Desv V ", className="CajaHijoName"),  html.Div("--"+" %",    id="DESVV_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("THDV ",   className="CajaHijoName"),  html.Div("--"+" %",    id="THDV_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("THDI ",   className="CajaHijoName"),  html.Div("--"+" %",    id="THDI_M1",  className="CajaHijoVar")], className="CajaHijo")
                    ]
                         ,className="CajaM", style={"top":"250px", "left":"260px"}),
                
                html.Div(
                    [
                        html.Div([html.Div("--"+" Hz",   id="FREQ_M2",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" A",    id="AMP_M2",   className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" V",    id="VRMS_M2",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kW",   id="POATC_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVA",  id="POAPC_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVAr", id="POREC_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="FPOT_M2",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVI_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVV_M2", className="CajaHijoVar")], className="CajaHijo")
                    ]
                         ,className="CajaM", style={"top":"250px", "left":"480px"}),
                
                html.Div(
                    [
                        html.Div([html.Div("--"+" Hz",   id="FREQ_M3",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" A",    id="AMP_M3",   className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" V",    id="VRMS_M3",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kW",   id="POATC_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVA",  id="POAPC_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVAr", id="POREC_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="FPOT_M3",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVI_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVV_M3", className="CajaHijoVar")], className="CajaHijo")
                    ]
                         ,className="CajaM", style={"top":"250px", "left":"660px"}),
                
                ],className="ImagenPadre", id="Diagrama")
Ventana = html.Div([
        
        html.Div("Ventana Operativa - Carta Amperimétrica",className="TendenciasTitle"),

        html.Div(dcc.Graph(id="GraficoVentana")),
        html.Div(dcc.Graph(id="GraficoCarta")),

    
    ], className="VentanaPadre")
EnergiaProd = html.Div([
    
        html.Div("Tendencias Acumuladas",className="TendenciasTitle"),
    
        html.Div([
            
            
                  html.Img(src="/assets/DesEne.png",className="iconoPE"),
                  html.Div("Energía", style={"font-weight":"bold"}),
                  html.Div("--"+" kWd", id="EneAcum")], className="EneProdHijo"),
    
        html.Div([
            html.Div([
                  html.Img(src="/assets/ProdAcum.png",className="iconoPE"),
                  html.Div("Producción", style={"font-weight":"bold", "text-align":"center"})
                    ], className="ProdAcum"),
                  html.Div([
                      html.Div([html.Div("Agua", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"BFPD", id="AguaAcum")], className="ItemProd"), 
                      html.Div([html.Div("Crudo", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"BFPD", id="CrudoAcum")], className="ItemProd"), 
                      html.Div([html.Div("Gas", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"und", id="GasAcum")], className="ItemProd"), 
                      html.Div([html.Div("Liquido", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"BFPD", id="LiqAcum")], className="ItemProd"), 
                    ], className="ProdAcumZ")
                  ], className="ProdAcumR"),
    
        html.Div([html.Img(src="/assets/IndConsumo.png",className="iconoPE"),
                  html.Div("Indice de Consumo", style={"font-weight":"bold"}),
                  html.Div("--", id="IC")], className="EneProdHijo"),
    
        html.Div([html.Img(src="/assets/Lutz.png",className="iconoPE"),
                  html.Div("Indice de Lutz", style={"font-weight":"bold"}),
                  html.Div("--", "Lutz")], className="EneProdHijo"),
    
    ], className="EneProdPadre")
Graficos=html.Div([
    
        html.Div("Mediciones de Variables", className="TituloTendencias"),
    
        html.Div([
            html.Div(dcc.Dropdown(listM1, 'POACTPQM1T_kW', id='DropM1', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoM1"), className="Grafico")
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listM2, 'POACTPQM2_kW', id='DropM2', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoM2"), className="Grafico")
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listM3, 'POACTPQM3_kW', id='DropM3', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoM3"), className="Grafico")
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listOtros, 'PIP_PSIG', id='DropOtro', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoOtro"), className="Grafico")
        ], className="GraficoHijo"),
                    
                    
    ],className="GraficosPadre")
CalidadEneA=html.Div([
    
        html.Div("Calidad de la Energía a la Entrada del Variador - Armónicos", className="TituloTendencias"),
        
        html.Div([
            html.Div("",style={"height":"45px"}),
            html.Div(dcc.Graph(id="GraficoTHDV"), className="GraficoCalidad"),
            dcc.Graph(id='TablaTHDV', style={"margin-left":"38px", "margin-top":"30px"}),
            html.Div(dcc.Graph(id="CumTHDV"), className="Grafico", style={"margin-left":"50px", "margin-top":"30px"}),
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listTHDI, 'THDI7PQM1', id='DropTHDI', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoTHDI"), className="GraficoCalidad"),
            dcc.Graph(id='TablaTHDI', style={"margin-left":"38px", "margin-top":"30px"}),
            html.Div(dcc.Graph(id="CumTHDI"), className="Grafico", style={"margin-left":"50px", "margin-top":"30px"})
        ], className="GraficoHijo"),
    
    
    ],className="ArmónicosPadre")
CalidadEneB=html.Div([
    
        html.Div("Calidad de la Energía - Factores de Potencia", className="TituloTendencias"),
        
        html.Div([
            html.Div(dcc.Dropdown(listFactores, 'FPTPQM1T', id='DropFactores', clearable=False), className="DropTags"),
            html.Div("",style={"height":"45px"}),
            html.Div(dcc.Graph(id="GraficoFactores"), className="GraficoCalidad"),
            dcc.Graph(id='TablaFactores', style={"margin-left":"38px", "margin-top":"30px"}),
            html.Div(dcc.Graph(id="CumFactores"), className="Grafico", style={"margin-left":"50px", "margin-top":"30px"}),
        ], className="GraficoHijo"),

    
    
    ],className="FactoresPadre")
Vibraciones=html.Div([
    
        html.Div("Análisis de Vibraciones", className="TituloTendencias"),
    
    
    ],className="VibracionesPadre")
Botones=html.Div(
        [
            dbc.Button('Descargar PDF', id='btn-Descargar', n_clicks=0, className="btn1"),
            #dbc.Button(children=['Download'],className="mr-1",id='js',n_clicks=0),

        ], className="Buttons") 

Cuerpo= html.Div([

    Encabezado,
    Nominales,
    Operatividad,
    Diagrama,
    Ventana,
    EnergiaProd,
    CalidadEneA,
    CalidadEneB,
    #Vibraciones,
    Graficos,
    #Botones,
    html.Div(id="Marca", className="MarcaText")
    
],className="Cuerpo")

layout = html.Div([html.Div([Cuerpo], className="ReportMain", id="Report"),
                       Botones])

def Rotulos(value):
    if value.find("_")!=-1:
        und=value[value.find("_")+1:]
        var=value[0:value.find("_")]
    else:
        var=value
        und=""
        
    return [und, var]

#Cambio en Gráficos
@callback(
    Output('GraficoM1', 'figure'),
    Output('GraficoM2', 'figure'),
    Output('GraficoM3', 'figure'),
    Output('GraficoOtro', 'figure'),
    Output('GraficoTHDV', 'figure'),
    Output('GraficoTHDI', 'figure'),
    Output('GraficoFactores', 'figure'),
    Output('CumTHDV', 'figure'),
    Output('CumTHDI', 'figure'),
    Output('CumFactores', 'figure'),
    Output('GraficoVentana', 'figure'),
    Output('GraficoCarta', 'figure'),
    Output('TablaTHDV', 'figure'),
    Output('TablaTHDI', 'figure'),
    Output('TablaFactores', 'figure'),
    
    Input('DropM1', 'value'),
    Input('DropM2', 'value'),
    Input('DropM3', 'value'),
    Input('DropTHDI', 'value'),
    Input('DropOtro', 'value'),
    Input('DropFactores', 'value')
)
def update_output(DropM1, DropM2, DropM3, DropTHDI, DropOtro, DropFactores):
    Data=pd.read_csv("./DataGuardian.csv")
    Data.rename(
    columns={
        
        'THDVTPQM1T':'Arm. Total de Voltaje'
        
        }, inplace=True)
    #print(Data.columns)

    HORASON=Data["HORAS_ON"].sum()
    
    GraficoM1 = go.Figure()
    GraficoM1.add_trace(go.Line(x=Data['time'], y=Data[str(DropM1)].dropna()))
    [undM1, varM1]=Rotulos(DropM1)
    GraficoM1.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undM1+"</b>",
            title={
            'text': f"<b>{varM1}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropM1)].min(),1.001*Data[str(DropM1)].max()]
            )
    GraficoM1.update_traces(line_color='#108DE4', line_width=1)
    GraficoM1.add_hrect(
        y0=Data[str(DropM1)].mean(), y1=Data[str(DropM1)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropM1)].mean(),2)} {undM1}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")

    GraficoM2 = go.Figure()
    GraficoM2.add_trace(go.Line(x=Data['time'], y=Data[str(DropM2)].dropna()))
    [undM2, varM2]=Rotulos(DropM2)
    GraficoM2.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undM2+"</b>",
            title={
            'text': f"<b>{varM2}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropM2)].min(),1.001*Data[str(DropM2)].max()]
            )
    GraficoM2.update_traces(line_color='#108DE4', line_width=1)
    GraficoM2.add_hrect(
        y0=Data[str(DropM2)].mean(), y1=Data[str(DropM2)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropM2)].mean(),2)} {undM2}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")
    
    GraficoM3 = go.Figure()
    GraficoM3.add_trace(go.Line(x=Data['time'], y=Data[str(DropM3)].dropna()))
    [undM3, varM3]=Rotulos(DropM3)
    GraficoM3.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undM3+"</b>",
            title={
            'text': f"<b>{varM3}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropM3)].min(),1.001*Data[str(DropM3)].max()]
            )
    GraficoM3.update_traces(line_color='#108DE4', line_width=1)
    GraficoM3.add_hrect(
        y0=Data[str(DropM3)].mean(), y1=Data[str(DropM3)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropM3)].mean(),2)} {undM3}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")
    
    GraficoOtro = go.Figure()
    GraficoOtro.add_trace(go.Line(x=Data['time'], y=Data[str(DropOtro)].dropna()))
    [undOtro, varOtro]=Rotulos(DropOtro)
    GraficoOtro.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undOtro+"</b>",
            title={
            'text': f"<b>{varOtro}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropOtro)].min(),1.001*Data[str(DropOtro)].max()]
            )
    GraficoOtro.update_traces(line_color='#108DE4', line_width=1)
    GraficoOtro.add_hrect(
        y0=Data[str(DropOtro)].mean(), y1=Data[str(DropOtro)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropOtro)].mean(),2)} {undOtro}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")
    
    limTHDV=8
    GraficoTHDV = go.Figure()
    GraficoTHDV.add_trace(go.Scatter(x=Data['time'], y=Data["Arm. Total de Voltaje"], mode="lines+markers",  marker=dict(size=3, color="green")))
    [und, var]=Rotulos("Arm. Total de Voltaje")
    GraficoTHDV.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            #yaxis_title="<b>"+und+"</b>",
            yaxis_title="<b>%</b>",
            title={
            'text': f"<b>{var}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.98*Data["Arm. Total de Voltaje"].min(),1.01*Data["Arm. Total de Voltaje"].max()]
            )
    GraficoTHDV.update_traces(line_color='#EF721B', line_width=0.5)
    GraficoTHDV.add_hrect(
        y0=Data["Arm. Total de Voltaje"].mean(), y1=Data["Arm. Total de Voltaje"].mean(), 
        line_color="#00552D", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data['Arm. Total de Voltaje'].mean(),2)} {und}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#00552D",
        line_dash="dot",
        row="3",
        col="all")
    GraficoTHDV.add_hrect(
        y0=limTHDV,
        y1=1.3*Data["Arm. Total de Voltaje"].max(),
        line_width=0,
        fillcolor="red", 
        opacity=0.1,
        annotation_text=f"Max: {limTHDV}%", 
        annotation_position="bottom right"
        )
    """
    GraficoTHDV.add_vrect(
            x0=Tiempos.iloc[i],
            x1=Tiempos.iloc[i+1], 
            annotation_text=" ",
            annotation_position="top left",
            fillcolor="#72EF1B", 
            opacity=0.25, 
            line_width=0) 
    """
    #IncumData=Data.query(f"'Arm. Total de Voltaje' > {limTHDV}")
    IncumData=Data[Data['Arm. Total de Voltaje']>limTHDV]
    Incum=IncumData["time"].count()
    Tiempos=pd.to_datetime(IncumData["time"], format="%Y-%m-%d %H:%M:%S")
    TiempoFuera=[]
    for i in range(1,len(Tiempos)-1):
        Diff=Tiempos.iloc[i+1].minute-Tiempos.iloc[i].minute
        TiempoFuera.append(Diff) 
    #CumData=Data.query(f"'Arm. Total de Voltaje' < {limTHDV}")
    CumData=Data[Data['Arm. Total de Voltaje']<limTHDV]
    Cum=CumData["time"].count()
    CumTHDV = go.Figure()
    CumTHDV.add_trace(go.Bar(
        y=['Cumplimiento'],
        x=[Incum/(Cum+Incum)*100],
        name=f'Mayor a {limTHDV}%',
        text=f"<b>{round(Incum/(Cum+Incum)*HORASON,1)} Horas</b>",
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 61, 0.6)',
            line=dict(color='rgba(255, 0, 61, 1.0)', width=2)
        )
    ))
    CumTHDV.add_trace(go.Bar(
        y=['Cumplimiento'],
        x=[Cum/(Cum+Incum)*100],
        name=f'Menor a {limTHDV}%',
        text=f"<b>{round(Cum/(Cum+Incum)*HORASON,1)} Horas</b>",
        orientation='h',
        marker=dict(
            color='rgba(16, 141, 228, 0.6)',
            line=dict(color='rgba(16, 141, 228, 1.0)', width=2)
        )
    ))
    CumTHDV.update_layout(
        barmode='stack',
        width=550,
        height=80,
        paper_bgcolor="rgb(248, 251, 254)",
        plot_bgcolor="rgb(248, 251, 254)",
        margin=dict(t=0, b=30, l=0, r=0),
        font_size=10,
        xaxis_title="<b>%</b>"
        )
    CumTHDV.update_traces(textfont_size=10, textangle=0, cliponaxis=False, textposition='inside')
    TablaTHDV = go.Figure()
    TablaTHDV.add_trace(go.Table(
            header=dict(values=['<b>Fecha</b>', '<b>Valor (%)</b>', '<b>Tiempo Fuera (min)</b>']),
            cells=dict(values=[IncumData["time"], IncumData["Arm. Total de Voltaje"], TiempoFuera]),
            columnwidth = [130,90,90,90]
            ))
    TablaTHDV.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=582,
            height=150,
            font_size=10
            )
    
    limTHDI=15
    GraficoTHDI = go.Figure()
    GraficoTHDI.add_trace(go.Line(x=Data['time'], y=Data[str(DropTHDI)], mode="lines+markers",  marker=dict(size=3, color="green")))
    [und, var]=Rotulos(DropTHDI)
    GraficoTHDI.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+und+"</b>",
            title={
            'text': f"<b>{var}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.98*Data[str(DropTHDI)].min(),1.01*Data[str(DropTHDI)].max()]
            )
    GraficoTHDI.update_traces(line_color='#EF721B', line_width=0.5)
    GraficoTHDI.add_hrect(
        y0=Data[str(DropTHDI)].mean(), y1=Data[str(DropTHDI)].mean(), 
        line_color="#00552D", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropTHDI)].mean(),2)} {und}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#00552D",
        line_dash="dot",
        row="3",
        col="all")
    GraficoTHDI.add_hrect(
        y0=limTHDI,
        y1=1.5*Data[str(DropTHDI)].max(),
        line_width=0,
        fillcolor="red", 
        opacity=0.1,
        annotation_text=f"Max: {limTHDI}%", 
        annotation_position="bottom right"
        )
    IncumData=Data.query(f"{DropTHDI} > {limTHDI}")
    Incum=IncumData[f"{DropTHDI}"].count()
    Tiempos=pd.to_datetime(IncumData["time"], format="%Y-%m-%d %H:%M:%S")
    TiempoFuera=[]
    for i in range(1,len(Tiempos)-1):
        Diff=Tiempos.iloc[i+1].minute-Tiempos.iloc[i].minute
        TiempoFuera.append(Diff) 
    CumData=Data.query(f"{DropTHDI} < {limTHDI}")
    Cum=CumData[f"{DropTHDI}"].count()
    CumTHDI = go.Figure()
    CumTHDI.add_trace(go.Bar(
        y=['Cumplimiento'],
        x=[Incum/(Cum+Incum)*100],
        text=f"<b>{round(Incum/(Cum+Incum)*HORASON,1)} Horas</b>",
        name=f'Mayor a {limTHDI}%',
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 61, 0.6)',
            line=dict(color='rgba(255, 0, 61, 1.0)', width=2)
        )
    ))
    CumTHDI.add_trace(go.Bar(
        y=['Cumplimiento'],
        x=[Cum/(Cum+Incum)*100],
        text=f"<b>{round(Cum/(Cum+Incum)*HORASON,1)} Horas</b>",
        name=f'Menor a {limTHDI}%',
        orientation='h',
        marker=dict(
            color='rgba(16, 141, 228, 0.6)',
            line=dict(color='rgba(16, 141, 228, 1.0)', width=2)
        )
    ))
    CumTHDI.update_layout(
        barmode='stack',
        width=550,
        height=80,
        paper_bgcolor="rgb(248, 251, 254)",
        plot_bgcolor="rgb(248, 251, 254)",
        margin=dict(t=0, b=30, l=0, r=0),
        font_size=10,
        xaxis_title="<b>%</b>")
    CumTHDI.update_traces(textfont_size=10, textangle=0, cliponaxis=False, textposition='inside')
    TablaTHDI = go.Figure()
    TablaTHDI.add_trace(go.Table(
            header=dict(values=['<b>Fecha</b>', '<b>Valor (%)</b>', '<b>Tiempo Fuera (min)</b>']),
            cells=dict(values=[IncumData["time"], IncumData[f"{DropTHDI}"], TiempoFuera]),
            columnwidth = [130,90,90,90]
            ))
    TablaTHDI.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=582,
            height=150,
            font_size=10
            )
    
    limFactores=90
    GraficoFactores = go.Figure()
    GraficoFactores.add_trace(go.Line(x=Data['time'], y=Data[str(DropFactores)], mode="lines+markers",  marker=dict(size=3, color="green")))
    [und, var]=Rotulos(DropFactores)
    GraficoFactores.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+und+"</b>",
            title={
            'text': f"<b>{var}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.98*Data[str(DropFactores)].min(),1.01*Data[str(DropFactores)].max()]
            )
    GraficoFactores.update_traces(line_color='#EF721B', line_width=0.5)
    GraficoFactores.add_hrect(
        y0=Data[str(DropFactores)].mean(), y1=Data[str(DropFactores)].mean(), 
        line_color="#00552D", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropFactores)].mean(),2)} {und}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#00552D",
        line_dash="dot",
        row="3",
        col="all")
    GraficoFactores.add_hrect(
        y0=limFactores,
        y1=1.5*Data[str(DropFactores)].max(),
        line_width=0,
        fillcolor="red", 
        opacity=0.1,
        annotation_text=f"Max: {limFactores}%", 
        annotation_position="bottom right"
        )
    IncumData=Data.query(f"{DropFactores} > {limFactores}")
    Incum=IncumData[f"{DropFactores}"].count()
    Tiempos=pd.to_datetime(IncumData["time"], format="%Y-%m-%d %H:%M:%S")
    TiempoFuera=[]
    for i in range(1,len(Tiempos)-1):
        Diff=Tiempos.iloc[i+1].minute-Tiempos.iloc[i].minute
        TiempoFuera.append(Diff) 
    CumData=Data.query(f"{DropFactores} < {limFactores}")
    Cum=CumData[f"{DropFactores}"].count()
    CumFactores = go.Figure()
    CumFactores.add_trace(go.Bar(
        y=['Cumplimiento'],
        x=[Incum/(Cum+Incum)*100],
        text=f"<b>{round(Incum/(Cum+Incum)*HORASON,1)} Horas</b>",
        name=f'Mayor a {limFactores}%',
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 61, 0.6)',
            line=dict(color='rgba(255, 0, 61, 1.0)', width=2)
        )
    ))
    CumFactores.add_trace(go.Bar(
        y=['Cumplimiento'],
        x=[Cum/(Cum+Incum)*100],
        text=f"<b>{round(Cum/(Cum+Incum)*HORASON,1)} Horas</b>",
        name=f'Menor a {limFactores}%',
        orientation='h',
        marker=dict(
            color='rgba(16, 141, 228, 0.6)',
            line=dict(color='rgba(16, 141, 228, 1.0)', width=2)
        )
    ))
    CumFactores.update_layout(
        barmode='stack',
        width=550,
        height=80,
        paper_bgcolor="rgb(248, 251, 254)",
        plot_bgcolor="rgb(248, 251, 254)",
        margin=dict(t=0, b=30, l=0, r=0),
        font_size=10,
        xaxis_title="<b>%</b>")
    CumFactores.update_traces(textfont_size=10, textangle=0, cliponaxis=False, textposition='inside')
    TablaFactores = go.Figure()
    TablaFactores.add_trace(go.Table(
            header=dict(values=['<b>Fecha</b>', '<b>Valor (%)</b>', '<b>Tiempo Fuera (min)</b>']),
            cells=dict(values=[IncumData["time"], IncumData[f"{DropFactores}"], TiempoFuera]),
            columnwidth = [130,90,90,90]
            ))
    TablaFactores.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            width=582,
            height=150,
            font_size=10
            )

    f = open('./pozo.json')
    pozo = json.load(f)
    pozo=pozo["Pozo"]
    
    f= open('./Curvas.json')
    Curvas = json.load(f)
    API=Curvas[pozo]["API"][0]

    Data['time'] = pd.to_datetime(Data['time'])
    df = Data.set_index('time')
    df = df.resample('D').mean()
    VLiq=list(df["VOLUMEN_LIQUIDO"].dropna())
    PIP=list(df["PIP_PSIG"])
    PDP=list(df["PDP_PSIG"])
    GE= 141.5/(API+131.5)
    TDH=[(PDP[i]-PIP[i])*2.31/GE for i,x in enumerate(PDP)]
    
    
    try:
        
        if pozo=="CH0100":
            
            GraficoVentana = go.Figure()#        Nombre del Pozo..
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz60"], line = dict(width=2,color = "#00FF88", dash="dash"), type="scatter", name="60Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz40"], line = dict(width=2,color = "#108DE4", dash="dash"), type="scatter", name="40Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R1"], line = dict(width=2,color = "#EF721B", dash="dash"), type="scatter", name="R1", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R2"], line = dict(width=2,color = "#8D10E4", dash="dash"), type="scatter", name="R2", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R3"], line = dict(width=2,color = "#F95738", dash="dash"), type="scatter", name="R3", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R4"], line = dict(width=2,color = "Purple", dash="dash"), type="scatter", name="R4", mode="lines"))
            GraficoVentana.add_trace(go.Line(x=VLiq, y=TDH, line = dict(dash="dot"), marker=dict(color="Orange", size=5), type="scatter", name="Punto. Op. Histórica", mode="markers"))
            GraficoVentana.add_trace(go.Scatter(x=[VLiq[-1]], y=[TDH[-1]], line = dict(dash="dot"), marker=dict(color="Green", size=8, symbol="star-square-dot"), type="scatter", name="Punto. Op. Actual", mode="markers"))
            GraficoVentana.update_layout(
                    showlegend=True,
                    paper_bgcolor="rgb(248, 251, 254)",
                    margin=dict(t=15, b=0, l=0, r=0),
                    width=620,
                    height=300,
                    font_size=10,
                    yaxis_title="TDH (ft)",
                    title={
                    'text': f"Ventana Operativa",
                    'y':1,
                    'x':0.40,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    xaxis_range=Curvas[pozo]["LimX"],
                    yaxis_range=Curvas[pozo]["LimY"]
                    )
            
        elif pozo=="SU74":
            
            GraficoVentana = go.Figure()#        Nombre del Pozo..
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz60"], line = dict(width=2,color = "#00FF88", dash="dash"), type="scatter", name="60Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz40"], line = dict(width=2,color = "#108DE4", dash="dash"), type="scatter", name="40Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R1"], line = dict(width=2,color = "#EF721B", dash="dash"), type="scatter", name="Min Opt. OP", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R2"], line = dict(width=2,color = "#8D10E4", dash="dash"), type="scatter", name="MIN ROR FLT", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R3"], line = dict(width=2,color = "#F95738", dash="dash"), type="scatter", name="BEP", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R4"], line = dict(width=2,color = "Purple", dash="dash"), type="scatter", name="Max Opt. OP", mode="lines"))
            GraficoVentana.add_trace(go.Line(x=VLiq, y=TDH, line = dict(dash="dot"), marker=dict(color="Orange", size=5), type="scatter", name="Punto. Op. Histórica", mode="markers"))
            GraficoVentana.add_trace(go.Scatter(x=[VLiq[-1]], y=[TDH[-1]], line = dict(dash="dot"), marker=dict(color="Green", size=8, symbol="star-square-dot"), type="scatter", name="Punto. Op. Actual", mode="markers"))
            GraficoVentana.update_layout(
                    showlegend=True,
                    paper_bgcolor="rgb(248, 251, 254)",
                    margin=dict(t=15, b=0, l=0, r=0),
                    width=620,
                    height=300,
                    font_size=10,
                    yaxis_title="TDH (ft)",
                    title={
                    'text': f"Ventana Operativa",
                    'y':1,
                    'x':0.40,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    xaxis_range=Curvas[pozo]["LimX"],
                    yaxis_range=Curvas[pozo]["LimY"]
                    )
      
        elif pozo=="SU05":
            
            GraficoVentana = go.Figure()#        Nombre del Pozo..
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz60"], line = dict(width=2,color = "#00FF88", dash="dash"), type="scatter", name="60Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz40"], line = dict(width=2,color = "#108DE4", dash="dash"), type="scatter", name="40Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R1"], line = dict(width=2,color = "#EF721B", dash="dash"), type="scatter", name="R1", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R2"], line = dict(width=2,color = "#8D10E4", dash="dash"), type="scatter", name="R2", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["R3"], line = dict(width=2,color = "#F95738", dash="dash"), type="scatter", name="R3", mode="lines"))
            GraficoVentana.add_trace(go.Line(x=VLiq, y=TDH, line = dict(dash="dot"), marker=dict(color="Orange", size=5), type="scatter", name="Punto. Op. Histórica", mode="markers"))
            GraficoVentana.add_trace(go.Scatter(x=[VLiq[-1]], y=[TDH[-1]], line = dict(dash="dot"), marker=dict(color="Green", size=8, symbol="star-square-dot"), type="scatter", name="Punto. Op. Actual", mode="markers"))
            GraficoVentana.update_layout(
                    showlegend=True,
                    paper_bgcolor="rgb(248, 251, 254)",
                    margin=dict(t=15, b=0, l=0, r=0),
                    width=620,
                    height=300,
                    font_size=10,
                    yaxis_title="TDH (ft)",
                    title={
                    'text': f"Ventana Operativa",
                    'y':1,
                    'x':0.40,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    xaxis_range=Curvas[pozo]["LimX"],
                    yaxis_range=Curvas[pozo]["LimY"]
                    )
            
        else:
            
            GraficoVentana = go.Figure()#        Nombre del Pozo..
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz60"], line = dict(width=2,color = "#00FF88", dash="dash"), type="scatter", name="60Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["Hz40"], line = dict(width=2,color = "#108DE4", dash="dash"), type="scatter", name="40Hz", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["BEP08"], line = dict(width=2,color = "#EF721B", dash="dash"), type="scatter", name="0.8*BEP", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["BEP"], line = dict(width=2,color = "#8D10E4", dash="dash"), type="scatter", name="BEP", mode="lines"))
            GraficoVentana.add_trace(go.Line(Curvas[pozo]["BEP12"], line = dict(width=2,color = "#F95738", dash="dash"), type="scatter", name="1.2*BEP", mode="lines"))
            GraficoVentana.add_trace(go.Line(x=VLiq, y=TDH, line = dict(dash="dot"), marker=dict(color="Orange", size=5), type="scatter", name="Punto. Op. Histórica", mode="markers"))
            GraficoVentana.add_trace(go.Scatter(x=[VLiq[-1]], y=[TDH[-1]], line = dict(dash="dot"), marker=dict(color="Green", size=8, symbol="star-square-dot"), type="scatter", name="Punto. Op. Actual", mode="markers"))
            GraficoVentana.update_layout(
                    showlegend=True,
                    paper_bgcolor="rgb(248, 251, 254)",
                    margin=dict(t=15, b=0, l=0, r=0),
                    width=620,
                    height=300,
                    font_size=10,
                    yaxis_title="TDH (ft)",
                    title={
                    'text': f"Ventana Operativa",
                    'y':1,
                    'x':0.40,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    xaxis_range=Curvas[pozo]["LimX"],
                    yaxis_range=Curvas[pozo]["LimY"]
                    )
                
    except:
        
         GraficoVentana = go.Figure()
         GraficoVentana.update_layout(
                showlegend=True,
                paper_bgcolor="rgb(248, 251, 254)",
                margin=dict(t=15, b=0, l=0, r=0),
                width=620,
                height=300,
                font_size=10,
                yaxis_title="TDH (ft)",
                title={
                'text': f"Ventana Operativa NO DISPONIBLE",
                'y':1,
                'x':0.45,
                'xanchor': 'center',
                'yanchor': 'top'},
                xaxis_range=[0,20000],
                yaxis_range=[0,6000]
                )

    GraficoCarta = go.Figure()

    # Constants
    img_width = 840
    img_height = 580
    scale_factor = 0.5
    
    GraficoCarta.add_trace(
    go.Scatter(
        x=[0, img_width * scale_factor],
        y=[0, img_height * scale_factor],
        mode="markers",
        marker_opacity=0
        )
    )
    # Configure axes
    GraficoCarta.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )
    GraficoCarta.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )
    GraficoCarta.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source="/assets/Carta_amperimetrica.png")
    )
    GraficoCarta.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    #Que % está fuera de rango y en qué rangos de tiempo... estadistica de ello
    
    """    
    
    data=pd.DataFrame(pd.read_csv('./Data_Corriente.csv'))
    data['time']=pd.to_datetime(data['time'], utc=True)
    #data["time"].dt.strftime('%d,%m,%Y')
    data['time']=data['time']+pd.DateOffset(hours=-5)  
    data['time']=data['time'].dt.strftime('%d %h %Y,%H:%M:%S')
    print(data)
    # setting the axes projection as polar
    plt.axes(projection = 'polar')
    
    # setting the radius
    r = 1.5
    
    # creating an array containing the
    # radian values
    delta=(2 * np.pi)/len(data)
    rads = np.arange(0, (2 * np.pi), delta)
    rads=pd.DataFrame(rads,columns=['rads'])
    data=data.join(rads)
    data=data.set_index('rads')
    data=data.dropna()

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(data.index, data['AMP_MOTOR'])
    ax.set_rmax(130)
    ax.set_rmin(50)
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    #ax.set_rticks([250,350])  # Less radial ticks
    #ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    delta2=int(len(data)/4)
    ax.set_xticklabels([str(data.iloc[0]['time']), '', str(data.iloc[0+delta2]['time']), '', str(data.iloc[0+delta2*2]['time']), '', str(data.iloc[0+delta2*3]['time']), ''])
    ax.grid(True)
    ax.set_title("Carta Amperimétrica", va='bottom')
    
    GraficoCarta2=fig
    
    """
    
    return [GraficoM1, GraficoM2, GraficoM3, GraficoOtro, GraficoTHDV, GraficoTHDI, GraficoFactores, CumTHDV, CumTHDI, CumFactores, GraficoVentana, GraficoCarta, TablaTHDV, TablaTHDI, TablaFactores]

#Actualización de Variables
@callback(
    Output('GraficoTorta', 'figure'),
    Output('nombre_pozo', 'children'),
    Output('nombre_gerencia', 'children'),
    
    Output('TablaVFD', 'figure'),
    Output('TablaSUT', 'figure'),
    Output('TablaCABLE', 'figure'),
    Output('TablaMOTOR', 'figure'),
    Output('TablaBOMBA', 'figure'),
    Output('fechaIni', 'children'),
    Output('fechaFin', 'children'),
    
    Output('VRMS_M1', 'children'),
    Output('VRMS_M2', 'children'),
    Output('VRMS_M3', 'children'),
    Output('FREQ_M1', 'children'),
    Output('AMP_M1', 'children'),
    Output('POATC_M1', 'children'),
    Output('POAPC_M1', 'children'),
    Output('POREC_M1', 'children'),
    Output('FPOT_M1', 'children'),
    Output('DESVI_M1', 'children'),
    Output('DESVV_M1', 'children'),
    Output('THDV_M1', 'children'),
    Output('THDI_M1', 'children'),
    
    Output('FREQ_M2', 'children'),
    Output('AMP_M2', 'children'),
    Output('POATC_M2', 'children'),
    Output('POAPC_M2', 'children'),
    Output('POREC_M2', 'children'),
    Output('FPOT_M2', 'children'),
    Output('DESVI_M2', 'children'),
    Output('DESVV_M2', 'children'),

    Output('FREQ_M3', 'children'),
    Output('AMP_M3', 'children'),
    Output('POATC_M3', 'children'),
    Output('POAPC_M3', 'children'),
    Output('POREC_M3', 'children'),
    Output('FPOT_M3', 'children'),
    Output('DESVI_M3', 'children'),
    Output('DESVV_M3', 'children'),
    
    Output('EFIVFD', 'children'),
    Output('EFISUT', 'children'),
    Output('EFIMB', 'children'),
    Output('PotHid', 'children'),
    Output('EfiSis', 'children'),
    Output('PCARGAVFD', 'children'),
    Output('PCARGASUT', 'children'),
    
    Output('EneAcum', 'children'),
    Output('AguaAcum', 'children'),
    Output('CrudoAcum', 'children'),
    Output('GasAcum', 'children'),
    Output('LiqAcum', 'children'),
    Output('IC', 'children'),
    Output('Lutz', 'children'),
    
    #Output('THDV_M1', 'children'),

    
    Input('PCARGAVFD', 'children')
)
def actualizar_vars(var):
    
    Data=pd.read_csv("./DataGuardian.csv")
    f = open('./pozo.json')
    pozo = json.load(f)
    
    #------------Nominales-----------------------------------------------

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
    

    #-----------Operatividad----------------------------------------------
    nombre_pozo = "REPORTE PREDICTIVO POZO "+pozo["Pozo"]
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

    #---------------- M1 -----------------------------------------------------------------------------------------

    VM1=str(round((Data["VABPQM1T_volt"].mean()+Data["VBCPQM1T_volt"].mean()+Data["VCAPQM1T_volt"].mean())/3,2))
    FREQM1 = str(round(Data["FREQPQM1_Hz"].mean(),2))
    AMPM1 = str(round((Data["AMPAPQM1T_amp"].mean()+Data["AMPBPQM1T_amp"].mean()+Data["AMPCPQM1T_amp"].mean())/3,2))
    POACTM1 = str(round(Data["POACTPQM1T_kW"].mean(),2))
    POAPM1 = str(round(math.sqrt(math.pow(Data["POACTPQM1T_kW"].mean(),2)+math.pow(Data["PORETPQM1T_kvar"].mean(),2)),2))
    POREM1 = str(round(Data["PORETPQM1T_kvar"].mean(),1))
    FPOTM1 = str(round(Data["FPTPQM1T"].mean(),2))
    DESVIM1 = str(round(Data["DESAMPM1_%"].mean(),2))
    DESVVM1 = str(round(Data["DESVMPM1_%"].mean(),2))
    THDVM1 = str(round(Data["THDVTPQM1T"].mean(),2))
    THDIM1 = str(round(Data["THDITPQM1T"].mean(),2))

    #---------------- M2 -----------------------------------------------------------------------------------------

    VM2=str(round((Data["VABPQM2_volt"].mean()+Data["VBCPQM2_volt"].mean()+Data["VCAPQM2_volt"].mean())/3,2))
    FREQM2 = str(round(Data["FREQPQM2_Hz"].mean(),2))
    AMPM2 = str(round((Data["AMPAPQM2_amp"].mean()+Data["AMPBPQM2_amp"].mean()+Data["AMPCPQM2_amp"].mean())/3,2))
    POACTM2 = str(round(Data["POACTPQM2_kW"].mean(),2))
    POACTM2 = str(round(Data["POACTPQM2_kW"].mean(),2))
    POAPM2 = str(round(math.sqrt(math.pow(Data["POACTPQM2_kW"].mean(),2)+math.pow(Data["PORETPQM2_kvar"].mean(),2)),2))
    POREM2 = str(round(Data["PORETPQM2_kvar"].mean(),1))
    FPOTM2 = str(round(Data["FPTPQM2"].mean(),2))
    DESVIM2 = str(round(Data["DESAMPM2_%"].mean(),2))
    DESVVM2 = str(round(Data["DESVMPM2_%"].mean(),2))

    #---------------- M3 -----------------------------------------------------------------------------------------

    VM3=str(round((Data["VABPQM3_volt"].mean()+Data["VBCPQM3_volt"].mean()+Data["VCAPQM3_volt"].mean())/3,2))
    FREQM3 = FREQM2
    AMPM3 = str(round((Data["AMPAPQM3_amp"].mean()+Data["AMPBPQM3_amp"].mean()+Data["AMPCPQM3_amp"].mean())/3,2))
    POACTM3 = str(round(Data["POACTPQM3_kW"].mean(),2))
    POACTM3 = str(round(Data["POACTPQM3_kW"].mean(),2))
    POAPM3 = str(round(math.sqrt(math.pow(Data["POACTPQM3_kW"].mean(),2)+math.pow(Data["PORETPQM3_kvar"].mean(),2)),2))
    POREM3 = str(round(Data["PORETPQM3_kvar"].mean(),1))
    FPOTM3 = str(round(Data["FPTPQM3"].mean(),2))
    DESVIM3 = str(round(Data["DESAMPM3_%"].mean(),2))
    DESVVM3 = str(round(Data["DESVMPM3_%"].mean(),2))
    
    #--------------------OTROS CÁLCULOS--------------------------------------------------------------------------
    
    EFIVFD=str(round(float(POACTM2)/float(POACTM1)*100,2))
    EFISUT=str(round(float(POACTM3)/float(POACTM2)*100,2))
    EFIMB="--"
    PotHid=str(round(Data["POT_HID"].mean(),2))
    EfiSis=str(round(float(PotHid)/float(POACTM1)*100,2))
    PNom=pozo["Nominales"]["VFD"]["Potencia Nominal"][0]
    PCARGAVFD=str(round(float(POAPM1)/PNom*100,2))
    PNom=pozo["Nominales"]["SUT"]["Potencia Nominal"][0]
    PCARGASUT=str(round(float(POAPM2)/PNom*100,2))
    
    
    EneAcum=str(round(Data["POACTPQM1T_kW"].sum()/20,2))
    AguaAcum=str(round(Data["AGUA"].sum(),2)) #suma
    CrudoAcum=str(round(Data["CRUDO"].sum(),2)) #suma
    GasAcum="--"
    LiqAcum=str(round(Data["AGUA"].sum()+Data["CRUDO"].sum(),2))
    IC=str(round(float(EneAcum)/float(LiqAcum),2))
    Lutz="--"
 
    return [figTorta, nombre_pozo, nombre_gerencia, 
            
            figVFD, figSUT, figCABLE, figMOTOR, figBOMBA, FECHAINI, FECHAFIN, 
            
            VM1+" V", VM2+" V", VM3+" V", FREQM1+" Hz", AMPM1+" A",
            POACTM1+" kW", POAPM1+" kVA", POREM1+" kVAR", FPOTM1+" %", DESVIM1+" %", DESVVM1+" %", THDVM1+" %", THDIM1+" %",
            
            FREQM2+" Hz", AMPM2+" A",
            POACTM2+" kW", POAPM2+" kVA", POREM2+" kVAR", FPOTM2+" %", DESVIM2+" %", DESVVM2+" %",
            
            FREQM3+" Hz", AMPM3+" A", POACTM3+" kW", POAPM3+" kVA", POREM3+" kVAR", FPOTM3+" %", DESVIM3+" %", DESVVM3+" %",
            
            EFIVFD+" %", EFISUT+" %", EFIMB+" %", PotHid+" kWhid", EfiSis+" %",
            PCARGAVFD+" %", PCARGASUT+" %", EneAcum+" kWd", AguaAcum+" BFPD", CrudoAcum+" BFPD",
            GasAcum+" BFPD", LiqAcum+" BFPD", IC, Lutz
            
            ]

dash.clientside_callback( 
    """
    
        function(n_clicks){
        if(n_clicks > 0){
            
            let Hoy = new Date();
            let HoyS = Hoy.toLocaleDateString();
            document.querySelector("#Marca").innerHTML = "Reporte Generado por E2 Energía Eficiente el "+HoyS.toString();
            
            html2canvas(document.querySelector("#Report")).then(canvas => {
            
            var imgData = canvas.toDataURL('image/png');
            var doc = new jsPDF('p', 'mm', "a2");
            
            const pageHeight = doc.internal.pageSize.getHeight();
            const imgWidth = doc.internal.pageSize.getWidth();
            var imgHeight = canvas.height * imgWidth / canvas.width;
            var heightLeft = imgHeight;
            
            
            var position = 3; // give some top padding to first page

            doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;

            while (heightLeft >= 0) {
            position += heightLeft - imgHeight; // top padding for other pages
            doc.addPage();
            doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
            
            }
    
            doc.save('Reporte Predictivo.pdf');
            
})}}
    
    """
    ,
    Output('btn-Descargar','n_clicks'),
    Input('btn-Descargar','n_clicks')
)

if __name__ == '__main__':
    app.run_server(debug=True)
