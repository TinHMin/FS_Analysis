# Food Security in U.S: Before and After Covid-19 Pandemic
## Objectives
The project aims to answer three learning questions:
1. Are there any disparities in food access among U.S. households of different backgrounds?
2. How did COVID-19 affect access to food? Did the different types of household experience different level of negative impact on thier food security?
3. What are the projected trends in food insecurity in the near term?

Three different analyses were conducted to response each question consecetively as follow.

## 1. Explore disparities in access to food among U.S households
### Data analysis method 
Descriptive analysis

### Key Variables  
Househould characteristics - Household size, household type, poverty status, total spending on food in last week; Geographic characteristics - State and metropolitan status; and food security status 

### Data source          
Current Population Survey - [Food Security Supplement Dataset 2023](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-food-security.2023.html#list-tab-216513607) 
 & [2023 TIGER/Line® Shapefiles: States (and equivalent)](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2023&layergroup=States+%28and+equivalent%29) from U.S Census Bureau

 ### Script   [descriptive_analysis.py](descriptive_analysis.py)  
 Using the two datasets mentioned, the script does four tasks. 
 1. Read and extract the data elements for key variables relevant for the analysis and recode the selected variables
 2. Produce the two heat maps: one 2*2 grid map and 2-panel map
 3. Caculate the weighted count of food insecure households and prevalance rates
 4. Produce a geopackage which is used to create two GIS maps with QGIS software

### Analysis Output: Visualization
<p align="center">
  <img src="/Food Insecured Household_Number_2023.png" width="45%" />
  <img src="/Food Insecured Household_Percent_2023.png" width="45%" />
</p>

**Fig 1. Absolute and percent distribution of food insecure household in U.S in 2023** 

The maps show the number of food insecure household acroos different states in the country. Some states such as Taxes, California, New York have higher number of the insecure populations which is partly attributed to the larger population size of these states. In addition, some other states such as Goregia, Arkansas, Kentuky and Lousiana, experieced higher prevalence of food insecurity. Taxes happened to have both higher prevalence and number of food insecure household.

_________________________________________________________________________________________________________

<img src="/Four_Panel_Food_Insecurity_Heatmaps.png" width='80%' >

**Fig 2. Number of food insecure houshold(in 10k) by household characteristics in four census regions** 

In general, there was a large share of food insecure household in the south. Majority of food insecure household lived in the metropolitan areas, and as expected, food insecurity was more common in those under 185% poverty line. 
_______________________________________________________________________________________________________

<img src="/Two_Panel_Food_Insecurity_Heatmaps.png" width='80%' >

**Fig 3. Number of food insecure household (in 10k) by household size and total spending on food by states**

The graph shows, generally, food insecurity was more common in smaller family households and among those with less spending on food. The condition was more prominent in such states as Taxes, New York, California, and Illinois.
_________________________________________________________________________________________________________

## 2 Assess the impact of convid-19 pandemic on access to food among different households by comparing food security status of 2019 against 2023
### Data analysis method 
Comparative analysis

### Key Variables  
Househould characteristics - Household size, household type, poverty status; Geographic characteristics - State and metropolitan status; and food security status

### Data source          
Current Population Survey -[Food Security Supplement [Dataset 2023](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-food-security.2023.html#list-tab-216513607)  & [Dataset 2019](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-food-security.2019.html#list-tab-216513607)

### Script      [comparative_analysis.py](comparative_analysis.py) 
 Using the two datasets mentioned, the script carries out three tasks. 
 1. Read and extract the data elements for key variables relevant for the analysis and recode the selected variables and merge the datasets
 2. Calculate absolute and percent differences of food security status
 3. Produce the two 2*2 grid heat maps and one bubble plot
    
### Analysis Output: Visualization

<img src="/Percent Change in Food Insecurity  by State(2019 v 2023).png" width="80%" >

**Fig 4. Changes in Food Insecurity(Number and Percent) by State (2019 v 2023)**

Percent change was calculated as (2023 − 2019) / 2019 (%). When comparing the status before COVID-19 (2019) to after (2023), the percentage decreased in the states of Alabama and Wisconsin, remained the same or nearly the same in Tennessee, Kansas, and Delaware, and increased in the remaining states. Arkansas, Idaho, Oregon, and Texas were among the states with the highest percent increases. In terms of absolute increase, Texas, Florida, California, Idaho and Ohio were the tops. 
_________________________________________________________________________________________________________

<img src="/Number of Food Insecure Households(2019 v 2023).png" width="80%">

**Fig 5. Changes in Food Insecurity(Number) by Household Characteristics (2019 v 2023)**

_________________________________________________________________________________________________________
<img src="/Food Insecurity Percentage by Group(2019 v 2023).png" width="80%" >

**Fig 6. Changes in Food Insecurity(Percent) by Household Characteristics (2019 v 2023)**

The pandemic have made the gap larger in access to food among household of different characteristics. In terms of household size, individuals living alone or in larger households experienced a higher percentage of food insecurity. Those residing in non-metropolitan areas also showed a higher prevalence compared to their metropolitan counterparts. Notably, the highest percentage was observed among individuals who did not report their residence status, suggesting a need for further investigation into who they are. Compared to others, female-headed households experienced nearly twice the burden, which was further exacerbated by the pandemic. Households living below 185% of the poverty line faced food insecurity at nearly five times the rate of those above the line. 

_________________________________________________________________________________________________________


## 3 Assess the trend of food security status and forecast for next three years

### Data analysis method 
Time series analysis - Autoregressive Integrated Moving Average (ARIMA) Model (2,0,1)

### Data source 
1. Food security data from  [Trend in U.S Food Security](https://www.ers.usda.gov/topics/food-nutrition-assistance/food-security-in-the-us/interactive-charts-and-highlights#trends) Economic Research Service USDA.
2. SNAP participation and Poverty data from [SNAP Key Statistics and Research](https://www.ers.usda.gov/topics/food-nutrition-assistance/supplemental-nutrition-assistance-program-snap/key-statistics-and-research0) Economic Research Service USDA.
   
### Script   [tseries_forecasting_analysis.py](tseries_forecasting_analysis.py) 
Using the two dataset mentioned above, the script does four key tasks as below.
1. Create a time sereis graph for food security, poverty and SNAP participation rate
2. Explore the appropriate orders for ARIMA model
3. Test the accuracy of the obtained model and produce the a graph to illustrate the model efficiency
4. Forcast the food insecurity percent for the next three years (2024-2026) and put the result on the graph

### Analysis Output: Visualization

<img src="/Food_security_trend.png" width="80%" >

**Fig 7. Long Term Trends of Food Insecurity Prevalence, SNAP Participation Rate and Poverty Rate**

The poverty rate and food insecurity rate have historically followed similar trends. The SNAP participation rate increased sharply after 2001, which may have contributed to a decline in food insecurity levels. During the COVID-19 pandemic, SNAP expanded its coverage once again but began to level off after 2021. Meanwhile, the food insecurity rate continued to rise, indicating that expanded program coverage may not have fully offset the pandemic's effects.
_________________________________________________________________________________________________________

<table>
<tr>
<td style="width:70%; vertical-align:top;">
 
 **Stationary Assessed**
1. ADF Statistic: -3.49 p-value: 0.008

**Model(2,0,1) Summary**
1. AIC    8.911
2. BIC   74.588
3. HQIC  70.339
4. intercept p-value 0.208
5. ar.l1  p-value 0.000
6. ar.l2  p-value 0.000
7. ma.l1  p-value 0.729
8. Residual Mean-squared error: 0.9140

</td>
<td style="width:30%; vertical-align:top;">
<img src="/Assess_accuracy.png" width=500>
</td>
</tr>
</table>

**Fig 8. Statistic for assessing the stationary of the series and summary of the ARIMA(2,0,1)**

The ARIMA(2,0,1) model was selected as the best-fit model using Python's auto_arima function, which automates the selection based on criteria like AIC and BIC. Overall, the ARIMA(2,0,1) model provides a statistically justified and interpretable structure for forecasting food insecurity, with strong autoregressive components capturing temporal patterns
_________________________________________________________________________________________________________
<img src="/Forecast_3years.png" width="80%" >

**Fig 9. Forecasting for the next three years 2024-26 using the ARIMA(2,0,1) model**

According to the forecast generated by the ARIMA(2,0,1) model, the food insecurity percentage is projected to continue rising in 2024, followed by a stabilization over the next two years.
