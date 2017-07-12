#!/usr/bin/env python3

"""
usage: get_stock_price.py [SYMBOL]

Get stock information for a given symbol. Writes '[stock price] [percent change]'
to standard out.
"""

import argparse
import requests
import sys
import json


def main():
    parser = argparse.ArgumentParser(description='Get current stock information for a given symbol')
    parser.add_argument('SYMBOL', type=str, help='Stock symbol to look up')
    args = parser.parse_args()
    lookup_stock(args.SYMBOL)


def lookup_stock(symbol):
    r = requests.get('https://www.google.com/finance/info?q={}'.format(symbol))
    if not r.ok:
        print('Error looking up symbol {}'.format(symbol))
        sys.exit(1)

    # response starts with a comment, so strip that off
    text = r.text.strip().replace('//', '')
    stock_info = json.loads(text)[0]  # should be an array of length 0

    print('{price} {percent_change}'.format(price=stock_info['l'], percent_change=stock_info['cp']))


if __name__ == '__main__':
    main()
