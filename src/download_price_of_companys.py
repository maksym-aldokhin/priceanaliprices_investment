import sys
import os
import datetime

import yfinance as yf

from argparse import ArgumentParser

from company_name_to_ticker import company_name_to_ticker

class Options:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--company", help="list of company ", type=str)
        parser.add_argument("--path", help="path to storage", type=str)
        parser.add_argument("--start", help="start date. format: %m/%d/%Y", type=str)
        parser.add_argument("--end", help="end date. format: %m/%d/%Y", type=str)
        parsed = parser.parse_args()

        if not (',' in parsed.company):
            self.company = [parsed.company]
        else:
            self.company = parsed.company.split(',')

        self.path_to_storage = parsed.path
        self.start_date = datetime.datetime.strptime(parsed.start, "%m/%d/%Y")
        self.end_date = datetime.datetime.strptime(parsed.end, "%m/%d/%Y")


def main():
    options = Options()

    print("input company: ", options.company)

    date_start = options.start_date.strftime("%Y-%m-%d")
    date_end = options.end_date.strftime("%Y-%m-%d")
    print(date_start)
    print(date_end)

    for company in options.company:
        if not company in company_name_to_ticker:
            continue
        ticker = company_name_to_ticker[company]

        data = yf.download(ticker, start=date_start, end=date_end, interval = "1d")

        # print(data.head())

        path_to_save = options.path_to_storage + company + ".xlsx"
        data.to_excel(path_to_save)


if __name__ == "__main__":
    sys.exit(main())