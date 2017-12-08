#!/usr/bin/env python3

"""
usage: get_stock_price.py [SYMBOL]

Get stock information for a given symbol. Writes '[stock price] [percent change]'
to standard out.
"""

import argparse
import json
import os
import requests
import sys
from datetime import datetime, timedelta


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
        api_key = f.read

    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&interval=1min&apikey={}'.format(symbol, api_key))
    if not r.ok:
        print('Error looking up symbol {}'.format(symbol))
        sys.exit(1)

    j = r.json()
    last_refreshed = j['Meta Data']['3. Last Refreshed']
    last_refreshed = datetime.strptime(last_refreshed, '%Y-%m-%d %H:%M:%S')

    today = last_refreshed.strftime('%Y-%m-%d')
    yesterday = (last_refreshed - timedelta(days=1)).strftime('%Y-%m-%d')

    curr_price = float(j['Time Series (Daily)'][today]['4. close'])
    yesterday_close = float(j['Time Series (Daily)'][yesterday]['4. close'])

    price = round(curr_price, 2)
    percent_change = round(((curr_price - yesterday_close) / yesterday_close) * 100, 2)

    print('{price} {percent_change}'.format(price=price,
                                            percent_change=percent_change))


if __name__ == '__main__':
    main()
