#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Own scripts / modules
from scripts.load_data import load_class_data, load_data_wrs, load_world_lon_lat_data 
from scripts.lottie import get_icons
import scripts.callbacks_graphs as cg
from scripts.make_intro_cards import row_with_cards_in_columns
import scripts.load_data as ld
import scripts.metrics_in_theme as mit
import scripts.make_graphs as mg
import scripts.theme_intro_texts as tit

# Dashboard
import dash                                     # pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
from dash.dependencies import Input, Output

from flask_caching import Cache


from sklearn.preprocessing import MinMaxScaler

import plotly.graph_objects as go
import math
from dash_extensions import Lottie       # pip install dash-extensions

from plotly.subplots import make_subplots

import plotly.express as px
import plotly.figure_factory as ff

#Viz
import seaborn as sns
import matplotlib.pyplot as plt

#IMG
import base64

from urllib.request import urlopen
import json

import numpy as np
import pandas as pd



# -------------------------- DASH ---------------------------- #

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

#cache = Cache(app.server, config={
#    # try 'filesystem' if you don't want to setup redis
#    'CACHE_TYPE': 'redis',
#    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
#})

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

app.config.suppress_callback_exceptions = True

timeout = 60

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

timeout = 60


@cache.memoize(timeout=timeout)
def load_data_wrs(data_file=None):
        '''0.0.1  Create a function to load the dataset which was extracted from the Data Warehouse'''
        return pd.read_csv(data_file)
@cache.memoize(timeout=timeout)
def load_class_data(data_file=None):
        '''0.0.1  Create a function to load the income group for each country'''
        dfObj = pd.read_csv(data_file)
        dfObj.rename(columns = {'CountryName':'Country'}, inplace = True)
        return dfObj
@cache.memoize(timeout=timeout)
def load_world_lon_lat_data():
        '''0.0.1  Create a function to load longitude and latitude coordinates for each country'''
        url = 'https://gist.githubusercontent.com/erdem/8c7d26765831d0f9a8c62f02782ae00d/raw/248037cd701af0a4957cce340dabb0fd04e38f4c/countries.json'
        d = pd.read_json(url)
        d = d[['latlng', 'name']]
        d.rename(columns = {'name':'Country'}, inplace = True)
        return d
@cache.memoize(timeout=timeout)
def countrys_latest_MetricData(dfObj=None, country='France', metric='Road Network Density'):
    dfObj = dfObj[ (dfObj['Country'] == country) & (dfObj['Metric'] == metric) ]
    latest_year = np.max(dfObj["Year"])
    dfObj = dfObj[dfObj["Year"].isin([latest_year])].reset_index(drop=True)
    metric = dfObj['Metric'][0]
    value = np.around(dfObj['Value'][0], decimals=2, out=None)
    unit = dfObj['Unit'][0]
    return metric, latest_year, value, unit

# IMG 
image_filename = 'irfcountrydashboard/data/img/sns_facet.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename_2 = './irfcountrydashboard/data/img/sns_facet.png'  # replace with your own image
encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())



# -------------------------- DATA LOADING FUNCTIONS ---------------------------- #
#df_class = ld.load_class_data(data_file='irfcountrydashboard/data/CLASS.csv')
#df_lon_lat = ld.load_world_lon_lat_data()        
#df_wrs = ld.load_data_wrs(data_file='irfcountrydashboard/data/WRS Data 2014-2019 UTF-8 encoded.csv')
#df = df_wrs.merge(df_lon_lat, how='left', on='Country').merge(df_class, how='left', on='Country')

df_class = load_class_data(data_file='irfcountrydashboard/data/CLASS.csv')
df_lon_lat = load_world_lon_lat_data()        
df_wrs = load_data_wrs(data_file='irfcountrydashboard/data/WRS Data 2014-2019 UTF-8 encoded.csv')
df = df_wrs.merge(df_lon_lat, how='left', on='Country').merge(df_class, how='left', on='Country')

# -------------------------- LOTTIE GIFs LOADING FUNCTIONS ---------------------------- #
url_coonections, url_companies, url_msg_in, url_msg_out, url_reactions, options = get_icons()


# -------------------------- LOAD CARDS ---------------------------- #
card_1, card_2, card_3, card_4 = row_with_cards_in_columns(options=options)

# -------------------------- LOAD MAPS ---------------------------- #
geojson = px.data.election_geojson()
candidates = ['Road Network Density', 'Persons Killed Rate', 'Total Vehicles In Use Rate by Population', 'Motorway Highway Ratio']


# -------------------------- PROJECT DASHBOARD ---------------------------- #
colors = {
    'background': '#eaebeb',
    'text': '#7FDBFF'
}

app.layout = dbc.Container([
        
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([   
        dbc.Col(html.Div([html.H1(dcc.Markdown('''__IRF__'''), className="display-3", style={'textAlign': 'center', 'padding': '15px 15px 5px', 'font-family': 'Segoe UI'}),
                          html.Hr(className="my-2"),
                          html.P(dcc.Markdown('''__PRESENTS__'''), className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'}),
                          html.P(dcc.Markdown('''INTERACTIVE **__COUNTRY EXPLORER__**'''), className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'})]), width=12)
    ], className='mb-4 mt-4'),
    
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    
    dbc.Row([
        dbc.Col([], width=2),        
        dbc.Col([], width=2),
        dbc.Col([            
            html.H2("", style={'textAlign':'center'}),
            dcc.Dropdown(id='my-country-searchbox', multi=False, value='Turkey', options=[{'label': x, 'value':x} for x in sorted(df["Country"].unique())]),
        ], width=4),
        dbc.Col([], width=2),
        dbc.Col([], width=2),
    ], className='mb-4 mt-4'),
    
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    
    html.Div(className='row', style = {'display' : 'flex'},
        children=[
            dbc.Col([], width=2),
            dbc.Col(html.Div([
                        html.P(dcc.Markdown('''__**KPI**__ in 2019.'''), className="display-3", style={'textAlign': 'center', 'padding': '15px 15px 5px', 'font-family': 'Segoe UI'}),
                        html.Hr(className="my-2"),
                        #html.P(f"Let's start with an overview of the length of the road network of Turkey, and compare it with the all the upper middle income countries.", className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'}),
            ]), width=8),
            dbc.Col([], width=2),  
        ]
    ),
    

    html.Div(className='row', style = {'display' : 'flex'},
             children=[
                html.Div([
                    dbc.Row([], className='mb-3 mt-3'),
                    card_1,
                    dbc.Row([], className='mb-4 mt-4'),
                    card_2, 
                ], style={'width': '10%', 'display': 'inline-block',}),
                html.Div([
                    dbc.Row([], className='mb-3 mt-3'),
                    card_3,
                    dbc.Row([], className='mb-4 mt-4'),
                    card_4, 
                ], style={'width': '10%', 'display': 'inline-block',}),
                html.Div([
                    dcc.RadioItems(id = 'candidate', options=[{'value': x, 'label': x} for x in candidates], value = candidates[0], labelStyle={'display': 'inline-block'}, inputStyle={"margin-left": "20px"}),
                    dcc.Graph(id="bubble_worldmap_graph", config={'displayModeBar': False})], style={'width': '70%', 'display': 'inline-block',})
            ]
    ),
    
   
    
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
# ----- Road Network
    html.Div(className='row', style = {'display' : 'flex'},
            children=[
                dbc.Col([], width=2),
                dbc.Col(html.Div([
                            html.P(dcc.Markdown('''__**Road Network**__ development.'''), className="display-3", style={'textAlign': 'center', 'padding': '15px 15px 5px', 'font-family': 'Segoe UI'}),
                            html.Hr(className="my-2"),
                            html.P(f"Let's start with an overview of the length of the road network, and compare it with the country's income group mean value.", className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'}),
                ]), width=8),
                dbc.Col([], width=2),
                
                dbc.Row([
                    dbc.Col([], width=3),
                    dbc.Col([
                        html.Div([dbc.Col([dcc.Graph(id="paved_network_ratio", config={'displayModeBar': False})], width=6)], style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'}),    
                    ], width=6),
                    dbc.Col(id='text-road-network', className="lead", style={'textAlign': 'left', 'font-family': 'Segoe UI'}, width=3)                        
                ], className='mb-4'),    
            ]
    ),
    
    
    html.Div(className='row', style = {'display' : 'flex'},
            children=[
                dbc.Col([], width=2),
                dbc.Col(html.Div([html.P(f"From here, we want to get more insights in the 2019 data. How does the distribution of the road network differ among income groups, and where does Turkey stand in comparison?", className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'})]), width=8),
                dbc.Col([], width=2),
                dbc.Row([
                    dbc.Col([], width=3),
                    dbc.Col([html.Div([
                        #dbc.Col([dcc.Graph(id="paved_network_ratio_comparison", config={'displayModeBar': False})], width=6),
                        dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_image_2.decode()), width=584/2, height= 584/2)], width=6)
                        ], style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'}),    
                    ], width=6),
                    dbc.Col([], width=3)                        
                ], className='mb-4'),
                ]
    ), 
        
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    
#-----Road Accidents
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),

    html.Div(className='row', style = {'display' : 'flex', 'backgroundColor': ''},
            children=[
                dbc.Col([], style={'backgroundColor': ''}, width=2),
                dbc.Col(html.Div([
                    html.P(dcc.Markdown('''__**Road Accidents**__ development.'''), className="display-3", style={'textAlign': 'center', 'padding': '15px 15px 5px', 'font-family': 'Segoe UI', 'backgroundColor': ''}),
                    html.Hr(className="my-2"),
                    html.P(f"Let's start with an overview of road accidents, and compare it with the country's income group mean value.", className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI', 'backgroundColor': ''}),
                    ]), width=8
                ),
                dbc.Col([], style={'backgroundColor': ''}, width=2),
                dbc.Row([
                    #html.Div(id="paved_network_ratio-text", style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'}),
                    dbc.Col([], width=3),
                    dbc.Col([html.Div([dbc.Col([dcc.Graph(id="total_persons_killed_ratio", config={'displayModeBar': False})], width=6)], style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'})], width=6),
                    dbc.Col(id='text-total_persons_killed_ratio', className="lead", style={'textAlign': 'left', 'font-family': 'Segoe UI', 'backgroundColor': ''}, width=3)                                      
                ], className='mb-4'),    
            ]
    ),
    
    html.Div(className='row', style = {'display' : 'flex', 'backgroundColor': ''},
            children=[
                dbc.Col([], width=2),
                dbc.Col(html.Div([html.P(f"From here, we want to get more insights in the 2019 data. How does the distribution of the road network differ among income groups, and where does Turkey stand in comparison?", className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'})]), width=8),
                dbc.Col([], width=2),
                dbc.Row([
                    dbc.Col([], width=3),
                    dbc.Col([html.Div([
                        #dbc.Col([dcc.Graph(id="paved_network_ratio_comparison", config={'displayModeBar': False})], width=6),
                        dbc.Col([html.Img(src='data:image/png;base64,{}'.format(encoded_image_2.decode()), width=584/2, height= 584/2)], width=6)
                        ], style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'}),    
                    ], width=6),
                    dbc.Col([], width=3)                        
                ], className='mb-4'),
            ]
    ),   
          
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    
    html.Div(className='row', style = {'display' : 'flex', 'backgroundColor': ''},
            children=[
                dbc.Col([], width=2),
                dbc.Col(html.Div([
                    html.P(f"Up to now, we only had a look at total numbers of deaths per year. But how did the individual numbers for female and male killed persons evolve over time?", className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'}),
                    ]), width=8
                ),
                dbc.Col([], width=2),
                dbc.Row([
                    #html.Div(id="paved_network_ratio-text", style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'}),
                    dbc.Col([], width=3),
                    dbc.Col([html.Div([dbc.Col([dcc.Graph(id="distribution_comparison", config={'displayModeBar': False})], width=6)], style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'})], width=6),
                    dbc.Col([], width=3)                        
                ], className='mb-4'),    
            ]
    ),
    
    # Next theme general
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    dbc.Row([], className='mb-4 mt-4'),
    
    html.Div(className='row', style = {'display' : 'flex'},
            children=[
                dbc.Col([], width=2),
                dbc.Col(html.Div([
                            html.P(dcc.Markdown('''__**What influences**__ the amount of killed people?'''), className="display-3", style={'textAlign': 'center', 'padding': '15px 15px 5px', 'font-family': 'Segoe UI'}),
                            html.Hr(className="my-2"),
                            html.P(f"Let's start with the impact of two features on the persons killed rate, namely expenditure on the road infrastructure, and the amount of vehicles.", className="lead", style={'textAlign': 'center', 'font-family': 'Segoe UI'}),
                        ]), width=8),
                dbc.Col([], width=2),
                dbc.Row([
                    #html.Div(id="paved_network_ratio-text", style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'}),
                    dbc.Col([], width=3),
                    dbc.Col([html.Div([dbc.Col([dcc.Graph(id="bubble_persons_killed", config={'displayModeBar': False})], width=6)], style={'width': '50%', 'display': 'inline-block', 'backgroundColor': '#ffffff'})], width=6),
                    dbc.Col(id='text-bubble_persons_killed', className="lead", style={'textAlign': 'left', 'font-family': 'Segoe UI'}, width=3)                                 
                ], className='mb-4')
                ]
    ),
    
], fluid=True)
    
  

# GEO-JSON
candidates = ['Road Network Density', 'Persons Killed Rate', 'Total Vehicles In Use Rate by Population', 'Motorway Highway Ratio']

def load_geojson():
    with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as response:
        countries = json.load(response)
    return countries
geojson = load_geojson()

# CALLBACKS
@app.callback(
    [Output(component_id= "paved_network_ratio", component_property=  "figure"),
     Output(component_id= 'text-road-network', component_property= 'children')],
    [Input('my-country-searchbox','value')]
)
@cache.memoize(timeout=timeout)  # in seconds
def display_paved_network_ratio(country_slctd):
    
    fig, text = cg.display_country_incomegroup_graph(df=df, theme='Land Area', country=country_slctd, metric='Total Road Network', df_class=df_class, norm_metric='Land Area')
  
    return fig, text


@app.callback(
    Output("paved_network_ratio_comparison", "figure"),
    [Input('my-country-searchbox','value')]
)
@cache.memoize(timeout=timeout)  # in seconds
def display_paved_network_ratio_comparison(country_slctd):

    pass
 
# INTRO text
@app.callback(
    Output(component_id= 'paved_network_ratio-text', component_property= 'children'),
    Input(component_id = 'my-country-searchbox', component_property= 'value')
)
@cache.memoize(timeout=timeout)  # in seconds
def update_paved_network_ratio_text(country_slctd):
    
    text = tit.paved_network_ratio_text(country=None, val=None, mean_high_income=None)
    
    return text     
 
# theme road accidents 
@app.callback(
    [Output(component_id = "total_persons_killed_ratio", component_property = "figure"),
     Output(component_id= 'text-total_persons_killed_ratio', component_property= 'children')],
    [Input('my-country-searchbox','value')]
)
@cache.memoize(timeout=timeout)  # in seconds
def display_total_persons_killed_ratio(country_slctd):
    
    fig, text = cg.display_country_incomegroup_graph(df=df, theme='Road Accidents', country=country_slctd, metric='Total Persons Killed', df_class=df_class, norm_metric='Population')
    
    return fig, text


@app.callback(
    Output(component_id = "distribution_comparison", component_property = "figure"),
    [Input('my-country-searchbox','value')]
)
@cache.memoize(timeout=timeout)  # in seconds    
def display_distribution_comparison(country_slctd):
    
    fig, text = cg.display_distribution_comparison_graph(df=df, theme='Road Accidents', country=country_slctd, years=[2014,2015,2016,2017,2018,2019], metric='Persons Killed Rate')
        
    return fig       

# bubble_persons_killed
@app.callback(
    [Output(component_id = "bubble_persons_killed", component_property = "figure"),
     Output(component_id= 'text-bubble_persons_killed', component_property= 'children')], 
    [Input('my-country-searchbox','value')])
@cache.memoize(timeout=timeout)  # in seconds
def display_bubble_persons_killed_graph(country_slctd):
    
    fig, text = cg.display_bubble_persons_killed_graph(df=df, country=country_slctd, df_class=df_class)
    
    return fig, text





# maps top
@app.callback(
    Output(component_id = "bubble_worldmap_graph", component_property = "figure"), 
    [Input("candidate", "value")])
@cache.memoize(timeout=timeout)  # in seconds
def display_bubble_worldmap(candidate):
    
    fig, text = cg.display_bubble_worldmap_graph(df=df, metric=candidate, year=2019)
    
    return fig
    

 

# Updating 4 number cards
@app.callback(
    Output('content_road_network_density','children'),
    #Output('unit_road_network_density','children'),
    
    Output('content_persons_killed_rate','children'),
    #Output('unit_persons_killed_rate','children'),
    
    Output('content_total_vehicles_in_use_rate_by_population','children'),
    #Output('unit_total_vehicles_in_use_rate_by_population','children'),
    
    Output('content_motorway_highway_ratio','children'),
    #Output('unit_motorway_highway_ratio','children'),
    
    Input('my-country-searchbox','value'),
)
@cache.memoize(timeout=timeout)  # in seconds
def update_small_cards(country_slctd):
    # Road Network Density
    result = []
    for metric in ['Road Network Density', 'Persons Killed Rate', 'Total Vehicles In Use Rate by Population', 'Motorway Highway Ratio']:
        (metric, latest_year, value, unit) = ld.countrys_latest_MetricData(dfObj=df, country=country_slctd, metric=metric)
        result.append(value)

    return result





if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True, use_reloader=True)