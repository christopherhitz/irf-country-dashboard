#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8080/ in your web browser.

from irfcountrydashboard.load_data import load_class_data, load_data_wrs, load_world_lon_lat_data 
import dash                                     # pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

df_class = load_class_data(data_file='./data/CLASS.csv')
print(df_class.columns)

df_lon_lat = load_world_lon_lat_data()        

df_wrs = load_data_wrs(data_file='./data/WRS Data 2000-2019.csv')

df = df_wrs.merge(df_lon_lat, how='left', on='Country').merge(df_class, how='left', on='Country')
print(df.sample(n=10))
print(df.columns)

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
], fluid=True)  
