from ignore.API_KEY import API_KEY, DATA_SET
import requests as rq
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import seaborn as sns
# import seaborn as sns
# wrote script to pull 2024 data
MAX_PAGE = 40000
all_data = []
BASE_URL = "https://api.eia.gov/v2/seriesid/"
params = {
     "api_key": API_KEY,
    "data": DATA_SET,
    "facets[respondent][]": "CAL",   # 👈 Use "CAL" for CAISO; change if needed
    "offset": 0,
    "frequency": "D"
}
while True:
    try:
        response = rq.get(BASE_URL, params=params)
        data = response.json()
        data = data['response']['data']
        if not data:
            break
        all_data.extend(data)
    except Exception as e:
        print(e)
        break
    params['offset'] += 5000
records = data['response']['data']
# print(records)

df = pd.DataFrame(records)
print(df)
df.to_csv("daily_power.csv")

# df.to_csv("ignore/outage_data.csv", index=False)
# print(df)
# df.head()

df['period'] = pd.to_datetime(df['period'], errors="coerce")

plt.title("Hourly Electric Demand")

plt.xlabel("Period")
plt.ylabel("Value (MW)")

plt.plot(df["period"], df['value'])
plt.show()

plt.title("Electric Grid")
df['period'] = pd.to_datetime(df['period'], errors='coerce')
df = df.dropna(subset=['period'])  # Drop bad rows
df = df[df['value'].notnull()]

df['hour'] = df['period'].dt.hour
hourly_avg = df.groupby('hour')['value'].mean().reset_index()

# Plot
plt.figure(figsize=(10, 5))
plt.plot(hourly_avg['hour'], hourly_avg['value'], marker='o')
plt.title("Average Electricity Demand by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Average MW")
plt.grid(True)
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()

plt.xlabel("Period")
plt.ylabel("Value (MW)")

plt.plot(df["period"], df['value'])
plt.show()

# Average demand by day, accurate demand throughout day, 
# look at the average of each day where the hour is 17, compare last 24 hours to the
# last year
# standard deviation, how far away is it from the mean, if it is outside range of standard deviation
# then it is an outlier and should be looked at, look at points past 24 hours that could be off
# standard deviation
# look at more libraries