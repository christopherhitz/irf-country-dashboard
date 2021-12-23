#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_html_components as html
import numpy as np

def intro_text(country=None):
    '''This function contains the intro text which goes below the worldmap.'''
    
    #intro = f"In {2019}, {country} had a road network density of {0.33} kilometer \
    #    road per per square kilomter surface area. This is quite 
    #    a common value, compared to countries worldwide. Only central and 
    #    western European countries are showing higher values. But how is the populations access to vehicles in general? By switching 
    #    to the map Total Vehicles in Use, rated by population, we can see that
    #    {country} reaches almost {2014} vehicles per {100,000} inhabitants. This is 
    #    still in the lower third of the spectrum, and fits more with the values
    #    provided by Asian rather than European or some American countries. Due to road traffic, {country} shows very promising values with {6.56} being
    #    on the lower third third of the spectrum. From all countries which provided data in {2019}, {country} shows a very positive
    #    and common motorway to highway ratio of {1.22}, which indicates a high 
    #    level of road network."
    
    text = html.P(
            f'''In AAAAA {2019}, {country} had a road network of {0.33} kilometer \n
            road per per square kilomter surface area. This is quite \n
            a common value, compared to countries worldwide. Only central and \n
            western European countries are showing higher values. But how is the populations access to vehicles in general? By switching \n
            to the map Total Vehicles in Use, rated by population, we can see that \n
            {country} reaches almost {2014} vehicles per {100,000} inhabitants.''',
            className="lead", 
            style={'textAlign': 'left', 
                    'font-family': 'Seaford, sans-serif',
                    #'white-space': 'pre'
                    },)    
    return text

def paved_network_ratio_text(country=None, val=None, mean_high_income=None):
    '''This function contains the text which explains the paved_network_ratio_ graph for
    one selected country.'''
    
    pass