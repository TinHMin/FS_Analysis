# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 15:02:30 2025

@author: tinhl
"""
# Initial preparation and compilation
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300
#%% A Read and extract the data elements for key variables relevant for the analysis and recode the selected variables and merge the datasets
data2019=pd.read_csv('2019.csv')
data2019 = data2019.rename(columns={
    'GCFIP': 'GESTFIPS',
    'GCTCO': 'GTCO'
})
#  Get only necessary varibles , drop irrelevant data, and 
# combine the two datasets 2019 and 2023
list_3=['GESTFIPS','GTCO','GEREG','GTMETSTA','HRYEAR4',
      'HRHHID','HRNUMHOU', 'HRHTYPE','HHSUPWGT','PERRP',
      'HRFS12M1','HRPOOR', 'HES8B','HETS8O','PEEDUCA', 'PEMLR'] 
# get data2023
data2023=pd.read_csv('2023.csv')
data2023 = data2023[~data2023['HRFS12M1'].isin([-1, -9])]
data2023 = data2023.drop_duplicates(subset='HRHHID') # get data for unique household
data2023['HRFS12M1'] = data2023['HRFS12M1'].replace({3: 2})


# get data 2019 and combine
data2019= data2019[~data2019['HRFS12M1'].isin([-1,-9])] 
data2019 = data2019.drop_duplicates(subset='HRHHID') # get data for unique household
data_19_23 = pd.concat([data2019, data2023], ignore_index=True)
data_19_23=data_19_23[list_3]

#%% B Calculate absolute and percent differences of food security status

# 1 Regroup food insecurity (yes/no),
data_19_23['HRFS12M1'] = data_19_23['HRFS12M1'].replace({3: 2})
# Filter to food insecure only (HRFS12M1 == 2 ) and group by state and year of sums of weights
df_insecure = data_19_23[data_19_23['HRFS12M1'].isin([2])].copy()
gped = df_insecure.groupby(['GESTFIPS', 'HRYEAR4'])['HHSUPWGT'].sum().div(10000).reset_index()

# Pivot the table to have years as columns and reanme the year columns
data_19_23c = gped.pivot(index='GESTFIPS', columns='HRYEAR4', values='HHSUPWGT').reset_index()
data_19_23c.columns.name = None
data_19_23c = data_19_23c.rename(columns={2019: 'insecure_2019', 2023: 'insecure_2023'})

# Calculate the difference(number & percent)
data_19_23c['abs_diff_23_19'] = round(data_19_23c['insecure_2023'] - data_19_23c['insecure_2019'],0)
data_19_23c['percent_diff']=round(data_19_23c['abs_diff_23_19']/data_19_23c['insecure_2019']*100,1)
#%%
# 2 Check if the weight calculation is correct by comparing the result with published report data
def summarize_state(group):
    insecure = round(group.loc[group['HRFS12M1'] == 2, 'HHSUPWGT'].sum() / 10000,0)
    total = round(group['HHSUPWGT'].sum() / 10000,0)
    return pd.Series({'insecure': insecure, 'total': total})


state_grouped_19 = data2019.groupby('GESTFIPS').apply(summarize_state).reset_index()
state_grouped_19['percent_insecure'] = ((state_grouped_19['insecure'] / state_grouped_19['total']) * 100).round(1)
insecure_total_19 = data2019.loc[data2019['HRFS12M1'].isin([2,3]), 'HHSUPWGT'].sum()
total_households_19 = data2019['HHSUPWGT'].sum()
percent_insecure_national_19 = (insecure_total_19 / total_households_19) * 100
print(f"National food insecurity rate: {percent_insecure_national_19:.2f}%")
#%%
# 3 Merge with the geo data
data_19_23c['GESTFIPS'] = data_19_23c['GESTFIPS'].astype(str).str.zfill(2)
#  Get the state names and geo data
state_geoc=gpd.read_file('cb_2023_us_state_500k.zip')
list_2c=['STATEFP','STUSPS','NAME']
state_geoc=state_geoc[list_2c]
state_geoc=state_geoc[~state_geoc['STATEFP'].isin(['78','69','66','72'])]
state_geoc['STATEFP'] = state_geoc['STATEFP'] .astype(str)
data_19_23cg=data_19_23c.merge(state_geoc, right_on='STATEFP', left_on='GESTFIPS', how='left')
#%% D Visualization: Create three graphs
#1 Create a scatter plot graph to show abs and percent different 
# before/after covid-19 pandemic across states

# Create the Plot
plt.figure(figsize=(14,8))
sns.scatterplot(
    data=data_19_23cg,
    x='NAME',
    y='percent_diff',
    size='abs_diff_23_19',
    sizes=(40, 400),
    hue='percent_diff',
    palette='coolwarm',
    edgecolor='green',
    marker='o',
    legend = 'brief'
)

# Formatting
plt.title('Percent Change in Food Insecurity (2019 v 2023) by State\n(Bubble Size = Net increase from 2019)', fontsize=13)
plt.xlabel('State')
plt.ylabel('Percent Difference')
plt.axhline(0, color='gray', linestyle='--')
plt.xticks(rotation=90)
plt.legend(title='Legend', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('Percent Change in Food Insecurity  by State(2019 v 2023)')
#%%
# 2 Categorize data: Change datatype, grouping and rename;
# Rename poverty column
data_19_23['poverty']=data_19_23['HRPOOR'].map({
    1:'Below 185% poverty',
    2: 'Above 185% poverty'
    })
data_19_23['poverty'] = data_19_23['poverty'].astype(str)
print(data_19_23['poverty'].value_counts())

# Rename metropolitan status
data_19_23['metro_status']=data_19_23['GTMETSTA'].map({
    1: 'Metro',
    2: 'Nonmetro',
    3: "Not ID'd"
    })
print(data_19_23['metro_status'].value_counts())

# Group HH type using hht function from 'get_clean.py'
def hht(x):
    if x=='1' or x=='2':
        return 'Married-couple families'
    elif x=='3':
        return 'Male-head'
    elif x=='4':
        return 'Female-head'
    else:
        return 'Others'
    
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

data_19_23['HRHTYPE'] = data_19_23['HRHTYPE'].astype(str)
data_19_23['HH_type']=data_19_23['HRHTYPE'].apply(hht)
ordered_status_mr=['Married-couple families','Male-head','Female-head','Others']
data_19_23['HH_type']= pd.Categorical(data_19_23['HH_type'], categories=ordered_status_mr, ordered=True)
print(data_19_23['HH_type'].value_counts().sort_index())

# Group HH size using hhn function from get_clean.py
data_19_23['HRNUMHOU'] = data_19_23['HRNUMHOU'].astype(str)
data_19_23['HH_num']=data_19_23['HRNUMHOU'].apply(hhn)
ordered_status_HHS=['1','2','3','4','5','6','7+']
data_19_23['HH_num']= pd.Categorical(data_19_23['HH_num'], categories=ordered_status_HHS, ordered=True)
print(data_19_23['HH_num'].value_counts().sort_index())

#%%
# 4 Calculate the weighted counts
df_insecure_2 = data_19_23[data_19_23['HRFS12M1'].isin([2])].copy()
# Adjust weights
df_insecure_2['HHSUPWGT']=df_insecure_2['HHSUPWGT'].div (10000).round(0)
df_insecure_2.to_csv('data_19_23.csv')
#%%
# 5 Visualize to show absolute changes in food insecurity by four HH characterisitcs

# Create 2x2 grid of heatmaps

variables = ['metro_status', 'poverty','HH_type', 'HH_num']
titles = ['Metropolitan Status', 'Poverty Staus among Lowest Income Group','Household Type', 'Household Size', ]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Number of Food Insecured Household (10k) Before and After Pandemic", fontsize=16)

# Generate heatmaps
for ax, var, title in zip(axes.flat, variables, titles):
    heat_data_1 = df_insecure_2.groupby(['HRYEAR4', var])['HHSUPWGT'].sum().reset_index()
    pivot_1 = heat_data_1.pivot(index=var, columns='HRYEAR4', values='HHSUPWGT')

    sns.heatmap(pivot_1, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax, annot_kws={"size": 10})
    ax.set_title(title, fontsize=16)
    ax.set_xlabel(' ')

    ax.set_ylabel('')
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelrotation=0)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Number of Food Insecure Households(2019 v 2023)')


#%%
# 6 Visualize to show percent changes in food insecurity by four HH characterisitcs


# Updated function to compute % food insecure using HRFS12M1 == 2
def get_insecurity_percent(df, group_vars):
    group_cols = group_vars + ['HRYEAR4', 'HRFS12M1']
    
    # Weighted count
    df_grouped = data_19_23.groupby(group_cols)['HHSUPWGT'].sum().reset_index(name='count')
    
    # Total households per group
    df_total = df_grouped.groupby(group_vars + ['HRYEAR4'])['count'].sum().reset_index(name='total')
    
    # Merge and compute percent
    df_merged = df_grouped.merge(df_total, on=group_vars + ['HRYEAR4'])
    df_merged['percent'] = df_merged['count'] / df_merged['total'] * 100
    
    # Keep only food insecure (HRFS12M1 == 2)
    df_insecure = df_merged[df_merged['HRFS12M1'] == 2]
    
    return df_insecure[group_vars + ['HRYEAR4', 'percent']]

# Prepare each data slice
df_HH_num = get_insecurity_percent(data_19_23, ['HH_num'])
df_metro = get_insecurity_percent(data_19_23, ['metro_status'])
df_poverty = get_insecurity_percent(data_19_23, ['poverty'])
df_HH_type = get_insecurity_percent(data_19_23, ['HH_type'])

# Function to pivot and reshape for heatmap
def reshape_for_heatmap(df, group_var):
    df['group'] = df[group_var].astype(str) if isinstance(group_var, str) else df[group_var].agg('|'.join, axis=1)
    pivot = df.pivot(index='group', columns='HRYEAR4', values='percent')
    return pivot.sort_index()

# Reshape each for heatmap
hm_HH_num = reshape_for_heatmap(df_HH_num, 'HH_num')
hm_metro = reshape_for_heatmap(df_metro, 'metro_status')
hm_poverty = reshape_for_heatmap(df_poverty, 'poverty')
hm_HH_type = reshape_for_heatmap(df_HH_type, 'HH_type')


# Set up 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
heatmaps = [hm_HH_num, hm_metro, hm_poverty, hm_HH_type]
titles = ['By Household Size', 'By Metro Status', 'By Poverty Level', 'By Household Type']

# Plot each heatmap
for ax, data, title in zip(axes.flat, heatmaps, titles):
    sns.heatmap(data, annot=True, cmap='YlOrRd', fmt=".1f", linewidths=0.5, 
                cbar_kws={'label': '% Food Insecure'}, ax=ax, annot_kws={"size": 10})
    ax.set_title(title)
    ax.set_xlabel('Year')
    ax.set_ylabel('')

plt.tight_layout()
plt.suptitle('Food Insecurity Percentage by Group (2019 vs 2023)', fontsize=16, y=1.02)
plt.savefig('Food Insecurity Percentage by Group(2019 v 2023)')
