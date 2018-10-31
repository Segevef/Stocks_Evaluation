from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import os
import xlsxwriter
import time


def get_yahoo_financial(ticker):
    '''
    input: ticker name(string)
    output: yahoo financial table for ticker
    '''
    financial_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '/financials?p=' + str(ticker)
    financal_source_code = requests.get(financial_url)
    plain_financial_text = financal_source_code.text
    soup = bs(plain_financial_text, "html.parser")
    table = soup.findAll('table', {'class': 'Lh(1.7) W(100%) M(0)'})
    df = pd.read_html(str(table))[0]
    df.set_index(0, inplace=True)
    df.columns = ['2017', '2016', '2015', '2014']
    # df.to_csv('ticker_df.csv')
    return df


def get_yahoo_description(ticker):
    '''
    input: ticker name(string)
    output: yahoo description for ticker
    '''
    desc_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '/profile?p=' + str(ticker)
    desc_source_code = requests.get(desc_url)
    plain_dec_text = desc_source_code.text
    soup = bs(plain_dec_text, "html.parser")
    p = soup.findAll('p', {'class': 'Mt(15px) Lh(1.6)'})
    p = str(p[0])
    p = p.split('>')[1].split('</p>')[0]
    return p


def get_yahoo_analysis(ticker):
    '''
    input: ticker name(string)
    output: yahoo analysis table for ticker
    '''
    analysis_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '/analysis?p=' + str(ticker)
    analysis_source_code = requests.get(analysis_url)
    plain_analysis_text = analysis_source_code.text
    soup = bs(plain_analysis_text, "html.parser")
    analysis_df = soup.findAll('section', {'class': 'smartphone_Px(20px) smartphone_Mt(10px)'})
    analysis_df = pd.read_html(str(analysis_df))
    df = pd.concat(analysis_df)
    return df


def get_yahoo_holders(ticker):
    '''
    input: ticker name(string)
    output: yahoo holders table for ticker
    '''
    holders_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '/holders?p=' + str(ticker)
    holders_source_code = requests.get(holders_url)
    plain_holders_text = holders_source_code.text
    soup = bs(plain_holders_text, "html.parser")
    table = soup.find('table', {'class': 'W(100%) M(0) BdB Bdc($c-fuji-grey-c)'})
    holders_df = pd.read_html(str(table))
    return holders_df[0]


def yahoo_spider(ticker):
    '''
    input: ticker name(string)
    output: all yahoo relevant data for ticker
    '''
    data = dict()
    ticker_url = 'https://finance.yahoo.com/quote/' + str(ticker) + '?p=' + str(ticker)
    data['financial_df'] = get_yahoo_financial(ticker)
    data['description'] = get_yahoo_description(ticker)
    data['analysis'] = get_yahoo_analysis(ticker)
    data['holders'] = get_yahoo_holders(ticker)
    return data


def seprate_finviz_table(df, ticker):
    d = []
    tup = list(zip(['symbol'], [ticker]))
    d.extend(tup)
    for i in range(2, len(df.columns) + 1, 2):
        j = i - 2
        x = list(zip(df[j], df[i-1]))
        d.extend(x)

    d = dict(d)
    return d


def get_finviz_table(ticker):
    '''
    input: ticker name(string)
    output: finviz financial table for ticker
    '''
    url = 'https://finviz.com/quote.ashx?t=' + str(ticker)
    s = requests.Session()
    s.proxies = {"http": "http://61.233.25.166:80"}
    source_code = s.get(url)
    # source_code = requests.get(url)
    plain_text = source_code.text
    soup = bs(plain_text, "html.parser")
    table = soup.find('table', {'class': 'snapshot-table2'})
    finviz_df = pd.read_html(str(table))
    finviz_df = finviz_df[0]

    return finviz_df


def get_finviz_estimates(ticker):
    '''
    input: ticker name(string)
    output: finviz estimates report for ticker. past results of the company
    '''
    url = 'https://www.reuters.com/finance/stocks/analyst/' + str(ticker)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = bs(plain_text, "html.parser")
    div = soup.find('div', {'class': 'column1 gridPanel grid8'})
    estimates = pd.read_html(str(div))
    # df = pd.concat(estimates)
    # for table in estimates:
    #     columns = table.iloc[0]
    #     table.drop([0], inplace=True)
    #     table.set_index(0, inplace=True)
    #     name = columns[0]
    #     table.columns = columns[1:]
    #     # table.dropna(how='all', inplace=True)

    return estimates


def reverse_list(l):
    return list(reversed(l))


def get_estimates_graph(estimates):
    headers = estimates[3].iloc[0]
    estimates[3].columns = headers
    sales = estimates[3][1:6]
    sales_actual = sales['Actual']
    sales_estimate = sales['Estimate']
    earning = estimates[3][6:]
    x = sales.index.tolist()
    print(x)
    for i in range(0, len(x)):
        date = x[i]#.split('\xa0')[1]
        x[i] = date
    x = reverse_list(x)

    plt.plot(x, sales_actual, 'o')
    plt.plot(x, sales_estimate, 'o', color='r')
    plt.show()


def get_finviz_statements(ticker):
    return


def get_industry_url(ticker):
    url = 'https://finviz.com/quote.ashx?t=' + str(ticker)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = bs(plain_text, "html.parser")
    industry = soup.findAll('td', {'class': 'fullview-links'})[1]
    soup = bs(str(industry), "html.parser")
    industry = str(soup.findAll('a')[1])
    industry = industry.split('&amp;f=')[1].split('">')[0]

    industry = 'https://finviz.com/screener.ashx?v=111&f=' + industry

    return str(industry)


def get_competition_list(ticker):
    url = get_industry_url(ticker)
    source = requests.get(url).text
    soup = bs(source, "html.parser")
    competition_list = soup.findAll('div', {'id': 'screener-content'})
    # soup = bs(str(competition_list))
    competition_list = pd.read_html(str(competition_list))
    competition_df = competition_list[3]
    columns = competition_df.iloc[0].tolist()
    competition_df.drop([0], inplace=True)
    competition_df.set_index(0, inplace=True)
    competition_df.columns = columns[1:]

    return competition_df['Ticker']


def finviz_spider(ticker):
    data = dict()
    data['df'] = get_finviz_table(ticker)
    data['estimates'] = get_finviz_estimates(ticker)
    return data


def get_finviz_graph(ticker):
    url = 'https://finviz.com/chart.ashx?t=' + str(ticker) + '&ty=c&ta=1&p=d&s=l'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    print(img)
    return img


def analyze_ticker(ticker):
    stock = dict()
    stock['description'] = get_yahoo_description(ticker)
    stock['financial'] = get_yahoo_financial(ticker)
    stock['analysis'] = get_yahoo_analysis(ticker)
    stock['holders'] = get_yahoo_holders(ticker)
    estimates = get_finviz_estimates(ticker)
    stock['estimates'] = pd.concat(estimates)
    finviz_df = get_finviz_table(ticker)
    stock['finviz_table'] = seprate_finviz_table(finviz_df, ticker)

    return stock


def evaluate_competitors(ticker):
    industry = {}
    competitors_list = get_competition_list(ticker)
    finviz_keys = ['Index', 'Market Cap', 'Income', 'Sales', 'Book/sh', 'Cash/sh', 'Dividend', 'Dividend %',
                   'Employees', 'Optionable', 'Shortable', 'Recom', 'P/E', 'Forward P/E', 'PEG', 'P/S', 'P/B', 'P/C',
                   'P/FCF', 'Quick Ratio', 'Current Ratio', 'Debt/Eq', 'LT Debt/Eq', 'SMA20', 'EPS (ttm)', 'EPS next Y',
                   'EPS next Q', 'EPS this Y', 'EPS next Y', 'EPS next 5Y', 'EPS past 5Y', 'Sales past 5Y', 'Sales Q/Q',
                   'EPS Q/Q', 'Earnings', 'SMA50', 'Insider Own', 'Insider Trans', 'Inst Own', 'Inst Trans', 'ROA',
                   'ROE', 'ROI', 'Gross Margin', 'Oper. Margin', 'Profit Margin', 'Payout', 'SMA200', 'Shs Outstand',
                   'Shs Float', 'Short Float', 'Short Ratio', 'Target Price', '52W Range', '52W High', '52W Low',
                   'RSI (14)', 'Rel Volume', 'Avg Volume', 'Volume', 'Perf Week', 'Perf Month', 'Perf Quarter',
                   'Perf Half Y', 'Perf Year', 'Perf YTD', 'Beta', 'ATR', 'Volatility', 'Prev Close', 'Price', 'Change']
    df = pd.DataFrame(index=competitors_list, columns=finviz_keys)
    for ticker in competitors_list:
        stock = get_finviz_table(ticker)
        stock = seprate_finviz_table(stock, ticker)
        for key in stock.keys():
            value = stock[key]
            df.loc[ticker, key] = value
        industry[ticker] = stock

    return df


def export_to_xls(industry, ticker):
    path = 'C:/Users/nimro/webscrape/crawler/venv'
    current_date = time.strftime("%d-%m-%Y")
    file_name = ticker + '_' + 'evaluation' + '_' + current_date + '.xlsx'
    full_path = os.path.join(path, file_name)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    industry.drop(['Index'], inplace=True, axis=1)
    industry.to_excel(writer, sheet_name='data')
    writer.save()





# ticker = 'AMX'
# analyze_ticker(ticker)
# industry = evaluate_competitors(ticker)
# stock = get_finviz_table(ticker)
# export_to_xls(industry, ticker)


x = get_finviz_estimates('AMX')
get_estimates_graph(x)