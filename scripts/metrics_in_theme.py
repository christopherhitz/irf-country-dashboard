import pandas as pd
import seaborn as sns # for data visualization
import pandas as pd # for data analysis
import numpy as np # for numeric calculation
import matplotlib.pyplot as plt # for data visualization

import plotly.graph_objects as go
import numpy as np

import scripts.load_data as ld

# Metrics withing this theme
def metrics_in_theme(dfObj=None, theme='Road Expenditure and Revenue'):
    '''Get the metrics for one specific theme.
    Input:  - dfObj:         pandas.DataFrame
            - theme:         string
    Output: - Obj:           array of strings
    '''

    dfObj = dfObj[dfObj["Theme"].isin([theme])]
    x=dfObj["Metric"].unique()

    return dfObj["Metric"].unique()

def subset_income_groups_metrics(dfObj=pd.DataFrame({'country': ['A', 'B', 'C', 'D'], 'Metric': ['a', 'b', 'c', 'd'], 'GroupName': ['LI', 'LMI', 'UMI', 'HI']}), metrics=["a", "c"], incomegroups=['UMI']):
    '''Get a subset of the initial dataset for specific metrics and income groups.
    Input:  - dfObj:         pandas.DataFrame
            - metrics:       array of strings
            - incomegroups:  array of strings
    Output: - dfObj:         pandas.DataFrame
    '''
    boolean_mask = dfObj["Metric"].isin(metrics) & dfObj["GroupName"].isin(incomegroups)
    dfObj = dfObj[boolean_mask].reset_index(drop=True)
    return dfObj

def get_number_countries(dfObj=None, metric='Inland Surface PRIVATE Passenger Transport by ROAD', income_group='Lower middle income', year=2014):
    '''Get the countries for a specific income group, metric, and year.
    Input:  - dfObj:         pandas.DataFrame
            - metric:        string
            - incomegroup:   string 
            - year:          int, e.g. YYYY
    Output: - X:             pandas.DataFrame
            - num_countries: int
    '''
    for income_group in [income_group]:
        for metric in [metric]:
            for year in [year]:                
                X = dfObj[dfObj["GroupName"].isin([income_group]) & dfObj["Metric"].isin([metric]) & dfObj["Year"].isin([year])]
                num_countries = len(X["Country"])
    X = X.reset_index(drop=True)                            
    return X, num_countries 

def create_df(dfObj=None, df=None , metrics=['Total Inland Surface Freight Transport'], incomegroup='Lower middle income', years=[2014, 2015, 2016, 2017, 2018, 2019], country_slctd='Turkey'):
    '''Create DataFrame with the number of countries for a soecific income group for several metric and years.
    Input:  - dfObj:         pandas.DataFrame   
            - metrics:       array of strings
            - incomegroup:   string
            - years:         array of integers 
    Output: - dfObj:         pandas.DataFrame
    '''   
    
    # Get income group of selected country
    incomegroup_country_slctd = dfObj[dfObj["Country"].isin([country_slctd]) & dfObj["GroupName"].isin(['Low income',
                         'Lower middle income',
                         'Upper middle income',
                         'High income'])]["GroupName"].unique()[0]
    
    # Create DataFrame
    dfObj = pd.DataFrame(columns= metrics, index=range(0, len(years)))
 
    # Populate the dataframe with years
    dfObj.index = years
    #dfObj["GroupName"] = incomegroup
    
    # Reminder: Years are in the index of the dfObj
    for index, year in enumerate(years):
    
        for income_group in [incomegroup]:
       
            for metric in metrics:
 
                # Call  to calculate the number of countries
                X, num_countries = get_number_countries(dfObj=df, income_group=income_group, metric=metric, year=year)
      
                dfObj.at[year, metric] = num_countries
                
    # using dictionary to convert specific columns
    convert_dict = {incomegroup_country_slctd: int,
                    'Total Inland Surface Freight Transport': int,
                    'Inland Surface PUBLIC Passenger Transport by ROAD': int,
                    'Inland Surface PRIVATE Passenger Transport by ROAD': int
                   }  
    
    #dfObj = dfObj.astype(convert_dict)
    dfObj = dfObj.apply(pd.to_numeric, errors='ignore')
    #dfObj.set_index([dfObj.columns[0]], inplace=True)
    dfObj = dfObj.transpose()


    return dfObj                                   

def get_number_of_income_group_countries(df=None, years=None):
    '''Create DataFrame with Column Names & Specific Number of Rows.'''
    # Create DataFrame
    dfObj = pd.DataFrame(columns=['year', 'Low income', 'Lower middle income', 'Upper middle income', 'High income'],
                  index=range(0, len(years)))
    dfObj[f'year'] = years
            
    #Populate the dataframe with years
    for index, year in enumerate(years):        
        for income_group in dfObj.columns[1:]:
            num_countries = len(df[df["GroupName"].isin([income_group]) & df["Year"].isin([year])]["Country"].unique())
            dfObj.at[index, income_group] = num_countries
         
    return dfObj                
    
def normailze_metric(dfObj=pd.DataFrame({"Country": ['Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'France', 'France', 'France', 'France'],
                   "Metric": ['A', 'B', 'C', 'D', 'A', 'B', 'C', 'D'],
                   "GroupName": ['Low income', 'Low income', 'Low income', 'Low income', 'High income', 'High income', 'High income', 'High income'],
                   "Year": [2014, 2014, 2014, 2014, 2015, 2015, 2015, 2015],          
                   "Value": [1, 2, 3, 4, 10, 20, 30, 40]}),
         metric_to_norm='C',
         norm_metric='D'):
    ''' This function takes a metric and normalizes it using another metric.
    Input:  - dfObj:          pandas.DataFrame
            - metric_to_norm: string
            - norm_metric:    string
    Outout: - dfObj:          pandas.DataFrame
    '''
    dfObj = dfObj.pivot(index=['Country', 'Year', 'GroupName'], columns=['Metric'], values='Value')
    dfObj[f"{metric_to_norm}_norm"] = dfObj[metric_to_norm] / dfObj[norm_metric]
    
    '''Wide panel to long format. Less flexible but more user-friendly than melt.'''
    '''Unpivot a DataFrame from wide to long format, optionally leaving identifiers set.'''
    dfObj = dfObj.reset_index(drop=False)
    dfObj = pd.melt(dfObj, id_vars=['Country', 'Year', 'GroupName'], value_vars=[metric_to_norm, norm_metric, f"{metric_to_norm}_norm"])
    return dfObj

def prepare_plot_trace(dfObj=None, metric='Total Inland Surface Freight Transport', norm_metric='Total Road Network', incomegroup='Upper middle income'):
    '''Now, we want to plot the time signal of
    - the average for all countries within one income group
    - a specific country of that income group 
    
    Pitfalls:
    - Number of countries per time point may differ
    - Countries per time point may differ
    - Since the used metric for the countries will have different ranges, we need to normalize them, to make them comparable.
    - It might be often the case, that a country has no values for the metric, or the metric used for normalization.
    
    Input:  - dfObj:        pandas.DataFrame
            - metric:       string
            - norm_metric:  string
            - incomegroup:  string
    Output: - dfGroupByObj: pandas.DataFrame grouped by list of strings, e.g. ['Year','GroupName', 'Country'] 
    '''
    
    
    dfObj = dfObj.drop(['Theme', 'latlng', 'Code'], axis=1)
    dfObj = dfObj[dfObj["Year"].isin(np.arange(2014, 2019, 1, dtype=int))]
    dfObj = dfObj[dfObj["Metric"].isin([metric]+[norm_metric])]
    dfObj = dfObj[dfObj["GroupName"].isin([incomegroup])]
    unit = dfObj["Unit"].unique()
    dfObj = dfObj.drop(['Unit'], axis=1)
    #dfObj = dfObj[dfObj["Metric"].isin([metric]+[norm_metric]) & dfObj["GroupName"].isin(incomegroups)]
    #ddfObjfObj = dfObj.drop(['Metric'], axis=1)
    
    
    #Norm
  
    dfObj = normailze_metric(dfObj=dfObj, metric_to_norm=metric, norm_metric=norm_metric) 
    dfObj = dfObj[dfObj["Metric"].isin([f"{metric}_norm"])].reset_index(drop=True) 
    
    index = ['Year','GroupName', 'Country']
    dfGroupByObj = dfObj.set_index(index)
    
    '''Returns a groupby object that contains information about the groups.'''
    dfGroupByObj = dfGroupByObj.groupby(["Year", "GroupName"]).mean()
    return dfGroupByObj, dfObj
   
def plot_trace(dfGroupByObj=None, dfObj=None, incomegroup='Upper middle income', years=[2014, 2015, 2016, 2017, 2018], country='Turkey', metric='Total Inland Surface Freight Transport', metric_unit='Mio Tonne-Km'):
    '''This function plots two signals:
        1. Time trace of the mean of a normalized metric for all countries of an income group which provided data.
        2. The normalized values of the same metric as in 1. But for a single country from the income group in 1.
    Input:  - dfGroupByObj: pandas.GroupedByObject
            - dfObj:        pandasDataFrame
            - incomegroup:  string
            - years:        array of integegers, e.g. YYYY
            - country:      string
            - metric:       string 
            - metric_unit:  string
    Output: - fig:          figure object       
    '''
    
    dfObj = dfObj[dfObj["Country"].isin([country])]
    dfObj = dfObj.reset_index(drop=True)
    dfObj.value = dfObj.value.round(2)
    dfObj = dfObj.sort_values(['Year', 'Country'])
    dfObj.set_index(["Year"], inplace=True)
    
    dfGroupByObj = dfGroupByObj.sort_values(['Year', 'GroupName'])
    dfGroupByObj = dfGroupByObj.reset_index(drop=False)    
    dfGroupByObj.value = dfGroupByObj.value.round(2)
    dfGroupByObj.set_index(["Year"], inplace=True)
    
    max_y_value = np.max([np.max(dfObj["value"]), np.max(dfGroupByObj.value)])
   
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfObj.index, y=dfObj["value"], name=country,
                    text=dfObj['value'],
                    hoverinfo='name',
                    line_shape='spline',
                    marker={'size':10},
                    mode='lines+markers+text',         
                    line=dict(color="#00a3ff")))
    
    fig.add_trace(go.Scatter(x=dfGroupByObj.index, y=dfGroupByObj.value, name=f"mean of {incomegroup}",
                    text=dfGroupByObj['value'],
                    hoverinfo='text+name',
                    line_shape='spline',
                    marker={'size':10},
                    mode='lines+markers+text',         
                    line=dict(color="#2b2b2b")))
    
    
    for country in dfObj["Country"].unique():
        data=dfObj[dfObj["Country"].isin([country])]        
        #fig.add_trace(go.Scatter(x=data.Year, y=data.value, mode='markers', name=country,
        #                    text=["tweak line smoothness<br>with 'smoothing' in line object"],
        #                    hoverinfo='text+name'))
    
    #fig.add_trace(go.Scatter(x=x, y=y3["Value"] + 5, mode='markers', name="All",
    #                text=["tweak line smoothness<br>with 'smoothing' in line object"],
    #                hoverinfo='text+name'))
    
    fig.update_traces(hoverinfo='text+name', mode='lines+markers+text', textposition='top center')
    fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

    fig.update_layout(margin=dict(t=50, r=0, l=0, b=50),
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='#ffffff',
                             yaxis=dict(title=None, showgrid=False, showticklabels=False),
                             xaxis=dict(title=None, showgrid=False, showticklabels=True)
                            ).update_yaxes(
                                            showline=False,
                                            linewidth=0.25,
                                            matches=None,  #autoscale y axis
                                            linecolor='gray',
                                            gridcolor='gray'
                                            )
    
     
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ))
    
    fig.update_layout(
        autosize=False,
        width=500,
        height=300,)
    
    fig.update_layout(
        font_family="Segoe UI",
        font_color="#575757",
        title_font_family="Segoe UI",
        title_font_color="#575757",
        legend_title_font_color="#2b2b2b",
        title_text=f'<span style="font-size: 24px;"><b>{metric}</b></span>' + '<br>' +  f'<span style="font-size: 16px;">{metric_unit}</span>',
        #title_text='<span style="font-size: 24px;"><b>Surface Inland Freight Transport</b></span>' + '<br>',
        title_y=0.9,
        title_x=0.5)
    
    
    
    fig.update_layout(annotations=[
           go.layout.Annotation(
                showarrow=False,
                text='',
                #xanchor='right',
                x=2016,
                #xshift=275,
                yanchor='top',
                y=1.05*max_y_value,
                font=dict(
                    family="Segoe UI",
                    size=16,
                    color="#0000FF"
                )
            )])
        
    
    return fig

