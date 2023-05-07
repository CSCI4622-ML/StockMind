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
    # improve data reliability by acting as a user
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    res = requests.get(url, headers=headers)

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
        return 0, 0, 0

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

    # Check for good results
    if len(sentiment_scores) == 0:
        return 0, 0, 0

    relevance = relevant_sentences / len(body_sentences)
    relevance = np.log(relevance * 19 + 1) / np.log(10) # Apply log scaling
    relevance = max(min(relevance, 1), 0)
    sentiment = np.mean(sentiment_scores)
    effective_sentiment = sentiment * relevance

    return sentiment, relevance, effective_sentiment

def analyze_csv(symbol, name, limit=0):
    """
    Perform sentiment analysis on all articles in a CSV file given a company's symbol

    Args:
        - symbol (str): Stock symbol/ticker (e.g. AAPL)
        - name (str): Company name (e.g. Apple)
        - limit (int, optional): Maximum number of articles to analyze

    Returns:
        tuple[list, list, list, list]: (sentiment, relevance, effective_sentiment, timestamps)
    """
    df = pd.read_csv(f"./market_data/AlphaIntelligence/{symbol}.csv")

    sentiments = []
    relevances = []
    e_sentiments = []
    timestamps = []

    for i, url in enumerate(df['url']):
        if limit > 0 and i >= limit:
            break

        print(f"Analyzing {i + 1} / {limit if limit > 0 else len(df)}", end="\r")
        
        (sentiment, relevance, effective_sentiment) = sentiment_analysis(url, symbol, name)

        # Only append if we get valid results
        if isinstance(sentiment, float) and isinstance(relevance, float) and not np.isnan(sentiment):
            sentiments.append(sentiment)
            relevances.append(relevance)
            e_sentiments.append(effective_sentiment)
            timestamps.append(df['time_published'][i])

    # Clear final "analyzing" line
    print(" " * 25, end="\r")

    return relevances, sentiments, e_sentiments, timestamps

def analyze(text):
    """
    Perform sentiment analysis on text

    Args:
        - url (str): Text to analyze

    Returns:
        float: sentiment
    """

    return sid.polarity_scores(text)["compound"]
