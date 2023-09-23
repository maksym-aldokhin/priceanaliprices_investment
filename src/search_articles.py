import requests
import pandas as pd
import datetime
import os
import time
import sys

from bs4 import BeautifulSoup

from argparse import ArgumentParser

def search_articles(topic : str, date) -> str:
    date_after_str = date.strftime('%Y-%m-%d')
    # print(date_after_str)
    date_before = date + datetime.timedelta(days=1)
    date_before_str = date_before.strftime('%Y-%m-%d')
    # print(date_after_str)

    url = "https://news.google.com/search"
    url += "?q=" + topic
    url += "+after:" + date_after_str
    url += "+before:" + date_before_str
    url += "&hl=en-US&gl=US&ceid=US:en"

    print(url)

    response = requests.get(url)

    path_to_dir = os.getcwd() + "/temp/" + topic

    if not os.path.exists(path_to_dir):
        os.makedirs(path_to_dir)

    path_to_file = path_to_dir + "/" + date_after_str + ".html"
    with open(path_to_file, "wb") as htmlFile:
        htmlFile.write(response.content)
        print('Download completed.')

    return path_to_file


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

    last_download = datetime.datetime(2000, 1, 1)
    date = options.start_date
    while date <= options.end_date:
        for company in options.company:
            if datetime.datetime.now() - last_download < datetime.timedelta(seconds=1):
                time.sleep(1)
            try:
                a = search_articles(company, date)
            except:
                time.sleep(10)
                a = search_articles(company, date)
            last_download = datetime.datetime.now()
        date = date + datetime.timedelta(days=1)


if __name__ == "__main__":
    sys.exit(main())
