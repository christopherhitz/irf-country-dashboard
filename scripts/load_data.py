#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from flask_caching import Cache





def load_data_wrs(data_file=None):
        '''0.0.1  Create a function to load the dataset which was extracted from the Data Warehouse'''
        return pd.read_csv(data_file)

def load_class_data(data_file=None):
        '''0.0.1  Create a function to load the income group for each country'''
        dfObj = pd.read_csv(data_file)
        dfObj.rename(columns = {'CountryName':'Country'}, inplace = True)
        return dfObj

def load_world_lon_lat_data():
        '''0.0.1  Create a function to load longitude and latitude coordinates for each country'''
        url = 'https://gist.githubusercontent.com/erdem/8c7d26765831d0f9a8c62f02782ae00d/raw/248037cd701af0a4957cce340dabb0fd04e38f4c/countries.json'
        d = pd.read_json(url)
        d = d[['latlng', 'name']]
        d.rename(columns = {'name':'Country'}, inplace = True)
        return d

def countrys_latest_MetricData(dfObj=None, country='France', metric='Road Network Density'):
    dfObj = dfObj[ (dfObj['Country'] == country) & (dfObj['Metric'] == metric) ]
    latest_year = np.max(dfObj["Year"])
    dfObj = dfObj[dfObj["Year"].isin([latest_year])].reset_index(drop=True)
    metric = dfObj['Metric'][0]
    value = np.around(dfObj['Value'][0], decimals=2, out=None)
    unit = dfObj['Unit'][0]
    return metric, latest_year, value, unit

if __name__=='__main__':
        '''0.0.1 Load country dataset with features, and merge it with 
        the countrie's income group, and the country's longitude and latitude
        values.
        '''
        df_class = load_class_data(data_file='./data/CLASS.csv')        

        df_wrs = load_data_wrs(data_file='./data/WRS Data 2000-2019.csv')        
        
        df_lon_lat = load_world_lon_lat_data()

        df = df_wrs.merge(df_class, how='left', on='Country')
        
        #['world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america']
        rename_dict = {'Sub-Saharan Africa': 'africa',
                'Middle East & North Africa': 'asia',
                'Latin America & Caribbean': 'south america',
                'North America': 'north america',
                'South Asia': 'asia',
                'Europe & Central Asia': 'world',
                'East Asia & Pacific': 'world'}
        df.replace({"Region": rename_dict}, inplace=True)
                
        df = df.merge(df_lon_lat, how='left', on='Country')
        
        (metric, latest_year, value_rnd, unit_rnd) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Road Network Density')
