#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Updating the 5 number cards 
def update_small_cards(country_slctd):
    
    # Road Network Density
    (metric, latest_year, value_rnd, unit_rnd) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Road Network Density')
    print(f"Road Network Density: {value_rnd}")         
    
    # Persons Killed Rate
    (metric, latest_year, value_pkr, unit_pkr) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Persons Killed Rate')
    print(f"Persons Killed Rate: {value_pkr}")
    
    # TOTAL VEHICLES IN USE BY POPULATION
    (metric, latest_year, value_tvp, unit_tvp) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Total Vehicles In Use Rate by Population') 
    print(f"Total Vehicles in Use Rate by Population: {value_tvp}")
    
    # TOTAL VEHICLES IN USE BY NETWORK
    #(metric, latest_year, value_tvn, unit_tvn) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Total Vehicles In Use Rate by Network')
    #print(f"Total Vehicles in Use Rate by Network: {out_num}")
        
    # Motorway Highway Ratio  
    (metric, latest_year, value_mhr, unit_mhr) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Motorway Highway Ratio')
    print(f"Motorway Highway Ratio: {value_mhr}")
    
    return value_rnd, unit_rnd, value_pkr, unit_pkr, value_tvp, unit_tvp, value_mhr, unit_mhr