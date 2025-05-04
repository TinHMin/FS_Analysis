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

 ### Script (descriptive_analysis.py)  
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

<img src="/Four_Panel_Food_Insecurity_Heatmaps.png" width='80%' >

<img src="/Two_Panel_Food_Insecurity_Heatmaps.png" width='80%' >


## 2 Assess the impact of convid-19 pandemic on access to food among different households by comparing food security status of 2019 against 2023
### Data analysis method 
Comparative analysis

### Key Variables  
Househould characteristics - Household size, household type, poverty status; Geographic characteristics - State and metropolitan status; and food security status

### Data source          
Current Population Survey -[Food Security Supplement [Dataset 2023](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-food-security.2023.html#list-tab-216513607)  & [Dataset 2019](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-food-security.2019.html#list-tab-216513607)

### Script (comparative_analysis.py)  
 Using the two datasets mentioned, the script carries out three tasks. 
 1. Read and extract the data elements for key variables relevant for the analysis and recode the selected variables and merge the datasets
 2. Calculate absolute and percent differences of food security status
 3. Produce the two 2*2 grid heat maps
    
### Analysis Output: Visualization

<img src="/Percent Change in Food Insecurity  by State(2019 v 2023).png" width="80%" >
<img src="/Number of Food Insecure Households(2019 v 2023).png" width="80%">
<img src="/Food Insecurity Percentage by Group(2019 v 2023).png" width="80%" >

## 3 Assess the trend of food security status and forecast for next three years

### Data analysis method 
Time series analysis - Autoregressive Integrated Moving Average (ARIMA) Model (2,0,1)

### Data source 
1. Food security data from  [Trend in U.S Food Security](https://www.ers.usda.gov/topics/food-nutrition-assistance/food-security-in-the-us/interactive-charts-and-highlights#trends) Economic Research Service USDA.
2. SNAP participation and Poverty data from [SNAP Key Statistics and Research](https://www.ers.usda.gov/topics/food-nutrition-assistance/supplemental-nutrition-assistance-program-snap/key-statistics-and-research0) Economic Research Service USDA.
   
### Script (tseries_forecast_analysis.py)  
Using the two dataset mentioned above, the script does four key tasks as below.
1. Create a time sereis graph for food security, poverty and SNAP participation rate
2. Explore the appropriate orders for ARIMA model
3. Test the accuracy of the obtained model and produce the a graph to illustrate the model efficiency
4. Forcast the food insecurity percent for the next three years (2024-2026) and put the result on the graph

### Analysis Output: Visualization




<img src="/Forecast_3years.png"width="80%" >

<table>
<tr>
<td>

<img src="/Assess_accuracy.png">

</td>
<td>
 
 **Model diagnostics**
 a. ADF Statistic to assess data stationary: -3.49 p-value: 0.008
 b. Use z-score to detect outliers in the residuals []
 c. Residual Mean-squared error (RMSE): 0.9140


</td>
</tr>
</table>

<img src="/Food_security_trend.png" width="80%" >










 
