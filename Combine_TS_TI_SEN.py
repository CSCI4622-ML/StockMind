import os
import pandas as pd

script_path = os.getcwd()

files = os.listdir(f'{script_path}/market_data/TechIndicators')
os.makedirs(f'{script_path}/market_data/full_data', exist_ok=True)

for filename in files:
    company = os.path.splitext(filename)[0]

    techindicators_path = os.path.join(f'{script_path}/market_data/TechIndicators', f'{company}.csv')
    timeseries_path = os.path.join(f'{script_path}/market_data/TimeSeries', f'{company}.csv')
    news_path = os.path.join(f'{script_path}/market_data/AlphaIntelligence', f'{company}.csv')
    techindicators_df = pd.read_csv(techindicators_path)
    techindicators_df['date'] = pd.to_datetime(techindicators_df['date']).dt.date
    timeseries_df = pd.read_csv(timeseries_path)
    timeseries_df['date'] = pd.to_datetime(timeseries_df['date']).dt.date
    news_df = pd.read_csv(news_path)
    news_df['date'] = pd.to_datetime(news_df['date']).dt.date
    merged_df = pd.merge(techindicators_df, timeseries_df, on='date')
    merged_df = pd.merge(merged_df, news_df, on='date')
    output_path = os.path.join(f'{script_path}/market_data/full_data', f'{company}.csv')
    merged_df.to_csv(output_path, index=False)
