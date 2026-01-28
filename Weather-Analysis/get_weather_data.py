import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Get user input for the location
location = input("Example format: 'Vancouver, Canada' or 'Paris, France'\nEnter city and country: ")

# Get location data
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
geo_response = requests.get(geo_url).json()

if not geo_response.get('results'):
    print(f"Could not find coordinates for '{location}'. Please check the spelling.")
    exit()

# Extract location details
location = geo_response['results'][0]
latitude = location['latitude']
longitude = location['longitude']
city = location['name']
country = location.get('country', '')



# Calculate dates
today = datetime.now()
week_ago = today - timedelta(days = 7)

# Format dates for API (YYYY-MM-DD)
start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")



# Get weather for past week
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min"

response = requests.get(weather_url)
data = response.json()



# Extract the daily data
daily_data = data['daily']

# Create a DataFrame
df = pd.DataFrame({
    'date': daily_data['time'],
    'max_temp': daily_data['temperature_2m_max'],
    'min_temp': daily_data['temperature_2m_min']
})

# Convert date strings to datetime
df['date'] = pd.to_datetime(df['date'])



# Create the plot
plt.figure(figsize = (10, 6))
plt.plot(df['date'], df['max_temp'], marker = 'o', label = 'Max Temp')
plt.plot(df['date'], df['min_temp'], marker = 'o', label = 'Min Temp')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title(f'{city}, {country} Weather - Past 7 Days')
plt.legend()

# Rotate x-axis labels for readability
plt.xticks(rotation = 45)
plt.tight_layout()


# Create charts folder if it doesn't exist
if not os.path.exists('charts'):
    os.makedirs('charts')

# Save the plot
plt.savefig(f'charts/{city}_{country}_weather_chart.png')
print(f"Plot saved to charts/{city}_{country}_weather_chart.png")
plt.show()


# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Save to CSV
df.to_csv(f'data/{city}_{country}_weather.csv', index = False)
print(f"Data saved to data/{city}_{country}_weather.csv")