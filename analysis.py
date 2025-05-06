from API_KEY import API_KEY, DATA_SET
import requests as rq
import json
import pandas as pd
import matplotlib.pyplot as plt

try:
    url = f"https://api.eia.gov/v2/seriesid/{DATA_SET}?api_key={API_KEY}"
    response = rq.get(url)

    data = response.json()
    with open("response.json", "w") as rs:
        json.dump(data, rs, indent=4)

except Exception as e:
    print(e)

records = data['response']['data']
print(records[0].keys())

df = pd.DataFrame(records)
# print(df)
df.head()

plt.xticks(rotation=45, ha='right')
plt.figure(figsize=(12, 5))
plt.bar(df['period'], df['price'], label='Demand (MW)', color='blue')
plt.title('Hourly Electricity Demand')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()