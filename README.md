
<p style="text-align: center;">StockMind</p>


<p style="text-align: center;">Connor Davel, Peter McDevitt, Aidan Thiessen</p>

Instructions:

1) cd CSCI4622-ML (or whatever dir you are using)
2) git clone [https://github.com/CSCI4622-ML/alpha_vantage.git](https://github.com/CSCI4622-ML/alpha_vantage.git "https://github.com/CSCI4622-ML/alpha_vantage.git")
3) pip install -e alpha_vantage
4) git clone [https://github.com/CSCI4622-ML/ProjectCode.git](https://github.com/CSCI4622-ML/ProjectCode.git "https://github.com/CSCI4622-ML/ProjectCode.git")
5) cd ProjectCode/market_data
6) put your key in "alpha_vantage_key[template].py" and change the name
7) python setup.py # or just run however you do. Should take about 10 minutes or less to finish gathering the data
8) cd ..
9) python combine_TimeSeries_Techindicators.py
10) Train with NN.ipynb
