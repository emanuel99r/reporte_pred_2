from dash import Dash, html, dcc, ctx, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import json
import numpy as np
import dash


dash.register_page(__name__, title="Reporte de Desempeño")

listaDropdown=["IndiceConsumo","IB100","GEI","D.Energetico", "D.Ambiental", "D.Economico"]


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
    html.Div("Periodo del Reporte ",id="TitlePeriodo", className="Titulo1"),
        html.Div("(AAAA-MM-DD)", id="FormatoFecha"),
        html.Div([html.Div("Fecha Inicio: ", className="ItemOp"), html.Div("--", className="ItemOpR",style={"font-weight":"100"}, id="fechaIni2")], className="Item"),
        html.Div([html.Div("Fecha Fin: ",    className="ItemOp"), html.Div("--", className="ItemOpR",style={"font-weight":"100"}, id="fechaFin2")], className="Item"),
        ], className="PeriodoReporte")

Encabezado2 = html.Div([
    
    
    html.Div("Resumen",className="TituloNominales"),
    
    

    html.Div([
        html.Div([html.Img(src="/assets/Energia.png", id="energiasvg"),html.Div("Energia",id="Energiatext",className="text"),html.Div("--",id="EnergiaValue",className="ItemProd")]),
               html.Div([
            html.Div([
                  html.Img(src="/assets/ProdAcum.png",className="iconoPE"),
                  html.Div("Producción", style={"font-weight":"bold", "text-align":"center"})
                    ], className="ProdAcum"),
                  html.Div([
                      html.Div([html.Div("Agua", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"BFPD", id="AguaAcum1")], className="ItemProd"), 
                      html.Div([html.Div("Crudo", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"BFPD", id="CrudoAcum1")], className="ItemProd"), 
                      html.Div([html.Div("Gas", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"und", id="GasAcum1")], className="ItemProd"), 
                      html.Div([html.Div("Liquido", style={"font-weight":"bold", "margin-bottom":"10px"}),html.Div("--"+"BFPD", id="LiqAcum1")], className="ItemProd"), 
                    ], className="ProdAcumZ")
                  ], className="ProdAcumR"),
        html.Div([html.Img(src="/assets/DesEne.png", className="img"),html.Div("D.Energético",id="Energeticotext",className="text"),html.Div("--",id="DEnergeticoValue",style={"font-weight":"100"},className="TextValue")]),
        html.Div([html.Img(src="/assets/DesAmb.png", className="img"),html.Div("D. Ambiental",id="Ambientaltext",className="text"),html.Div("--",id="DAmbientalValue",style={"font-weight":"100"},className="TextValue"),
                html.Div("Factor Emision: 0.126 Kg CO2eq/kWh",className="Factores")]),
        html.Div([html.Img(src="/assets/DesEco.png", className="img"),html.Div("D. Economico",id="Economicotext",className="text"),html.Div("--",id="DEconomicoValue",style={"font-weight":"100"},className="TextValue"),
            html.Div("Tarifa: $350 COP/kWh",className="Factores")])
        
    ],className="iconos")

    
    ],className="TituloBox2")

Operatividad=html.Div([
    
    html.Div([
        
        html.Div([
        html.Div("Operatividad", className="Titulo1"),
        html.Div(dcc.Graph(id='GraficoTorta2', className="GraficoTorta"))
                ]),
       
        html.Div([
        html.Div("Identificación Sistema - Bomba",   className="TitleSistema"),
        html.Div([html.Div("Mod. Operación: ",    className="ItemOp"), html.Div("Frecuencia", className="ItemOpR")], className="Item"),
        html.Div([html.Div("Frecuencia Base: ",      className="ItemOp"), html.Div("60"+" Hz",   className="ItemOpR")], className="Item")
        ], className="IdenSistema")
    
    ],className="OperatividadPadreD")
])
GraficaCumpDea=html.Div([
    
    html.Div([
        html.Div("Porcentaje Cumplimiento \n Indice Base 100",id="CumplimientoTitulo",className="Titulo1"),
        html.Div("[Energia Base / Energia Real]",id="CumplimientoTitulo2",className="Titulo1"),
        dcc.Graph(id="GraficoCumplimiento",className="Grafico")
    ],className="leftPanel"),
    
    html.Div([
        html.Div("Tendencia Acumulada del Desempeño Enérgetico",id="TituloDEA",className="Titulo1"),
        # Se va modificar el grafico posteriormente 
        html.Div(dcc.Graph(id="GraficoDEA"), className="Grafico"),
        html.Div("Cumplimiento: Es el consumo base dividido entre el consumo real (IB100). Desempeño: Resultado de la diferencia entre el consumo real y el consumo base multiplicado por la tarifa de enérgia. (-) indica ahorros (+) Indica sobreconsumos. GEI: Emisiones de Gases de efecto Invernadero, COP= Cifra expresada en millones de pesos colombianos.",id="CumplTXT",className="DEAtxt")
    ])


],className="GraficosCumpDea")

GraficaIndiceConsumo=html.Div([
    

    html.Div("Indicadores",className="Titulo1"),

    html.Div([
        
        html.Div(dcc.Dropdown(listaDropdown,"D.Energetico", id='DropIndicadores',clearable=False),className="DropTags"),
        html.Div(dcc.Graph(id="GraphVariablesid"),className='GraficoIndicadoresClass'),
    ],className="ContenedorGraphDrop"),
    



],className="GraficosVariables")

SankeyCont=html.Div([
    

    html.Div("Diagrama Sankey",className="Titulo1"),

    html.Div([
        
        html.Div(dcc.Graph(id="SankeyGraphicPOAC"),className='SankeyGraphicClass'),
        html.Div([dcc.Graph(id="SankeyGraphicPerdidas",className='SankeyGraphicClass'),html.Div("* Basado en el promedio de las potencias", id="SankeyComment")]),

    
    
    ],className="SankeyContChild"),

    
    



],className="SankeyCont")

Data=pd.read_csv("./DataGuardian.csv") #Se peude mover, solo invoca el item del DropDown...
listMultiSelect=list(Data.columns)+['DeltaE', 'IB100', 'GEI', 'IndiceConsumo', 'D.Energetico', 'D.Ambiental', 'D.Economico']
listMultiSelect.pop(0)

TenMultiSelect=html.Div([
    
    dcc.Graph(id="GraficoMulti2"),
    html.Div([
              html.Div(dcc.Dropdown(listMultiSelect,['IndiceConsumo','DeltaE', "IB100"],id="DropMulti2", multi=True, placeholder="Seleccione las señales a graficar"), style={"width":"40%", "margin-right":"5px"}), 
              dbc.Button('Reset', id='resetMulti2', n_clicks=0, className="btn_reset")
                         
             ], className="DropMultiSelect")
    
], className="MultiSelectPadre")


Botones=html.Div(
        [
            dbc.Button('Descargar PDF', id='btn-Descargar2', n_clicks=0, className="btn1")

        ], className="Buttons")



Cuerpo= html.Div([

    Encabezado,
    PeriodoReporte,
    Encabezado2,
    Nominales,
    Operatividad,
    GraficaCumpDea,
    GraficaIndiceConsumo,
    SankeyCont,
    TenMultiSelect,
    html.Div(id="Marca2", className="MarcaText")
    

    
],className="Cuerpo")

layout = html.Div([html.Div([Cuerpo], className="ReportMain", id="Report2"),
                       Botones])

#Cambio en Gráficos
@callback(
    Output('GraphVariablesid','figure'),

    Input('DropIndicadores','value')


)
def update_output(DropIndicadores):
    Df_Variables=pd.read_csv("./Iden.csv")
    MinDate=Df_Variables['time'].iloc[0]
    MaxDate=Df_Variables['time'].iloc[-1]
    #print(MinDate, MaxDate)
    Df_Variables=Df_Variables.dropna()
    Df_Variables['DeltaE']=Df_Variables['Er']-Df_Variables['Eb']
    Df_Variables['IB100']=(Df_Variables['Eb']/Df_Variables['Er']) * 100
    Df_Variables['GEI']=Df_Variables['DeltaE']*0.126

    Data=pd.read_csv('./DataGuardian.csv')
    Data=Data[['time','AGUA','CRUDO']].dropna()
    
    IndiceList=[]
    for i in range(len(Data)):
    
        VolumenLiquido = Data.iloc[i,Data.columns.get_loc('AGUA')] + Data.iloc[i,Data.columns.get_loc('CRUDO')]
        IndiceConsumo= Df_Variables.iloc[i,Df_Variables.columns.get_loc('Er')] / VolumenLiquido
        IndiceList.append(IndiceConsumo)


    Df_Variables['IndiceConsumo']=IndiceList
    #print(Df_Variables["IndiceConsumo"])
    Df_Variables["D.Energetico"]=Df_Variables["DeltaE"]
    Df_Variables["D.Ambiental"]=Df_Variables["DeltaE"]*0.126  #Agregar Factor de Emision al JSON
    Df_Variables["D.Economico"]= Df_Variables["DeltaE"]*350 #Agregar al JSON
    dic={
        "IndiceConsumo":["Indice de Consumo Diario","IC [kWhd/BBL]"] ,
        "IB100": ["Cumplimiento Diario-Indicador Base 100[%]","[%]"],
        "GEI": ["Diferencial de Emisiones Gases Efecto Invernadero","GEI [Kg CO2eq/dia]"],
        "D.Energetico":["Desempeño Energético Diario","[kWhd]"],
        "D.Ambiental":["Desempeño Ambiental Diario","[Kg CO2eq / día]"],
        "D.Economico":["Desempeño Económico Diario","[ $ COP / día]"],

    }
    
    """    
    dataDF=Df_Variables.to_json(orient ='index')
    str_json = json.loads(dataDF)
    
    with open ("dataDF.json", "w") as file:
        json.dump(str_json,file,indent=4)
    """
    
    ColorLista1=[]
    for i in range(len(Df_Variables)):
        if Df_Variables["IB100"].iloc[i]>100:
            ColorLista1.append("#92bc5b")
        else:
            ColorLista1.append("#ff0040")
    
    ColorLista2=[]
    for i in range(len(Df_Variables)):
        if Df_Variables["DeltaE"].iloc[i]>0:
            ColorLista2.append("#ff0040")
        else:
            ColorLista2.append("#92bc5b")

        
    GraficoIndicadores=go.Figure()

    GraficoIndicadores.update_layout(
                    paper_bgcolor="rgb(248, 251, 254)",
                    plot_bgcolor='#e5ecf6', 
                    margin=dict(t=15, b=0, l=0, r=0),
                    width=800,
                    height=450,
                    font_size=10,
                    yaxis_title="<b>"+dic[str(DropIndicadores)][1]+"</b>",
                    title={
                    'text': "<b>"+dic[str(DropIndicadores)][0]+"</b>",
                    'y':1,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    yaxis_range=[0.8*Df_Variables[str(DropIndicadores)].min(),1.15*Df_Variables[str(DropIndicadores)].max()],
                    #legend=dict(yanchor="top",y=0.99,xanchor='right',x=0.99)
                    )
    
    if str(DropIndicadores)=="IndiceConsumo":

        GraficoIndicadores.add_trace(go.Bar(x=Df_Variables['time'],
                                            y=Df_Variables[str(DropIndicadores)].dropna(),
                                            showlegend=True,
                                            name= "<b>"+ "Ind Consumo Min: " +  str(round(Df_Variables['IndiceConsumo'].min(),3) ) +"</b>" 
                                            ))
    
        GraficoIndicadores.update_traces(marker_color='#92bc5b',marker_line_color='#38563d')
        GraficoIndicadores.add_shape(type='line',line_dash="dash",
                                    x0=MinDate,
                                    y0=Df_Variables['IndiceConsumo'].mean(),
                                    x1=MaxDate,
                                    y1=Df_Variables['IndiceConsumo'].mean(),
                                    line=dict(color='orange',),
                                    xref='x',
                                    yref='y')
        
        GraficoIndicadores.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='#92bc5b',symbol="square"),
                       legendgroup="Indice Max",
                       showlegend=True,
                       name="<b>"+ "Ind Consumo Max: " +  str(round(Df_Variables['IndiceConsumo'].max(),3) ) +"</b>"))
        
        GraficoIndicadores.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='orange',symbol="square"),
                       legendgroup="Indice Promedio",
                       showlegend=True,
                       name="<b>"+ "Ind Consumo Promedio: " +  str(round(Df_Variables['IndiceConsumo'].mean(),3) ) +"</b>"))
    
    
    elif str(DropIndicadores)=="IB100":

        GraficoIndicadores.add_trace(go.Bar(x=Df_Variables['time'],
                                            y=Df_Variables[str(DropIndicadores)].dropna(),
                                            name="<b>"+ "IB100 Min: " +  str(round(Df_Variables['IB100'].min(),3) ) +"</b>",
                                            showlegend=True))
        
        GraficoIndicadores.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='orange',symbol="square"),
                       legendgroup="IBM100 Max",
                       showlegend=True,
                       name="<b>"+ "IB100 Max: " +  str(round(Df_Variables['IB100'].max(),3) ) +"</b>"))
        
        GraficoIndicadores.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='orange',symbol="square"),
                       legendgroup="IBM100 Promedio",
                       showlegend=True,
                       name="<b>"+ "IB100 Promedio: " +  str(round(Df_Variables['IB100'].mean(),3) ) +"</b>"))

        GraficoIndicadores.update_traces(marker_color=ColorLista1,marker_line_color='#7b1623')

        GraficoIndicadores.add_shape(type='line',
                line_dash="dash",
                x0=MinDate,
                y0=100,
                x1=MaxDate,
                y1=100,
                line=dict(color='Red',),
                xref='x',
                yref='y')
        
        GraficoIndicadores.update_layout(yaxis_range=[0.9*Df_Variables['IB100'].min(),115])
    
    else:
        GraficoIndicadores.add_trace(go.Bar(x=Df_Variables['time'],
                                            y=Df_Variables[str(DropIndicadores)].dropna(),
                                            showlegend=True,
                                            name="<b>"+ str(DropIndicadores) + "  Min: " +  str(round(Df_Variables[str(DropIndicadores)].min(),3) ) +"</b>"))

        GraficoIndicadores.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='orange',symbol="square"),
                       legendgroup="Max",
                       showlegend=True,
                       name="<b>"+ str(DropIndicadores) +" Max: " +  str(round(Df_Variables[str(DropIndicadores)].max(),3) ) +"</b>"))

        GraficoIndicadores.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='orange',symbol="square"),
                       legendgroup="Promedio",
                       showlegend=True,
                       name="<b> "+ str(DropIndicadores) +" Promedio " +  str(round(Df_Variables[str(DropIndicadores)].mean(),3) ) +"</b>"))
        
        '''FechaMin=Df_Variables[Df_Variables['time']==Df_Variables[str(DropIndicadores)].min()]
        GraficoIndicadores.add_annotation(x=FechaMin,y=Df_Variables[str(DropIndicadores)].iloc[1],text="Valor Minimo")'''


        GraficoIndicadores.update_traces(marker_color=ColorLista2,marker_line_color='#38563d')

        #GraficoIndicadores.update_yaxes(autorange=True)

        GraficoIndicadores.update_layout(yaxis_range=[0.7*Df_Variables[str(DropIndicadores)].min(),1.1*Df_Variables[str(DropIndicadores)].max()])
    
    return GraficoIndicadores                          

#Actualización de Variables
@callback(
    Output('GraficoTorta2','figure'),

    #Encabezado 1
    Output('nombre_pozo2', 'children'),
    Output('nombre_gerencia2', 'children'),

    
    
    #Operatividad
    Output('fechaIni2', 'children'),
    Output('fechaFin2', 'children'),
    Output('EnergiaValue', 'children'),
    Output('AguaAcum1', 'children'),
    Output('CrudoAcum1', 'children'),
    Output('GasAcum1', 'children'),
    Output('LiqAcum1', 'children'),
    Output('DEnergeticoValue','children'),
    Output('DAmbientalValue','children'),
    Output('DEconomicoValue','children'),
    Output('GraficoDEA','figure'),
    Output('GraficoCumplimiento','figure'),
    
    #Nominales
    Output('TablaVFD2', 'figure'),
    Output('TablaSUT2', 'figure'),
    Output('TablaCABLE2', 'figure'),
    Output('TablaMOTOR2', 'figure'),
    Output('TablaBOMBA2', 'figure'),
    Output('SankeyGraphicPOAC','figure'),
    Output('SankeyGraphicPerdidas','figure'),

    Input('fechaIni2', 'children')

)
def actualizar_vars(var):
    

    Data=pd.read_csv('./DataGuardian.csv')
    Data['ProAcumulada']=Data["VOLUMEN_LIQUIDO"].dropna()

    Data2=pd.read_csv('./Iden.csv')

    EneAcum1="{:,.2f} kWh".format(Data2["Er"].sum())
    AguaAcum1="{:,.2f} BFPD".format(Data["AGUA"].sum())
    CrudoAcum1="{:,.2f} BFPD".format(Data["CRUDO"].sum())
    GasAcum1="{:,.2f} KPCPD".format(Data["GAS"].sum())
    LiqAcum1="{:,.2f} BFPD".format(Data["AGUA"].sum()+Data["CRUDO"].sum())

    Data2['DeltaE']=Data2['Er']-Data2['Eb']
    Data2['IB100']=Data2['Eb']/Data2['Er']
    Data2["D.Energetico"]=Data2["DeltaE"]
    Data2["D.Ambiental"]=Data2["DeltaE"]*0.126  #Agregar Factor de Emision al JSON
    Data2["D.Economico"]= Data2["DeltaE"] * 350 #Agregar al JSON
    

    
    DEnergetico=" {:,.2f} kWh".format(Data2["D.Energetico"].sum())
    DAmbiental=" {:,.2f}  Kg CO2eq".format(Data2["D.Ambiental"].sum()) 
    DEconomico= "$ {:,.2f} COP".format(Data2["D.Economico"].sum())

    
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
        marker=dict(colors=["#00821a", "#FF003D"])
        )
    
    #Grafico Desempeño energetico
   
    ColorLista=[]
    
    DataCusum=Data2["CUSUM"].dropna()
    for i in range(len(DataCusum)):
        print(i)
        if i==0:
            if DataCusum.iloc[i]<DataCusum.iloc[i+1]:
                ColorLista.append('red')

            else:
                ColorLista.append('green')

        
        elif i>0:
            if DataCusum.iloc[i]>DataCusum.iloc[i-1]:
                ColorLista.append("red")
            
            else:
                ColorLista.append("green")
       

    print(len(ColorLista))
    print(ColorLista)

    #Grafico de Cumplimiento
    GraficoDEA=go.Figure()
    GraficoDEA.add_trace(go.Line(x=Data2["time"],
                                 y=Data2["CUSUM"].dropna(),
                                 line = dict(dash="dot", color="grey"),
                                 marker=dict(color=ColorLista,
                                 size=5, symbol="square"),
                                 type="scatter",showlegend=False, mode="lines+markers",
                                 #fill='tonext',
                                 #fillcolor="rgb(248, 251, 254)"
                                ))
    
                        
    
                            
    GraficoDEA.add_trace(go.Line(x=Data2['time'],y=Data2["CUSUM"]+1000000,
                                line = dict(dash="dot", color="gray"),
                                name="CUSUM",
                                type="scatter",
                                fill='tonexty',
                                fillcolor="#e4e4e4",
                                mode='lines'))
    
    GraficoDEA.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='green',symbol="square"),
                       legendgroup='Día de ahorro', showlegend=True, name='Día de ahorro'))

    GraficoDEA.add_trace(go.Scatter(x=[None], y=[None], mode='markers',
                       marker=dict(size=10, color='red',symbol="square"),
                       legendgroup='Día de Sobreconsumo', showlegend=True, name='Día de Sobreconsumo'))
    
    GraficoDEA.update_layout(
            
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=0, r=0),
            plot_bgcolor='rgba(255, 255,255,0.6)',
            yaxis_title="Desviación del consumo de Energia [ kWh ]",
            yaxis_range=[Data2["CUSUM"].min(),Data2["CUSUM"].max()],
            xaxis_range=[Data2["time"].min(),Data2["time"].max()],
            width=700,
            height=500,
           
            )

    
    #----------GRAFICO DE CUMPLIMIENTO ----------


    figCumplimiento=go.Figure(go.Indicator(
    mode = "gauge+number",
    value = Data2['IB100'].mean()*100,
    domain = {'x': [0, 1], 'y': [0, 1]},
    
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
            'thickness': 0.6,
            'value':Data2['IB100'].mean()*100 }},
    
    number={'suffix':"%"}
    
    ))
    
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


    #Figura de Sankey Potencias Activas
    
    DataSankey=pd.read_csv('.\DataGuardian.csv')
    
   
    PerdidasCable=DataSankey['PERDIDAS_CAB'].mean()
    PerdidasVFD=DataSankey['POACTPQM1T_kW'].mean()-DataSankey['POACTPQM2_kW'].mean()
    PerdidasSUT=DataSankey['POACTPQM2_kW'].mean()-DataSankey['POACTPQM3_kW'].mean()
    PerdidasMB=DataSankey['POTENCIAMOTOR'].mean()-DataSankey['POT_HID'].mean()
    PerdidasTotales=PerdidasVFD+PerdidasMB+PerdidasSUT+ PerdidasCable
    
    

    POACM1=DataSankey['POACTPQM1T_kW'].mean()
    PotenciaMotor=POACM1-PerdidasTotales
    


    figSankeyPOAC = go.Figure(data=[go.Sankey(
                        valuesuffix = "kWh",
                        node = dict(
                        pad = 15,
                        thickness = 20,
                        line = dict(width = 0.5),
                        label = ['Potencia Entrada al sistema, {:,.2f} kWh '.format(POACM1),
                                'Potencia Motor, {:,.2f} kWh'.format(PotenciaMotor),
                                'Perdidas SUT, {:,.2f} kWh'.format(PerdidasSUT),
                                'Perdidas VFD, {:,.2f}  kWh'.format(PerdidasVFD),
                                'Perdidas Cable, {:,.2f} kWh'.format(PerdidasCable),
                                ],
                        
                
                        ),
                        link = dict(
                        source = [0, 0, 0, 0], 
                        target = [1, 2, 3, 4],
                        
                        value = [ PotenciaMotor, PerdidasSUT , PerdidasVFD, PerdidasCable],
                        
                        ))])

    figSankeyPOAC.update_layout(title={'text': "Potencia Entrada al Sistema [kWh]",
                                            'y':0.85, # new
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top' # new

                                        },
                                paper_bgcolor="rgb(248, 251, 254)",
                                width=650,
                                height=450,

                                font_size=12)

    

    # Figura de Sankey Perdidas

    
   
    
   
    
    figSankeyPerdidas = go.Figure(data=[go.Sankey(
                        valuesuffix = " kWh",
                        node = dict(
                        pad = 15,
                        thickness = 20,
                        line = dict(color = "black", width = 0.5),
                        label = ['Perdidas Totales, {:,.2f} kWh'.format(PerdidasTotales),
                                'Perdidas SUT, {:,.2f} kWh'.format(PerdidasSUT),
                                'Perdidas VFD, {:,.2f}  kWh'.format(PerdidasVFD) ,
                                'Perdidas Motor Bomba, {:,.2f} kWh'.format(PerdidasMB),
                                'Perdidas Cable, {:,.2f} kWh'.format(PerdidasCable) ],
                        color=['#808b96','#f7dc6f', '#00ccb4', '#EC7063', '#85bd60']
                        ),
                        link = dict(
                        source = [ 0, 0, 0, 0,0], # indices correspond to labels, eg A1, A2, A1, B1, ...
                        target = [1, 1,2,3,4],
                        value = [0, PerdidasSUT ,PerdidasVFD, PerdidasMB, PerdidasCable ],
                        color=['#EC7063', '#FEF3C7', '#a6e3d7', '#EBBAB5','#85bd60']
                        ))])

    figSankeyPerdidas.update_layout(title={'text': "Perdidas de Energia [kWh]",
                                            'y':0.85, # new
                                            'x':0.5,
                                            'xanchor': 'center',
                                            'yanchor': 'top',
                                                    # new

                                            },
                                    paper_bgcolor="rgb(248, 251, 254)",
                                    width=650,
                                    height=450,
                                    font_size=12)
    
    

    


    


    
    return[figTorta, nombre_pozo, nombre_gerencia, FECHAINI, FECHAFIN,EneAcum1,AguaAcum1,CrudoAcum1,GasAcum1,LiqAcum1,DEnergetico,DAmbiental,DEconomico,GraficoDEA, figCumplimiento, 
           
           figVFD, figSUT, figCABLE, figMOTOR, figBOMBA,figSankeyPOAC,figSankeyPerdidas]


#Gráficos MultiSelect Doble Eje
@callback(
    
    Output('GraficoMulti2', 'figure'),
    Output('DropMulti2','disabled'),
    Output('resetMulti2','n_clicks'),
    
    
    Input('DropMulti2','value'),
    Input('resetMulti2','n_clicks')
    
    
)
def graficoMultiSelect(DropMultiValue, ClickReset):
    
    Data=pd.read_csv("./DataGuardian.csv")
    Data2=pd.read_csv("./Iden.csv")
    
    Df_Variables=pd.read_csv("./Iden.csv")
    Df_Variables=Df_Variables.dropna()
    Df_Variables['DeltaE']=Df_Variables['Er']-Df_Variables['Eb']
    Df_Variables['IB100']=(Df_Variables['Eb']/Df_Variables['Er']) * 100
    Df_Variables['GEI']=Df_Variables['DeltaE']*0.126

    #Data=pd.read_csv('./DataGuardian.csv')
    DataL=Data[['time','AGUA','CRUDO']].dropna()
    
    IndiceList=[]
    for i in range(len(DataL)):
    
        VolumenLiquido = DataL['AGUA'].iloc[i] + DataL['CRUDO'].iloc[i]
        IndiceConsumo= Df_Variables['Er'].iloc[i] / VolumenLiquido
        IndiceList.append(IndiceConsumo)


    Df_Variables['IndiceConsumo']=IndiceList
    #print(Df_Variables["IndiceConsumo"])
    Df_Variables["D.Energetico"]=Df_Variables["DeltaE"]
    Df_Variables["D.Ambiental"]=Df_Variables["DeltaE"]*0.126  #Agregar Factor de Emision al JSON
    Df_Variables["D.Economico"]= Df_Variables["DeltaE"]*350 #Agregar al JSON
  
    GraficoMulti=go.Figure()
    GraficoMulti.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=-0, r=0),
            width=1300,
            height=450,
            font_size=10
            )
    
    titles=[]
    disabled=False
    clicks=0
    
    lenDrop=len(DropMultiValue)
    
    
    if lenDrop==1:
        titles=[DropMultiValue[0],"--","--","--"] 
    elif lenDrop==2:
        titles=[DropMultiValue[0],DropMultiValue[1],"--","--"]
    elif lenDrop==3:
        titles=[DropMultiValue[0],DropMultiValue[1],DropMultiValue[2],"--"]
    elif lenDrop>=4:
        titles=[DropMultiValue[0],DropMultiValue[1],DropMultiValue[2], DropMultiValue[3]]
        disabled=True
        
    if ClickReset>=1:
        disabled=False
        clicks=0
            
    colors=["#1f77b4", "#ff7f0e", "green", "#9467bd"]
    
    if lenDrop!=0:
    
        GraficoMulti.update_layout(
            xaxis=dict(
                domain=[0.3, 0.7]
            ),
            yaxis=dict(
                title=titles[0],
                titlefont=dict(
                    color=colors[0]
                ),
                tickfont=dict(
                    color=colors[0]
                )
            ),
            yaxis2=dict(
                title=titles[1],
                titlefont=dict(
                    color=colors[1]
                ),
                tickfont=dict(
                    color=colors[1]
                ),
                anchor="x",
                overlaying="y",
                side="right",
                
            ),
            yaxis3=dict(
                title=titles[2],
                titlefont=dict(
                    color=colors[2]
                ),
                tickfont=dict(
                    color=colors[2]
                ),
                anchor="free",
                overlaying="y",
                side="left",
                position=0.23
            ),
            yaxis4=dict(
                title=titles[3],
                titlefont=dict(
                    color=colors[3]
                ),
                tickfont=dict(
                    color=colors[3]
                ),
                anchor="free",
                overlaying="y",
                side="right",
                position=0.76
            )
        )

    else:
        
            GraficoMulti.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=-0, r=0),
            width=550,
            height=450,
            font_size=10
            )


    if DropMultiValue!=None:
        ax=1
        if lenDrop<len(DropMultiValue)+1:
            for Signal in DropMultiValue:
                    
                    if Signal not in ['DeltaE', 'IB100', 'GEI', 'IndiceConsumo', 'D.Energetico', 'D.Ambiental', 'D.Economico']:
                        
                        D=Data[Data[Signal]>0]
                        
                        GraficoMulti.add_trace(
                            go.Scatter(
                                
                            x=D["time"],
                            y=D[Signal],
                            name=Signal,
                            yaxis=f"y{ax}",
                            line_color=colors[ax-1],
                            
                        ))
                        
                    else:
                        
                        
                        GraficoMulti.add_trace(
                            go.Scatter(
                                
                            x=Df_Variables["time"],
                            y=Df_Variables[Signal],
                            name=Signal,
                            yaxis=f"y{ax}",
                            line_color=colors[ax-1],
                            
                        ))
                        
                        
                        
                    
                    ax=ax+1

        
    return [GraficoMulti, disabled, clicks]



dash.clientside_callback( 
    """
    
        function(n_clicks){
        if(n_clicks > 0){
            
            let Hoy = new Date();
            let HoyS = Hoy.toLocaleDateString();
            document.querySelector("#Marca2").innerHTML = "[v.0.1] Reporte Generado por E2 Energía Eficiente el "+HoyS.toString();
            
            html2canvas(document.querySelector("#Report2")).then(canvas => {
            
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
    
            doc.save('Reporte de Desempeño Energético.pdf');
            
})}}
    
    """
    ,
    Output('btn-Descargar2','n_clicks'),
    Input('btn-Descargar2','n_clicks')
)