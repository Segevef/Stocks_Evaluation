from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
import sys


def get_yahoo_financial(ticker):
    financial_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '/financials?p=' + str(ticker)
    financal_source_code = requests.get(financial_url)
    plain_financial_text = financal_source_code.text
    soup = bs(plain_financial_text)
    table = soup.findAll('table', {'class': 'Lh(1.7) W(100%) M(0)'})
    df = pd.read_html(str(table))[0]
    df.set_index(0, inplace=True)
    df.columns = ['2017', '2016', '2015', '2014']
    # df.to_csv('ticker_df.csv')
    print(df)
    return df


def get_yahoo_description(ticker):
    desc_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '/profile?p=' + str(ticker)
    desc_source_code = requests.get(desc_url)
    plain_dec_text = desc_source_code.text
    soup = bs(plain_dec_text)
    p = soup.findAll('p', {'class': 'Mt(15px) Lh(1.6)'})
    p = p[0]
    print(p)


def yahoo_spider(ticker):
    ticker_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '?p=' + str(ticker)
    financial_df = get_yahoo_financial(ticker)



def finviz_spider(ticker):
    url = 'https://finviz.com/quote.ashx?t=' + str(ticker)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = bs(plain_text)
    graph_url = 'https://finviz.com/chart.ashx?t=' + str(ticker) + '&ty=c&ta=1&p=d&s=l'
    graph_data = requests.get(graph_url).content
    path = 'C:/Users/nimro/webscrape/crawler'
    file_name = str(ticker) + '_df.csv'

    if file_name in os.listdir(path):
        with os.open(file_name, 'w') as file:
            os.write(file, graph_data)

    else:
        x = str(ticker) + '_df.csv'
        with os.open(x, 'a') as file:
            os.write(file, graph_data)

    print(graph_data)


get_yahoo_description('TEVA')