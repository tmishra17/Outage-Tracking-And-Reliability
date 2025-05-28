from ignore.API_KEY import API_KEY, DATA_SET
import requests as rq
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import seaborn as sns

params = {
    "API_KEY": API_KEY,
    "DATA_SET": DATA_SET,
    "facets[respondent][]": "CAL",   # 👈 Use "CAL" for CAISO; change if needed
    "start": "2024-01-01",
    "end": "2024-12-31",
    "offset": 0
}
# use requests and call the api with these params
all_data_2024 = []
BASE_URL_2024 = "https://api.eia.gov/v2/electricity/rto/region-data/data/"


MAX_PAGE = 40000

params = {
    "api_key": API_KEY,
    "data": DATA_SET,
    "facets[respondent][]": "CAL",   # 👈 Use "CAL" for CAISO; change if needed
    "start": "2024-01-01",
    "end": "2024-12-31",
    "offset": 0
}
# use requests and call the api with these params
all_data_2024 = []
BASE_URL_2024 = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
# first get 2024 data to compare
while params["offset"] < MAX_PAGE:

    try:
        res_2024 = rq.get(BASE_URL_2024, params=params)
        print(res_2024.text)
        temp = res_2024.json()
        data_2024 = temp['response']['data']
        print(data_2024)
        all_data_2024.extend(data_2024)
        if not res_2024:
            break
    except Exception as e:
        print(e)
        break
    params["offset"] += 5000

# print(records)
print(len(all_data_2024))
df_2024 = pd.DataFrame(all_data_2024)
df_2024['period'] = pd.to_datetime(df_2024['period'], errors='coerce')
hour_17_2024 = df_2024[df_2024['period'].dt.hour == 17]
hour_17_2024.to_csv("2024_eia_power_data.csv")

# df.to_csv("ignore/outage_data.csv", index=False)
# print(df)
# df.head()

