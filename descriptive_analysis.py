# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 20:06:10 2025

@author: tinhl
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import geopandas as gpd
plt.rcParams['figure.dpi'] = 300
#%% A Read and extract the data elements for key variables relevant for the analysis and recode the selected variables
# 1 Get the variables of interest with data from cps-fss
pd.set_option('display.max_rows', None)
data23=pd.read_csv('2023.csv', dtype=str)

data23['GESTFIPS'] = data23['GESTFIPS'].astype(str).str.zfill(2)
data23['HRHTYPE'].nunique()
list_1=['GESTFIPS','GTCO','GEREG','GTMETSTA','HRYEAR4',
      'HRHHID','HRNUMHOU', 'HRHTYPE','HHSUPWGT','PERRP',
      'HRFS12M1','HRPOOR', 'HES8B','HETS8O','PEEDUCA', 'PEMLR'] 
#print(data23['HEFAMINC'].value_counts())
data23=data23[list_1]
data23 = data23.drop_duplicates(subset=['HRHHID'])
#%%
# 2 Rename columns
data23=data23.rename(columns={
    'GESTFIPS': 'state',
    'GTCO': 'county',
    'GEREG': 'region',
    'GTMETSTA': 'metro_status',
    'HRYEAR4': 'year',
    'HRHHID':'HH_id',
    'HRNUMHOU':'HH_num',
    'HRHTYPE':'HH_type',
    'HHSUPWGT': 'weights',
    'PERRP': 'Relat_ref_person',
    'HRFS12M1': 'food_security',   
    'HRPOOR': 'poverty',
    'HES8B':'need_to_spend',
    'HETS8O':'total_food_spending',
    'PEEDUCA': 'education',
    'PEMLR': 'employment',
    })
 #%%
 # 3 Managing missing/irrelevant data and recode into readable categories, and categorise
 # 3.1 Food Security
data23= data23[~data23['food_security'].isin(['-1','-9'])] 
data23['food_security_status']=data23['food_security'].map({
    '1': "Food secure",
    '2': 'Low food insecure',
    '3':'Very low food insecure'})
data23['food_security_gp']=data23['food_security'].replace({'3':'2'})
print(data23['food_security_gp'].value_counts())
#%%
# 3.2 Poverty status
data23['pov_rename']=data23['poverty'].map({
    '1':'Below 185% poverty',
    '2': 'Above 185% poverty'
    })
print(data23['pov_rename'].value_counts())
#%%
# 3.3 Spending need to secure food
data23=data23[~data23['need_to_spend'].isin(['-1','-2','-3','-9'])]
data23['Sp_need_rename']=data23['need_to_spend'].map({
    '1':'Need to spend more',
    '2': 'Need to spend less',
    '3': 'Spend the same'
    })
print(data23['Sp_need_rename'].value_counts())
#%%
# 3.4 Total spending on food last week
def tfs(x):
    x=int(x)
    if x<=100:
        return '0-100'
    elif x<=200:
        return '101-200'
    elif x<= 300:
        return '201-300'
    elif x<=400:
        return '301-400'
    else:
        return '400+'
data23['food_spending_gp']=data23['total_food_spending'].apply(tfs)
print(data23['food_spending_gp'].value_counts().sort_index())
#%%
# 3.5 HH type
def hht(x):
    if x=='1' or x=='2':
        return 'Married-couple families'
    elif x=='3':
        return 'Male-head'
    elif x=='4':
        return 'Female-head'
    else:
        return 'Others'
data23['HH_type_gp']=data23['HH_type'].apply(hht)
ordered_status_mr=['Married-couple families','Male-head','Female-head','Others']
data23['HH_type_gp']= pd.Categorical(data23['HH_type_gp'], categories=ordered_status_mr, ordered=True)

print(data23['HH_type_gp'].value_counts().sort_index())
#%%
# 3.6 HH Number
print(data23['HH_num'].value_counts())
def hhn(x):
    if x=='1':
        return '1'
    elif x=='2':
        return '2'
    elif x=='3':
        return '3'
    elif x=='4':
        return '4'
    elif x=='5':
        return '5'
    elif x=='6':
        return '6'
    else:
        return '7+'
    
data23['HH_num_gp']=data23['HH_num'].apply(hhn)
ordered_status_HHS=['1','2','3','4','5','6','7+']
data23['HH_num_gp']= pd.Categorical(data23['HH_num_gp'], categories=ordered_status_HHS, ordered=True)
print(data23['HH_num_gp'].value_counts().sort_index())
#%%
# 3.7 Region & Metropolitan status
data23['region']=data23['region'].map({
    '1': 'Northeast',
    '2':'Midwest',
    '3':'South',
    '4':'West'
    })
data23['metro_status']=data23['metro_status'].map({
    '1': 'Metro',
    '2': 'Nonmetro',
    '3': "Not ID'd"
    })
print(data23['region'].value_counts())
#%%
# 4 Get weighted count of food insecurity
data23['weights']=data23['weights'].astype(int)/10000000
data23_insecure = data23[data23['food_security_gp']=='2']
#%% B Visualization: Produce the two heat maps: a 2*2 grid map and 2-panel map


# 1 Merge with geodata file
state_geo=gpd.read_file('cb_2023_us_state_500k.zip')
list_2=['STATEFP','STUSPS','NAME','geometry','ALAND','AWATER']
state_geo=state_geo[list_2]
state_geo=state_geo[~state_geo['STATEFP'].isin(['78','69','66','72'])]
state_geo['STATEFP'] = state_geo['STATEFP'] .astype(str)

# Merge with the cps-fss data for 2023 data analysis
data23_merged=data23_insecure.merge(state_geo, right_on='STATEFP', left_on='state', how='left', validate='many_to_one')


#%%
# 2 Create a four-panel heat map
variables = ['metro_status', 'pov_rename','Sp_need_rename', 'HH_type_gp']
titles = ['Metropolitan Status', 'Poverty Staus among Lowest Income Group','Spending for Food', 'Household Type', ]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Number of Food Insecured Household (10k) by Census Regions", fontsize=16)

# Generate heatmaps
for ax, var, title in zip(axes.flat, variables, titles):
    heat_data = data23_merged.groupby(['region', var])['weights'].sum().reset_index()
    pivot = heat_data.pivot(index='region', columns=var, values='weights')
    
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax, annot_kws={"size": 10})
    ax.set_title(title, fontsize=13)
    ax.set_xlabel(' ')

    ax.set_ylabel('Census Region')
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10, labelrotation=0)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Four_Panel_Food_Insecurity_Heatmaps.png')

#%%
# 3 Create a 2-panel heatmap graph

# prepare the data
print(data23['state'].value_counts())
heat_data1 = data23_merged.groupby(['NAME', 'HH_num_gp'])['weights'].sum().reset_index()
pivot1 = heat_data1.pivot(index='NAME', columns='HH_num_gp', values='weights')

heat_data2 = data23_merged.groupby(['NAME', 'food_spending_gp'])['weights'].sum().reset_index()
pivot2 = heat_data2.pivot(index='NAME', columns='food_spending_gp', values='weights')

# create map
fig, axes = plt.subplots(1, 2, figsize=(14, 12), sharey=True)

# Panel 1
sns.heatmap(pivot1, annot=True, fmt=".0f", cmap="YlGnBu", annot_kws={"size": 8}, ax=axes[0])
axes[0].set_title("Number of Food Insecured HHs by HH Size(10k)", fontsize=11)
axes[0].set_xlabel("Household Size")
axes[0].set_ylabel('')
axes[0].tick_params(axis='y', labelsize=10)

# Panel 2
sns.heatmap(pivot2, annot=True, fmt=".0f", cmap="YlGnBu", annot_kws={"size": 8}, ax=axes[1])
axes[1].set_title("Number of Food Insecured HHs by Spending on Food(10k)", fontsize=11)
axes[1].set_xlabel("Spending on food by HH last week(cap US$500)")
axes[1].set_ylabel("")  # Hide duplicate y-axis label

plt.tight_layout()
plt.savefig('Two_Panel_Food_Insecurity_Heatmaps.png')

#%%
# C Calculation of weights and percent of food insecurity HH
# 1 Preparation
data2023=pd.read_csv('2023.csv')
data2023 = data2023[~data2023['HRFS12M1'].isin([-1, -9])]
data2023 = data2023.drop_duplicates(subset='HRHHID') # get data for unique household
data2023['HRFS12M1'] = data2023['HRFS12M1'].replace({3: 2})
print(data2023['HRFS12M1'].value_counts())
# 2 Weight and percent calculation by state
def summarize_state(group):
    insecure = round(group.loc[group['HRFS12M1'] == 2, 'HHSUPWGT'].sum() / 10000,0)
    total = round(group['HHSUPWGT'].sum() / 10000,0)
    return pd.Series({'insecure': insecure, 'total': total})

state_grouped = data2023.groupby('GESTFIPS').apply(summarize_state).reset_index()

state_grouped['percent_insecure'] = ((state_grouped['insecure'] / state_grouped['total']) * 100).round(1)

# 3 Percent for the whole country
insecure_total = data2023.loc[data2023['HRFS12M1'] == 2, 'HHSUPWGT'].sum()
total_households = data2023['HHSUPWGT'].sum()
percent_insecure_national = (insecure_total / total_households) * 100
print(f"National food insecurity rate: {percent_insecure_national:.2f}%")
#%%
# D Prepare geopackage to develop two maps in QGIS
# 1 initial preparation and merge the the two dataset
state_grouped['GESTFIPS'] = state_grouped['GESTFIPS'].astype(str).str.zfill(2)
data2023_merged=state_geo.merge(state_grouped, left_on='STATEFP', right_on='GESTFIPS', how='right')
data2023_merged= data2023_merged.to_crs('EPSG:5070')

# Split Alaska, Hawaii, and contiguous state
alaska = data2023_merged[data2023_merged['NAME'] == 'Alaska'].copy()
hawaii = data2023_merged[data2023_merged['NAME'] == 'Hawaii'].copy()
conus=data2023_merged[~data2023_merged['NAME'].isin(['Alaska','Hawaii'])].copy()

# Adjust geometries
alaska.geometry = alaska.scale(xfact=0.35, yfact=0.35, origin='center')  # shrink
alaska.geometry = alaska.translate(xoff=2200000, yoff=-4600000)          # move southeast
hawaii.geometry = hawaii.translate(xoff=5200000, yoff=-1400000)

# Combine the split files into a simple dataframe and produce a gpkg
data2023_merged_adj = pd.concat([conus, alaska, hawaii])
data2023_merged_adj.to_file('food_insecurity_2023_1.gpkg', driver='GPKG', layer='FS')

