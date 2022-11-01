import pandas as pd
import yfinance as yf
import pyarrow.feather as feather
import datetime
import requests
import io
import os

file_path = './stock_data/input'


# Definition of get_stonks_data function for last 5 years


def get_stonks_data(get_stonks, year=2017, month=1, day=1):
    if year < 2017:
        return 'Please choose a date after 2016.12.31.'
    start = datetime.datetime(year=year, month=month, day=day)
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
    # iterate over each symbol
    for i in Symbols:
        try:
            # download the stock price
            stock = yf.download(i, start=start, end=end, progress=False)

            # append the individual stock prices
            if len(stock) == 0:
                print('No Data')
            else:
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                stock['Name'] = i
                stock.to_csv('./stock_data/input/{}.csv'.format(i))
                feather.write_feather(stock, './stock_data/input/{}.ftr'.format(i))
        except Exception:
            print('Problem', Exception)


print(get_stonks_data(['TSLA', 'AAME'], 2017))
