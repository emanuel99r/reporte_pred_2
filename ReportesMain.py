from dash import Dash, html, dcc
import dash

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
page=dash.page_registry.values()
Links={}

for p in dash.page_registry.values():   
    Links[p["name"]]=p



app.layout = html.Div([
	#html.H1('Reportes Piloto Guardian'),

    html.Div([
        
        html.Div([html.Img(src="/assets/Inicio_logo.png", className="LogoImg"), dcc.Link("INICIO",                 href=Links["Inicio"]["relative_path"])],  className="LinkInicio"),
        html.Div([html.Img(src="/assets/Desempeno_logo.png", className="LogoImg"), dcc.Link("REPORTE DE DESEMPEÑO",   href=Links["Desempeno"]["relative_path"])], className="Link"),
        html.Div([html.Img(src="/assets/Predictivo_logo.png", className="LogoImg"), dcc.Link("REPORTE PREDICTIVO",     href=Links["Predictivo"]["relative_path"])], className="Link"),
        html.Div([html.Img(src="/assets/Carta_logo.png", className="LogoImg"), dcc.Link("CARTA AMPERIMÉTRICA",     href=Links["Carta"]["relative_path"])], className="Link"),
        
        ],className="Links"),

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)