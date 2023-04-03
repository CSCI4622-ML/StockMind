import os
import pandas as pd

script_path = os.path.dirname(os.path.abspath(__file__))

files = os.listdir(f'{script_path}/market_data/TechIndicators')
os.makedirs(f'{script_path}/market_data/merged_data', exist_ok=True)

for filename in files:
    company = os.path.splitext(filename)[0]

    techindicators_path = os.path.join(f'{script_path}/market_data/TechIndicators', f'{company}.csv')
    timeseries_path = os.path.join(f'{script_path}/market_data/TimeSeries', f'{company}.csv')
    techindicators_df = pd.read_csv(techindicators_path)
    timeseries_df = pd.read_csv(timeseries_path)
    merged_df = pd.merge(techindicators_df, timeseries_df, on='date')
    output_path = os.path.join(f'{script_path}/market_data/merged_data', f'{company}.csv')
    merged_df.to_csv(output_path, index=False)
