# libraries
import seaborn as sns
import matplotlib.pyplot as plt

def display_total_vehicles_in_use_ratio_comparison(dfObj=None, country_slctd=None, metric_slctd=None):
  
    dfObj = dfObj[dfObj["GroupName"].isin(['Low income', 'Lower middle income', 'Upper middle income', 'High income'])]
    dfObj = dfObj[dfObj["Metric"].isin([metric_slctd])]
    dfObj = dfObj.drop(['Code', 'Theme', 'latlng'], axis=1).rename(columns={'Value': dfObj["Unit"].unique()[0]}).reset_index(drop=True)
    
    # colors=['#c0e1fa', '#9fd2f9', '#70befb', '#38a6fb']
    
    # set seaborn whitegrid theme
    sns.set(style="whitegrid")

    # using small multiple
    # create a grid 
    g = sns.FacetGrid(dfObj, col='GroupName', hue='GroupName', col_wrap=2)
    
    # draw density plots
    g = g.map(sns.kdeplot,dfObj["Unit"].unique()[0], cut=0, fill=True, common_norm=False, alpha=0.5, legend=False, palette="crest")
    
    # control the title of each facet
    g = g.set_titles("{col_name}")
    
    # Vertical line
    val = dfObj[dfObj["Country"].isin([country_slctd]) & dfObj["Year"].isin([2019]) & dfObj["Metric"].isin([metric_slctd])][dfObj["Unit"].unique()[0]].unique()

    
    g.savefig('sns_facet.png')
    
    return g

def display_bubble_persons_killed(dfObj=None, country_slctd=None, metric_slctd=None):
  
    dfObj = dfObj[dfObj["GroupName"].isin(['Low income', 'Lower middle income', 'Upper middle income', 'High income'])]
    dfObj = dfObj[dfObj["Metric"].isin([metric_slctd])]
    dfObj = dfObj.drop(['Code', 'Theme', 'latlng'], axis=1).rename(columns={'Value': dfObj["Unit"].unique()[0]}).reset_index(drop=True)
    
    # colors=['#c0e1fa', '#9fd2f9', '#70befb', '#38a6fb']
    
    # set seaborn whitegrid theme
    sns.set(style="whitegrid")

    # using small multiple
    # create a grid 
    g = sns.FacetGrid(dfObj, col='GroupName', hue='GroupName', col_wrap=2)
    
    # draw density plots
    g = g.map(sns.kdeplot,dfObj["Unit"].unique()[0], cut=0, fill=True, common_norm=False, alpha=0.5, legend=False, palette="crest")
    
    # control the title of each facet
    g = g.set_titles("{col_name}")
    
    # Vertical line
    val = dfObj[dfObj["Country"].isin([country_slctd]) & dfObj["Year"].isin([2019]) & dfObj["Metric"].isin([metric_slctd])][dfObj["Unit"].unique()[0]].unique()

    
    g.savefig('sns_facet.png')
    
    return g