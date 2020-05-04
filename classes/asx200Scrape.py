import bs4 as bs
import pickle
import requests
import datetime as dt
from datetime import datetime
import os
import pandas as pd
import pandas_datareader.data as web


def save_asx200_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/S%26P/ASX_200')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    
    with open("asx200tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    
    return tickers


def get_data_from_yahoo(reload_asx200=False):
    if reload_asx200:
        tickers = save_asx200_tickers()

    else:
        with open("asx200tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.datetime(2000, 1, 1)
    end = datetime.now()
    
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            # df = web.get_data_yahoo([ticker], start=start, end=end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))


