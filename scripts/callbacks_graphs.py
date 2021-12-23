import scripts.metrics_in_theme as mit
import math
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from plotly.subplots import make_subplots

def display_total_vehicles_in_use_ratio_graph(country_slctd, metric_slctd):
    ''' ... '''
    # NOT USED ANYMORE
    pass

def display_bubble_worldmap_graph(df=None, metric='Metric', year=2018):
    ''' ... '''
    
    dfObj = df[df["Year"].isin([year]) & df["Metric"].isin([metric]) & df["GroupName"].isin(["Low income", "Lower middle income", "Upper middle income", "High income"])].reset_index(drop=True)
    dfObj = dfObj.dropna().reset_index(drop=True)    
    lat=[]
    lon=[]
    for i in range(len(dfObj["latlng"])):
        lat.append(dfObj["latlng"][i][0]) 
        lon.append(dfObj["latlng"][i][1])
    dfObj["lat"]=lat
    dfObj["lon"]=lon
    dfObj.drop(["latlng"], axis=1)
    dfObj['text'] = dfObj['Country'] + f'<br>{metric} ' + (dfObj['Value']/1e0).astype(str) + ' ' + (dfObj['Unit'])

    scaler = MinMaxScaler()
    X = np.expand_dims(dfObj['Value'], axis=1)
    scaler.fit(X)
    X = scaler.transform(X)

    dfObj["Value"] = X
    
    income_groups = ["Low income", "Lower middle income", "Upper middle income", "High income"]
    #limits = [(0,0.1), (0.2,0.3), (0.4,0.5), (0.6,0.7), (0.8,0.99)]
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    scale = 1 #250_000


    fig = go.Figure()

    for i in range(len(income_groups)): #range(len(limits)):
            #lim = limits[i]
            group = income_groups[i]
            #df_sub = dfObj[lim[0]:lim[1]]
            df_sub = dfObj[dfObj["GroupName"]==group]
            fig.add_trace(go.Scattergeo(
                locationmode = 'ISO-3',
                locations = df_sub['Code'],
                lon = df_sub['lon'],
                lat = df_sub['lat'],
                text = df_sub['text'],
                marker = dict(
                    size = df_sub['Value']/scale*100,
                    color = colors[i],
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode = 'area'
                ),
                #name = '{0} - {1}'.format(lim[0],lim[1])
                name = group
                ))
        
    fig.update_layout(
        showlegend = True,
        geo = dict(
            #scope = 'usa',
            landcolor = 'rgb(217, 217, 217)'))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ))

    fig.update_layout(
        autosize=False,
        margin=dict(t=120, b=0, l=0, r=0),
        #width=1600,
        #height=900
        )

    metric_unit=dfObj["Unit"].unique()[0]

    fig.update_layout(
        font_family="Segoe UI",
        font_color="#575757",
        title_font_family="Segoe UI",
        title_font_color="#575757",
        legend_title_font_color="#2b2b2b",
        title_text=f'<span style="font-size: 24px;"><b>{metric}</b></span>' + '<br>' +  f'<span style="font-size: 16px;">{metric_unit}</span>',
        #title_text='<span style="font-size: 24px;"><b>Surface Inland Freight Transport</b></span>' + '<br>',
        title_y=0.8,
        title_x=0.5)

    fig.update_layout(annotations=[
               go.layout.Annotation(
                    showarrow=False,
                    text='2019', #2019',
                    #xanchor='right',
                    x=0.12,
                    #xshift=275,
                    #yanchor='top',
                    y=0.2,#*max_y_value,
                    font=dict(
                        family="Segoe UI",
                        size=43,
                        color="#dbdbdb"
                    )
                )])
    
    text = 'test test test'
    
    return fig, text
    

def display_country_incomegroup_graph(df=None, theme=None, country='Country', metric='Metric', df_class=None, norm_metric=None):
    ''' ... '''      
    
    # To-do: make a dictionary for all normalization metrics, instead passing it as an argument !?
    # To-do: think about a scaling factor !?
    scaling_factor = 100_000
    # To-do: Country's income group is extracted 2x, e.g. "incomegroup_country_slctd" and "incomegroup"!?
    # To-do: "# Call the function to prepare the plot data to get both signals." ff is to complicated. Think about an easier way.
    # To-do: "# Prepare text for short analysis" is too individual. Better to store the different cases in a dictionary!?
    
    #df_class = ld.load_class_data(data_file='irfcountrydashboard/data/CLASS.csv')
    
    # Get the income group of the selected country from the World Bank data file, holding the class and area information for each country.
    incomegroup_country_slctd = df_class[df_class["Country"].isin([country]) & df_class["GroupName"].isin(['Low income', 'Lower middle income', 'Upper middle income', 'High income'])]["GroupName"].unique()[0]
    # Call the function which extracts the metrics for a specific theme from the IRF dataset, merged with World Bak datafile, and geo coordinates data file.          
    metrics = mit.metrics_in_theme(dfObj=df, theme=theme)
    # Create a dataframe for specific years, metrics, and income groups, from the merged main dataset. 
    X = mit.create_df(dfObj=df, df=df, incomegroup=incomegroup_country_slctd, metrics=metrics, years=[2014, 2015, 2016, 2017, 2018, 2019])
    # Call the function to extract the number of countries within each income group per year.
    NUM_INCOME_GROUP = mit.get_number_of_income_group_countries(df=df, years=[2014, 2015, 2016, 2017, 2018, 2019])
    # Get the maximum number of countries within a income group per year.
    vmax = NUM_INCOME_GROUP[incomegroup_country_slctd].unique()[0]
    # Create a heatmap for visualization of the number of countries per year and income group.
    #ax = sns.heatmap(X, annot=True, fmt="d",  cmap="Blues", linewidths=.6, vmin=0, vmax=vmax, square=False)
    # Extract the metric's unit from the main dataset. 
    best_metric_unit = df[df["Metric"].isin([metric])]["Unit"].unique()
    # Prepare the data for plotting.
    X_grouped, X = mit.prepare_plot_trace(dfObj=df, incomegroup=incomegroup_country_slctd, metric=metric, norm_metric=norm_metric)
    # Scale the signals 
    X["value"] = X["value"]*scaling_factor
    X_grouped["value"] = X_grouped["value"]*scaling_factor
    # Get the income group of the selected country from the World Bank data file, holding the class and area information for each country.
    incomegroup = df_class[df_class["Country"].isin([country]) & df_class["GroupName"].isin(['Low income', 'Lower middle income', 'Upper middle income', 'High income'])]["GroupName"].unique()[0]
    # Call the function to plot the signals.
    fig = mit.plot_trace(dfGroupByObj=X_grouped, dfObj=X, country=country, incomegroup=incomegroup, metric=metric, metric_unit=best_metric_unit[0])
    # Call the function to prepare the plot data to get both signals.
    dfGroupByObj, dfObj = mit.prepare_plot_trace(dfObj=df, metric=metric, norm_metric='Population', incomegroup=incomegroup_country_slctd)
    last_value_dfGroupByObj = dfGroupByObj["value"][dfGroupByObj.index[-1]]
    test = dfObj[dfObj["Country"]==country] 
    last_value_dfObj = test["value"][test.index[-1]]
    
    # Calculate difference between latest year of data for that country and mean income group value.
    diff_value = last_value_dfObj - last_value_dfGroupByObj
    # Prepare text for short analysis
    if diff_value > 0:
        trend = 'higher'
        analysis = 'is doing a great job!'
    else:
        trend = 'lower' 
        analysis = 'seems to have some potential to improve.'
    
    text = f"As we can see, {country}'s most recent value is by {diff_value} {trend} than its income group's mean value for the same year. Thus, {country} {analysis}"
    
    return fig, text



def display_bubble_persons_killed_graph(df=None, theme=None, country='Country', metric='Metric', df_class=None, norm_metric=None):
    ''' ... '''  
    
    # To-do: make the following lines more automatic, e,g, they are very hard-coded.
    features = ['Total Persons Killed', 'Total Expenditure', 'Total Vehicles In Use']
    norm_features = ['Population', 'Total Road Network', 'Population']
    unit_features = ['n', 'Mio USD', 'n']
    unit_norm_features = ['n', 'km', 'n']
    unit_after_norm = ['', 'Mio USD per km', '']
    year = 2019
    # To-do: MinMax-scale features!?
    
    dfObj = df
    # Select a subset of the main dataset.
    dfObj = dfObj[dfObj['Year'].isin([year]) & dfObj['GroupName'].isin(['Low income', 'Lower middle income', 'Upper middle income', 'High income'])]
    dfObj = dfObj[dfObj["Metric"].isin(features+norm_features)]
    # Transform from long to wide dataframe format.
    dfObj = dfObj.pivot(index=['Country', 'Year', 'GroupName'], columns=['Metric'], values='Value').reset_index(drop=False)

    # Create the normalized features columns.
    index=0
    for feature, norm_feature in zip(features, norm_features):
        dfObj[feature] = dfObj[feature] / dfObj[norm_feature]
        dfObj["Unit"] = unit_after_norm[index] 
        index += 1
        
        
    #dfObj["Total Expenditure / Total Road Network"] = dfObj["Total Expenditure"] / dfObj["Total Road Network"]
    dfObj = dfObj.sort_values(['GroupName', 'Country']).reset_index(drop=True)
    dfObj = dfObj.dropna()
    
    hover_text = []
    bubble_size = []    
    for index, row in dfObj.iterrows():
        hover_text.append(('Country: {country}<br>'+
                          'Total Persons Killed: {total_persons_killed}<br>'+
                          'Total Expenditure: {total_expenditure}<br>'+
                          'Total Vehicles In Use: {total_vehicles_in_use}<br>'+
                          'Year: {year}').format(country=row['Country'],
                                                total_persons_killed=row['Total Persons Killed'],
                                                total_expenditure=row['Total Expenditure'],
                                                total_vehicles_in_use=row['Total Vehicles In Use'],
                                                year=row['Year']))
        bubble_size.append(math.sqrt(row['Total Persons Killed']))
        
        
    dfObj['text'] = hover_text
    dfObj['size'] = bubble_size
    sizeref = 1.*np.max(dfObj['size'])/(200**1)

    # Dictionary with dataframes for each continent
    incomegroup_names = ['Low income', 'Lower middle income', 'Upper middle income', 'High income']
    incomegroup_data = {groupname:dfObj.query("GroupName == '%s'" %groupname)
                                  for groupname in incomegroup_names}
    
    incomegroup_country_slctd = {groupname:dfObj.query("Country == '%s'" %country)
                                  for groupname in incomegroup_names}
    
    # Create figure
    fig = go.Figure()
    colors = ['#e9e9e9', '#bdbdbd', '#878787', '#656565']
    index = 0
    
    for incomegroup_name, groupname in incomegroup_data.items():
        fig.add_trace(go.Scatter(
            x=groupname['Total Expenditure']*100_000, y=groupname['Total Vehicles In Use'],
            name=incomegroup_name, text=groupname['text'],
            marker_size=groupname['size'],
            line=dict(color=colors[index])
            ))
        index += 1
        
        
    # Tune marker appearance and layout
    fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                  sizeref=sizeref, 
                                                  line_width=2))

    fig.update_layout(
        #title='Persons Killed Rate /100,000 population',
        xaxis=dict(
            title='Expenditure (Mio USD / km)',
            gridcolor='white',
            #type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Vehicles in Use (n / 100,000 population)',
            gridcolor='white',
            type='log',
            gridwidth=2,
        ),
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
    )
    
    fig.update_layout(annotations=[
           go.layout.Annotation(
                showarrow=False,
                text='2019',
                xanchor='right',
                x=np.max(groupname['Total Expenditure']),
                #xshift=275,
                yanchor='top',
                y=2.05*np.min(groupname['Total Vehicles In Use']),
                font=dict(
                    family="Segoe UI",
                    size=62,
                    color="#c2baba"
                )
            )])
    
        # ---
    counter=1
    for incomegroup_name, groupname in incomegroup_country_slctd.items():
        while counter==1:
            fig.add_trace(go.Scatter(
                x=groupname['Total Expenditure'], y=groupname['Total Vehicles In Use'],
                name=country,
                marker_size=groupname['size'],
                line=dict(color='#de6262')
                ))
            counter += 1
            
    # Tune marker appearance and layout
    fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                  sizeref=sizeref, 
                                                  line_width=1))
            
    fig.update_layout(
        autosize=False,
        width=900,
        height=400,)
    
    fig.update_layout(
        font_family="Segoe UI",
        font_color="#575757",
        title_font_family="Segoe UI",
        title_font_color="#575757",
        legend_title_font_color="#2b2b2b",
        #title_text=f'<span style="font-size: 24px;"><b>{metric}</b></span>' + '<br>' +  f'<span style="font-size: 16px;">{metric_unit}</span>',
        title_text='<span style="font-size: 24px;"><b>Persons Killed Rate /100,000 population</b></span>' + '<br>',
        title_y=0.9,
        title_x=0.5)
    
    text = 'test test test'
    
    return fig, text

def display_distribution_comparison_graph(df=None, theme='Road Accidents', country='Country', years=[2014,2015,2016,2017,2018,2019], metric='Total Persons Killed'):
    ''' ... '''
    # To-do: Make code more efficient (loop subplots, ...)
    
    
    
    dfObj = df[df["Country"].isin([country]) & df["GroupName"].isin(['Low income', 'Lower middle income',  'Upper middle income', 'High income']) & df["Metric"].isin(['Fatalities Gender Ratio', 'Persons Killed Rate', 'Injury Accident Rate', 'Injury Accident Density'])]
    
    values_male = []
    for year in years:
        values_male.append(np.float(dfObj[dfObj["Metric"].isin(['Fatalities Gender Ratio']) & dfObj["Year"].isin([year])]['Value']))
    
    values_female = []
    for i in range(len(values_male)):
        values_female.append(100 - values_male[i])
        
    values = list(zip(values_male, values_female))
    labels = ['male', 'female']
    
    fig = make_subplots(rows=1, cols=len(values), 
                    column_titles = ('2014','2015','2016','2017','2018','2019'),
                    specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}]]
                   )
    
    fig.add_trace(
        go.Pie(labels=labels, values=values[0], hole=.3),
        row=1, col=1
    )
    fig.add_trace(
        go.Pie(labels=labels, values=values[1], hole=.3),
        row=1, col=2
    )
    fig.add_trace(
        go.Pie(labels=labels, values=values[2], hole=.3),
        row=1, col=3
    )
    fig.add_trace(
        go.Pie(labels=labels, values=values[3], hole=.3),
        row=1, col=4
    )
    fig.add_trace(
        go.Pie(labels=labels, values=values[4], hole=.3),
        row=1, col=5
    )
    fig.add_trace(
        go.Pie(labels=labels, values=values[5], hole=.3),
        row=1, col=6
    )

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    # calculation of circle centers
    centers = []
    counter = 0
    start = 0.045 # found by trial and error
    while counter < 6:
        #centers.append(start + (counter) * 0.22-start)
        centers.append(counter*4.88*start)
        counter += 1
        

    centers = [0.045+0*0.174, 0.045+1*0.174+0.045, 0.045+2*0.174+0.045, 0.0450+3*0.174+0.045, 0.0450+4*0.174+0.045, 0.0450+5*0.174+0.045]
    
    pd.DataFrame(centers).diff(1)

    #fig.update_layout(
    #title_text=f"Fatalities Gender Ratio {country_slctd} 2014-2019",
    # Add annotations in the center of the donut pies.
    #annotations=[dict(text='2014', x=centers[0], y=0.5, font_size=12, showarrow=False),
    #             dict(text='2015', x=centers[1], y=0.5, font_size=12, showarrow=False),
    #             dict(text='2016', x=centers[2], y=0.5, font_size=12, showarrow=False),
    #             dict(text='2017', x=centers[3], y=0.5, font_size=12, showarrow=False),
    #             dict(text='2018', x=centers[4], y=0.5, font_size=12, showarrow=False),
    #             dict(text='2019', x=centers[5], y=0.5, font_size=12, showarrow=False),                
    #            ])
    
    fig.update_layout(
        autosize=False,
        width=800,
        height=300,)
    
    fig.update_layout(
        font_family="Segoe UI",
        font_color="#575757",
        title_font_family="Segoe UI",
        title_font_color="#575757",
        legend_title_font_color="#2b2b2b",
        title_text=f'<span style="font-size: 24px;"><b>Fatalities Gender Ratio</b></span>' + '<br>' +  f'<span style="font-size: 16px;">{country} 2014-2019</span>',
        #title_text='<span style="font-size: 24px;"><b>Surface Inland Freight Transport</b></span>' + '<br>',
        title_y=0.9,
        title_x=0.5)
   
    text = 'test, test, test'
       
    return fig, text 