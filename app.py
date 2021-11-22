#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8080/ in your web browser.

from irfcountrydashboard.load_data import load_class_data, load_data_wrs, load_world_lon_lat_data 
import dash                                     # pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

from dash_extensions import Lottie       # pip install dash-extensions
from scripts.lottie import get_icons


# -------------------------- DATA LOADING FUNCTIONS ---------------------------- #
df_class = load_class_data(data_file='irfcountrydashboard/data/CLASS.csv')
print(df_class.columns)

df_lon_lat = load_world_lon_lat_data()        

df_wrs = load_data_wrs(data_file='irfcountrydashboard/data/WRS Data 2000-2019.csv')

df = df_wrs.merge(df_lon_lat, how='left', on='Country').merge(df_class, how='left', on='Country')
print(df.sample(n=10))
print(df.columns)
# -------------------------- LOTTIE GIFs LOADING FUNCTIONS ---------------------------- #
url_coonections, url_companies, url_msg_in, url_msg_out, url_reactions, options = get_icons()

# -------------------------- DASH ---------------------------- #

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

app.config.suppress_callback_exceptions = True









# -------------------------- PROJECT DASHBOARD ---------------------------- #

app.layout = dbc.Container([
    dbc.Row([   
        dbc.Col(html.Div([html.H1("IRF Data Warehouse Country Explorer", className="display-3"),
                        html.P(
                            "The easy way to see a countries' development over time for several indicators, its comparison to different countries, or income groups, in an interactive App.",
                            className="lead",
                        ),
                        html.P("", className="font-italic"),
                ]), width=10),
    ], className='mb-4 mt-2'),
    
    dbc.Row([
        dbc.Col([], width=3),        
        dbc.Col([            
            html.H2("", style={'textAlign':'center'}),
            dcc.Dropdown(id='my-country-searchbox', multi=False, value='Turkey', options=[{'label': x, 'value':x} for x in sorted(df["Country"].unique())]),
        ], width=4),
        dbc.Col([], width=3),
    ], className='mb-3 mt-2'),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Road Network Density 2019'),
                    html.H2(id='content-connections', children="000"),
                    html.H6(id='content-connections_unit', children='unit')
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="70%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.H6('Persons Killed Rate 2019'),
                    html.H2(id='content-companies', children="000"),
                    html.H6(id='content-companies_unit', children='unit')
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="42%", height="15%", url=url_msg_in)),
                dbc.CardBody([
                    html.H6('Total Vehicles in Use Rate by Population 2019'),
                    html.H2(id='content-msg-in', children="000"),
                    html.H6(id='content-msg-in_unit', children='unit')
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="37%", height="40%", url=url_msg_out)),
                dbc.CardBody([
                    html.H6('Total Vehicles in Use Rate by Network 2019'),
                    html.H2(id='content-msg-out', children="000"),
                    html.H6(id='content-msg-out_unit', children='unit')
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="40%", height="40%", url=url_reactions)),
                dbc.CardBody([
                    html.H6('Motorway Highway Ratio 2019'),
                    html.H2(id='content-reactions', children="000"),
                    html.H6(id='content-reactions_unit', children='unit')
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
    ], className='mb-2 mt-2'),

], fluid=True)  









if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)