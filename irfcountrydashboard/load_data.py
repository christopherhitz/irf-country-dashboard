#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

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

if __name__=='__main__':
        '''0.0.1 Load country dataset with features, and merge it with 
        the countrie's income group, and the country's longitude and latitude
        values.
        '''
        df_class = load_class_data(data_file='./data/CLASS.csv')        
        #print(df_class.sample(n=10))

        df_wrs = load_data_wrs(data_file='./data/WRS Data 2000-2019.csv')        
        #print(df.sample(n=10))
        #print(f"<<<<<< Shape: {df.shape}")
        
        df_lon_lat = load_world_lon_lat_data()
        #print(df.sample(n=10))
        #print(f"<<<<<< Shape: {df.shape}")
        
        df = df_wrs.merge(df_class, how='left', on='Country')
        #print(df.sample(n=10))
        #print(f"<<<<<< Shape: {df.shape}")
        #print(f"------------- Shape: {df.shape}")
        #print(f"- - - - -  {df.columns}")
        #print(df["Region"].unique())
        
        #['world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america']
        rename_dict = {'Sub-Saharan Africa': 'africa',
                'Middle East & North Africa': 'asia',
                'Latin America & Caribbean': 'south america',
                'North America': 'north america',
                'South Asia': 'asia',
                'Europe & Central Asia': 'world',
                'East Asia & Pacific': 'world'}
        df.replace({"Region": rename_dict}, inplace=True)
        print(df["Region"].unique())
                
        df = df.merge(df_lon_lat, how='left', on='Country')
        print(df.sample())
        print(df.columns)
