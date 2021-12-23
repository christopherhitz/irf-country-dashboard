#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import dash_html_components as html
from dash_extensions import Lottie       # pip install dash-extensions
from scripts.lottie import get_icons

# -------------------------- LOTTIE GIFs LOADING FUNCTIONS ---------------------------- #
url_coonections, url_companies, url_msg_in, url_msg_out, url_reactions, options = get_icons()

def row_with_cards_in_columns(options=None):
    '''This function creates four cards which will be displayed below the country searchbox.
    
    Outputs: -card_1: Road Network Density 2019
             -card_2: Persons Killed Rate 2019
             -card_3: Total Vehicles in Use Rate by Population 2019 
             -card_4: Total Vehicles in Use Rate by Network 2019
    '''
    card_1 = dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_coonections)),
                dbc.CardBody([
                    html.P('Road Network Density'),
                    html.H4(id='content_road_network_density', children="000"),
                    #html.P(id='unit_road_network_density', children='unit')
                ], style={'textAlign':'center'})
            ]) 
    
    card_2 = dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="70%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.P('Persons Killed Rate'),
                    html.H4(id='content_persons_killed_rate', children="100"),
                    #html.P(id='unit_persons_killed_rate', children='unit')
                ], style={'textAlign':'center'})
            ])
    
    card_3 = dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="42%", height="15%", url=url_msg_in)),
                dbc.CardBody([
                    html.P('Vehicles per 100k inhabitants'),
                    html.H4(id='content_total_vehicles_in_use_rate_by_population', children="200"),
                    #html.P(id='unit_total_vehicles_in_use_rate_by_population', children='unit')
                ], style={'textAlign':'center'})
            ])
    
    card_4 = dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="37%", height="40%", url=url_msg_out)),
                dbc.CardBody([
                    html.P('Motorway Highway Ratio'),
                    html.H4(id='content_motorway_highway_ratio', children="3_000"),
                    #html.P(id='unit_motorway_highway_ratio', children='unit')
                ], style={'textAlign': 'center'})
            ])
                
    return card_1, card_2, card_3, card_4