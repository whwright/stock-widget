#!/usr/bin/env python3

"""
usage: get_stock_price.py [SYMBOL]

Get stock information for a given symbol. Writes '[stock price] [percent change]'
to standard out.
"""

import argparse
import os
import requests
import sys


def main():
    parser = argparse.ArgumentParser(description='Get current stock information for a given symbol')
    parser.add_argument('SYMBOL', type=str, help='Stock symbol to look up')
    args = parser.parse_args()
    lookup_stock(args.SYMBOL)


def lookup_stock(symbol):
    api_key_file = '/opt/stock-widget/alphavantage'
    if not os.path.isfile(api_key_file):
        print('- -')
        return

    with open(api_key_file, 'r') as f:
        api_key = f.read()

    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&interval=1min&apikey={}'.format(symbol, api_key))
    if not r.ok:
        print('Error looking up symbol {}'.format(symbol))
        sys.exit(1)

    j = r.json()
    time_series = j['Time Series (Daily)']
    for i, date_key in enumerate(sorted(time_series, reverse=True)):
        if i == 0:
            curr_price = float(time_series[date_key]['4. close'])
        elif i == 1:
            last_close = float(time_series[date_key]['4. close'])
        else:
            break

    price = round(curr_price, 2)
    percent_change = round(((curr_price - last_close) / last_close) * 100, 2)

    print('{price} {percent_change}'.format(price=price,
                                            percent_change=percent_change))


if __name__ == '__main__':
    main()
