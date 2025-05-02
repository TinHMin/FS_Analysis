# Food Security in U.S: Before and After Covid-19 Pandemic
## Objectives
The project aims to answer three learning questions:
1. Are there any disparities in food access among U.S. households of different backgrounds?
2. How did COVID-19 affect access to food? Did the different types of household experience different level of negative impact on thier food security?
3. What are the projected trends in food insecurity in the near term?

Three different analyses were conducted to response each question consecetively as follow.

## A. Access disparities in access to food among U.S households
### Data analysis method - Descriptive analysis

### Key Variables  
Househould characteristics - Household size, household type, poverty status, total spending on food in last week; Geographic characteristics - State and metropolitan status; and food security status 

### Data source          
Current Population Survey - [Food Security Supplement Dataset 2023](https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-food-security.2023.html#list-tab-216513607) 
 & [2023 TIGER/Line® Shapefiles: States (and equivalent)](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2023&layergroup=States+%28and+equivalent%29) from U.S Census Bureau

 ### Script (descriptive_analysis.py)  
 Using the two datasets mentioned, the script will do four tasks. 
 1. Read and extract the data elements for key variables relevant for the analysis and recode the selected variables
 2. Produce the two heat maps: one 2*2 grid map and 2-panel map
 3. Caculate the weighted count of food insecure households and prevalance rates
 4. Produce a geopackage which is used to create two GIS maps with QGIS software

### Analysis Output: Visualization
<p align="center">
  <img src="/Food Insecured Household_Number_2023.png" width="45%" />
  <img src="/Food Insecured Household_Percent_2023.png" width="45%" />
</p>

<img src="/Four_Panel_Food_Insecurity_Heatmaps.png" >

<img src="/Two_Panel_Food_Insecurity_Heatmaps.png" >























 
