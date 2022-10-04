import pandas as pd
import yfinance as yf
import datetime
import requests
import io


# Definition of get_stonks_data function for last 5 years
def get_stonks_data(get_stonks):
    start = datetime.datetime.today()
    start = start.replace(year=start.year - 5)
    end = datetime.datetime.today()

    url = "https://pkgstore.datahub.io/core/nasdaq-listings/nasdaq-listed_csv/data/7665719fb51081ba0bd834fde71ce822" \
          "/nasdaq-listed_csv.csv"
    s = requests.get(url).content
    companies = pd.read_csv(io.StringIO(s.decode('utf-8')))
    all_companies = companies['Company Name'].tolist()
    all_symbols = companies['Symbol'].tolist()
    tmp = zip(all_symbols, all_companies)
    combined_company_symbol = list(tmp)
    Symbols = get_stonks
    # create empty dataframe
    stock_final = pd.DataFrame()
    # iterate over each symbol
    for i in Symbols:

        try:
            # download the stock price
            stock = []
            stock = yf.download(i, start=start, end=end, progress=False)

            # append the individual stock prices
            if len(stock) == 0:
                None
            else:
                stock['Name'] = i
                stock_final = pd.concat([stock, stock_final])
        except Exception:
            None

    return stock_final


# print(get_stonks_data(['TSLA', 'AAME']))
