# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 21:39:35 2025

@author: tinhl
"""
# Initial preparation
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
#%% A Create a time sereis graph for food security, poverty and SNAP participation rate

fs_trend=pd.read_csv('fs_trends.csv', index_col=0,dtype=float)
snap=pd.read_csv('snap.csv', index_col=0, dtype=float)
tseries_df=snap.merge(fs_trend, on='Year', how = 'right')
tseries_df = tseries_df.reset_index()

# Develop a time series graph
plt.figure(figsize=(12, 6))
plt.plot(tseries_df['Year'], tseries_df['poverty_rate'], label='Poverty Rate', marker='s', linewidth=2.2)
plt.plot(tseries_df['Year'], tseries_df['snap_participate_rate'], label='SNAP Participation Rate', marker='^', linewidth=2.2)
plt.plot(tseries_df['Year'], tseries_df['insecure_percent'], label='Food Insecurity %', marker='D', linewidth=2.2)

# Shaded region for 2019–2020 (COVID onset)
plt.axvspan(2019, 2021, color='red', alpha=0.15)
plt.text(2019 + 0.1, plt.ylim()[1]*0.95, 'COVID-19', color='red', fontsize=10)

# Labels and styling
plt.title(' Trends: Food Insecurity, Poverty and SNAP Participate Rate (2001–2023)', fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Year', fontsize=13)
plt.ylabel('Percent of Population / Households', fontsize=13)
plt.legend(title='Indicator', fontsize=10, title_fontsize=11, loc='upper left', frameon=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(ticks=tseries_df['Year'], rotation=45)
plt.yticks(fontsize=10)
plt.tight_layout()
plt.savefig('Food_security_trend')
#%% B Explore the appropriate orders for ARIMA model

# 1 Prepare data for timeseries analysis
tseries_df['date'] = pd.to_datetime(tseries_df['Year'], format='%Y')

tseries_df.set_index('date', inplace=True)
tseries_df.index.freq = 'YS'
time_series = tseries_df['insecure_percent']

#%%
# 2 Check for Stationarity
# Convert to pandas Series

from statsmodels.tsa.stattools import adfuller

ts = pd.Series(time_series)

# Run Augmented Dickey-Fuller test
result = adfuller(ts)

# Print results
print('ADF Statistic:', result[0])
print('p-value:', result[1])
print('Used lag:', result[2])
print('Number of observations used:', result[3])
print('Critical Values:')
for key, value in result[4].items():
    print(f'   {key}: {value}')
# The time series is stationary at the 5% level (and at 10% too), 
# Reject the null hypothesis of a unit root and it is likely stationary

#%%
# 3 Identify ARIMA Parameters
from pmdarima import auto_arima

# Fit auto_arima to find the best parameters
auto_arima_model = auto_arima(time_series, seasonal=False, stepwise=True)
print(auto_arima_model.summary())
# Best fit model is ARIMA(2,0,1). Residual analysis :The Ljung-Box test (p=0.54>p-0.05)
# Thus, residuals are independent (white noise)

#%%
# 4 Refine the model parameters(1)

# Refitting the model without MA terms
# Set ARIMA parameters: p=2 (AR terms), d=0 (no differencing), q=0 (no MA terms)
refined_model = ARIMA(time_series, order=(2, 0, 0)) 
refined_model_fit = refined_model.fit()
print(refined_model_fit.summary())
#%%
# 5 Refine the model parameters(2)
refined_model = ARIMA(time_series, order=(1, 0, 0))  
refined_model_fit1 = refined_model.fit()
print(refined_model_fit1.summary())

# I have tried multiple combinations of MA and AR terms to countercheck if there is 
# any better model than the one produced by the auto_arima function.
#%% C Test the accuracy of the obtained model and produce the a graph to illustrate the model efficiency
# 1 Assess outlier
residuals = auto_arima_model.resid 
residuals = np.array(auto_arima_model.resid())
z_scores = (residuals - np.mean(residuals)) / np.std(residuals)
outliers = np.where(np.abs(z_scores) > 3)[0]  # Indices of outliers
print("Outliers Detected at Indices:", outliers)
# No outlier is observed


# 2 Validate the forecast accuracy of your ARIMA(2,0,1) model using RMSE (Root Mean Squared Error):
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Forecast horizon (3 years)
forecast_steps = 3  

# Split data into training and testing sets
train_size = int(len(time_series) * 0.5)  # Using 50% of the data for training 
train_data, test_data = time_series[:train_size], time_series[train_size:]

# Fit the ARIMA(2, 0, 1) model on the training data
model = ARIMA(train_data, order=(2, 0, 1))
fitted_model = model.fit()

# Forecast for the test data period
forecast = fitted_model.forecast(steps=len(test_data))

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(test_data, forecast))
print(f"RMSE: {rmse:.4f}")

# Plot actual vs forecasted values
plt.figure(figsize=(10, 6))
plt.plot(range(len(time_series)), time_series, label="Actual Data")
plt.plot(range(train_size, len(time_series)), forecast, label="Forecasted Data", color="red")
plt.axvline(x=train_size, linestyle='--', color="gray", label="Train-Test Split")
plt.legend()
plt.xlabel("Year")
plt.ylabel("Food Insecurity Percent")
plt.title("ARIMA(2, 0, 1) Forecast vs Actual")
plt.savefig('Assess_accuracy')

#%%
# D Forcast the food insecurity percent for the next three years (2024-2026) and put the result on the graph
model = ARIMA(time_series, order=(2, 0, 1))  
final_model1 = model.fit()

# Forecast the next 3 years
forecast_steps = 3  
forecast = final_model1.forecast(steps=forecast_steps)

# Generate years for the x-axis
start_year = 2001  # Starting year of your time series data
years = list(range(start_year, start_year + len(time_series)))  # Original years
forecast_years = list(range(years[-1] + 1, years[-1] + 1 + forecast_steps))  # Forecasted years

# Combine original data with forecast for smoother line
combined_data = list(time_series) + list(forecast)

# plot original and forecast data
plt.figure(figsize=(12, 6))
plt.plot(years, time_series, label="Observed Data", color="blue", linewidth=2, marker='o')
plt.plot(forecast_years, forecast, label="Forecasted Data", color="brown", linewidth=2, linestyle='--', marker='x')
plt.plot([years[-1], forecast_years[0]], [time_series[-1], forecast[0]], color="brown", linestyle='-', linewidth=2)
plt.axvline(x=years[-1], linestyle="--", color="gray", label="End of Observations")

# Add annotations for the forecasted years
for i, value in enumerate(forecast):
    plt.text(forecast_years[i], value, f"{value:.1f}", color="black", fontsize=10, ha="center", va="bottom")

# Title and labels
plt.title("Forecast: Food Insecurity Percent Among U.S. Households for Year 2024-26", fontsize=14, fontweight='bold')
plt.suptitle('Univariate time-series analysis with ARIMA(2,0,1)')
plt.xlabel("Year", fontsize=12)
plt.ylabel("Food Insecurity Percent", fontsize=12)

# Customize x-axis and y-axi ticks
plt.xticks(list(range(start_year, forecast_years[-1] + 1, 1)), rotation=45)
plt.yticks(list(range(6, 19, 2)))

# Add legend and grid
plt.grid(color="lightgray", linestyle="--", linewidth=0.7, alpha=0.7)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('Forecast_3years')
