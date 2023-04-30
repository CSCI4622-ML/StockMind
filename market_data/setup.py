import sys
import os
from pathlib import Path
import alpha_vantage
import pandas as pd
import numpy as np
from alpha_vantage_key import *
import time
import json
import csv

# hande the data setup in parallel file structure will be as below:
# FILE STRUCTURE
#/market_data
#   /TimeSeries
#       <symbol1>.csv
#       <symbol2>.csv
#       ...
#   /TechIndicators
#       <symbol1>.csv
#       <symbol2>.csv
#   /AlphaIntelligence
#       <symbol1>.csv
#       <symbol2>.csv

def output_query(data, file_location, replace_existing=False):
    file = Path(file_location)
    if file.exists() and file.is_file():
        if replace_existing:
            print(f"replacing {file_location} with updated data")
        else:
            print(f"{file_location} already exists. specify \"replace_existing=True\" to replace")
            return
    else:
        print(f"making new file {file_location}")
        file.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(data, pd.DataFrame):
        data.to_csv(file, sep=',', header=True)
    elif isinstance(data, dict):
        json_object = json.dumps(data, indent=4)
        with open(file_location, "w") as outfile:
            outfile.write(json_object)
    # else:
    #     with open(file_location, "w") as outfile:
    #         for row in data:
    #             outfile.write("".join(row))
    #             outfile.write("\n")
    return

# limit the speed of the querying if necessary
ALPHA_VANTAGE_QUERY_LAST_TIME = time.time()
ALPHA_VANTAGE_QUERY_LIMIT = 60 / 150 # seconds per query allowed 
def query_limit():
    # slow the query speed to meet the 150 queries per minute limit
    time_since_last_query = time.time() - ALPHA_VANTAGE_QUERY_LAST_TIME
    if time_since_last_query < ALPHA_VANTAGE_QUERY_LIMIT:
        print(f"waiting {ALPHA_VANTAGE_QUERY_LIMIT - time_since_last_query} seconds before next query")
        time.sleep(ALPHA_VANTAGE_QUERY_LIMIT - time_since_last_query)


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname) # change location to setup file's directory

# symbols that will be used when querying all data
symbols = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'PCAR', 'TSLA', 'NVDA', 'V', 'TSM', 'UNH']
"""
#------------------TIME SERIES DATA-----------------------
output_dir = "TimeSeries"
for sym in symbols:
    output_file = Path(output_dir) / f"{sym}.csv"
    ts = alpha_vantage.timeseries.TimeSeries(key=ALPHA_VANTAGE_KEY, output_format='pandas')
    query_limit()
    data, meta_data = ts.get_daily_adjusted(symbol=sym, outputsize='full')
    output_query(data, output_file, replace_existing=True)

#------------------TECH INDICATOR DATA-----------------------
output_dir = "TechIndicators"
indicator_functions = [
                        ("get_ad", [], {}),
                        ("get_adosc", [], {}),
                        ("get_adx", [], {}),
                        ("get_adxr", [], {}),
                        ("get_apo", [], {}),
                        ("get_aroon", [], {}),
                        ("get_aroonosc", [], {}),
                        ("get_atr", [], {}),
                        ("get_bbands", [], {}),
                        ("get_bop", [], {}),
                        ("get_cci", [], {}),
                        ("get_cmo", [], {}),
                        ("get_dema", [], {}),
                        ("get_dx", [], {}),
                        ("get_ema", [], {}),
                        ("get_ht_dcperiod", [], {}),
                        ("get_ht_dcphase", [], {}),
                        ("get_ht_phasor", [], {}),
                        ("get_ht_sine", [], {}),
                        ("get_ht_trendline", [], {}),
                        ("get_ht_trendmode", [], {}),
                        ("get_kama", [], {}),
                        ("get_macd", [], {}),
                        ("get_macdext", [], {}),
                        ("get_mama", [], {}),
                        ("get_mfi", [], {}),
                        ("get_midpoint", [], {}),
                        ("get_midprice", [], {}),
                        ("get_minus_di", [], {}),
                        ("get_minus_dm", [], {}),
                        ("get_mom", [], {}),
                        ("get_natr", [], {}),
                        ("get_obv", [], {}),
                        ("get_plus_di", [], {}),
                        ("get_plus_dm", [], {}),
                        ("get_ppo", [], {}),
                        ("get_roc", [], {}),
                        ("get_rocr", [], {}),
                        ("get_rsi", [], {}),
                        ("get_sar", [], {}),
                        ("get_sma", [], {}),
                        ("get_stoch", [], {}),
                        ("get_stochf", [], {}),
                        ("get_stochrsi", [], {}),
                        ("get_t3", [], {}),
                        ("get_tema", [], {}),
                        ("get_trange", [], {}),
                        ("get_trima", [], {}),
                        ("get_trix", [], {}),
                        ("get_ultosc", [], {}),
                        ("get_willr", [], {}),
                        ("get_wma", [], {})
                        ]
for sym in symbols:
    output_file = Path(output_dir) / f"{sym}.csv"
    ts = alpha_vantage.TechIndicators(key=ALPHA_VANTAGE_KEY, output_format='pandas')
    data = pd.DataFrame()
    for fun_string, args, kwargs in indicator_functions:
        fun = getattr(ts, fun_string)
        query_limit()
        query, meta_data = fun(sym, *args, **kwargs)
        data = pd.concat([data, query], axis=1, join='outer')
    data.dropna(inplace=True)
    output_query(data, output_file, replace_existing=True)
"""

#------------------SENTIMENT ANALYSIS  DATA-----------------------

output_dir = "AlphaIntelligence"
symbols = ["AAPL"] # Limited to reduce testing time

num_articles = 30
num_months = 15
starting_month = 2 # Feb
day_of_month = "01"

for sym in symbols:
    output_file = Path(output_dir) / f"{sym}.csv"
    ts = alpha_vantage.AlphaIntelligence(key=ALPHA_VANTAGE_KEY, output_format='pandas', indexing_type='integer')
    data, meta_data = None, None
    print(sym)

    for i in range(num_months):
        start_year = "{}".format(2022 + (i + starting_month - 1) // 12)
        start_month = "{:02d}".format((i + starting_month - 1) % 12 + 1)

        end_year = "{}".format(2022 + (i + starting_month) // 12)
        end_month = "{:02d}".format((i  + starting_month) % 12 + 1)
            
        time_from = start_year + start_month + day_of_month + "T0000"
        time_to = end_year + end_month + day_of_month + "T0000"

        print(i, "=> From:", time_from, "- To:", time_to)

        query_limit()
        try:
            cur_data, cur_meta_data = ts.get_news(symbol=sym, time_from=time_from, time_to=time_to, limit=num_articles, sort="RELEVANCE")

            cur_data['index'] = [ind + num_articles*i for ind in cur_data['index']]
            cur_data.index = [ind + num_articles*i for ind in cur_data.index]

            if (data is None):
                data = cur_data
                meta_data = cur_meta_data
            else:
                data = pd.concat([data, cur_data])
        except:
            print("No articles found")
    
    output_query(data, output_file, replace_existing=True)