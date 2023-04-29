import re
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer



# NOTE: Uncomment this line the first time you run
# nltk.download('vader_lexicon')
# nltk.download('punkt')


#symbols = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'PCAR', 'TSLA', 'NVDA', 'V', 'TSM', 'UNH']
#names = ['Apple', 'Microsoft', 'Google', 'Google', 'Amazon', 'Paccar', 'Tesla', 'Nvidia', 'Visa', 'Taiwan Semiconductor', 'UnitedHealth']


sid = SentimentIntensityAnalyzer()

def sentiment_analysis(url, symbol, name):
    """
    Perform sentiment analysis on given url

    Args:
        - url (str): URL to analyze
        - symbol (str): Stock symbol/ticker (e.g. AAPL)
        - name (str): Company name (e.g. Apple)

    Returns:
        tuple[float, float, float]: (sentiment, relevance, effective_sentiment)
    """
    res = requests.get(url)

    # Parse html
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    sentences = nltk.sent_tokenize(text)

    # Match sentence structure
    body_regex = r"[A-Z0-9][^.!?]*[.!?]"

    body_sentences = []
    for sentence in sentences:
        if re.match(body_regex, sentence) and sentence.count('\n') <= 1:
            body_sentences.append(sentence)

    if len(body_sentences) == 0:
        return (None, None, None)

    # Clean text
    body_text = " ".join(body_sentences)
    body_text = body_text.replace("\n", " ")

    # Relevance & Sentiment analysis
    sentiment_scores = []
    relevance_scores = []
    relevant_sentences = 0
    discount = 0.5

    for i, sentence in enumerate(body_sentences):
        sentence = sentence.strip("\n")

        # Relevance
        relevant = False
        relevance = 0
        length = len(sentence.split())

        if length == 0:
            continue

        if max(sentence.count(symbol), sentence.count(name)) > 0:
            relevant = True

        if relevant:
            relevance = 1 / (length * discount)

        relevance = min(max(relevance, 0), 1) # Maximum of 1, minimum of 0
        relevance_scores.append(relevance)
        

        # Sentiment
        sentiment = sid.polarity_scores(sentence)["compound"]
        if relevance > 0:
            sentiment_scores.append(sentiment)
            relevant_sentences += 1

        #print(sentence)
        #print("SENTIMENT:", sentiment)
        #print("RELEVANCE:", relevance)
        #print()

    if len(sentiment_scores) == 0:
        return (None, None, None)

    relevance = relevant_sentences / len(body_sentences)
    relevance = np.log(relevance * 19 + 1) / np.log(10) # Apply log scaling
    relevance = max(min(relevance, 1), 0)
    sentiment = np.mean(sentiment_scores)
    effective_sentiment = sentiment * relevance

    return (sentiment, relevance, effective_sentiment)

# Example
# sentiment, relevance, effective_sentiment = sentiment_analysis("https://www.fool.com/investing/how-to-invest/stocks/how-to-invest-in-apple-stock/", "AAPL", "Apple")
# print("Overall relevance:", relevance)
# print("Overall sentiment:", sentiment)
# print("Effective sentiment:", effective_sentiment)

def analyze_csv(symbol, name):
    df = pd.read_csv(f"./market_data/AlphaIntelligence/{symbol}.csv")

    sentiments = []
    relevances = []
    e_sentiments = []

    for i, url in enumerate(df['url']):
        # Limit amount of articles
        # if i >= 50:
        #     break

        # print(f"Analyzing {i + 1}: {url}", end="\r", flush=True)
        
        (sentiment, relevance, effective_sentiment) = sentiment_analysis(url, symbol, name)

        if isinstance(sentiment, float) and isinstance(relevance, float) and not np.isnan(sentiment):
            sentiments.append(sentiment)
            relevances.append(relevance)
            e_sentiments.append(effective_sentiment)
        
    # print()
    # print("Overall relevance:", np.mean(relevances))
    # print("Overall sentiment:", np.mean(sentiments))
    # print("Effective sentiment:", np.mean(e_sentiments))

analyze_csv("AAPL", "Apple")