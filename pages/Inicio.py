import dash
from dash import html, dcc

dash.register_page(__name__, path='/', title="Reportes Guardian")

Links={
    "Inicio":{"relative_path":"http://127.0.0.1:8050"},
    "Desempeno":{"relative_path":"http://127.0.0.1:8050/desempeno"},
    "Predictivo":{"relative_path":"http://127.0.0.1:8050/predictivo"},
    "Carta":{"relative_path":"http://127.0.0.1:8050/carta"},
}

layout = html.Div([
	#html.H1('Reportes Piloto Guardian'),
 
    html.Div([html.Img(src="/assets/Desempeno_logo.png", className="LogoImg"), html.A("REPORTE DE DESEMPEÑO",   href=Links["Desempeno"]["relative_path"], target="_blank")], className="Link"),
    html.Div([html.Img(src="/assets/Predictivo_logo.png", className="LogoImg"), html.A("REPORTE PREDICTIVO",     href=Links["Predictivo"]["relative_path"], target="_blank")], className="Link"),
    html.Div([html.Img(src="/assets/Carta_logo.png", className="LogoImg"), html.A("CARTA AMPERIMÉTRICA",     href=Links["Carta"]["relative_path"], target="_blank")], className="Link"),

], className="MainLinks")

