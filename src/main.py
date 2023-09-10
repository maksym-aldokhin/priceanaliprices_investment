import sys
from argparse import ArgumentParser
import datetime
import time

from search_articles import search_articles
from download_articles import download_articles
from article_rank import calculate_articles_rank
from publisher_rank import calculate_publisher_rank

class Options:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--company", help="list of company ", type=str)
        parser.add_argument("--start", help="start date. format: %m/%d/%Y", type=str)
        parser.add_argument("--end", help="end date. format: %m/%d/%Y", type=str)
        parsed = parser.parse_args()

        if not (',' in parsed.company):
            print("format of string: '", parsed.company, "' not currect. Example: 'company1,company2,'")
            sys.exit()

        self.company = parsed.company.split(',')
        self.start_date = datetime.datetime.strptime(parsed.start, "%m/%d/%Y")
        self.end_date = datetime.datetime.strptime(parsed.end, "%m/%d/%Y")


def main():
    options = Options()

    print("input company: ", options.company)

    # date = datetime.datetime(2022, 12, 13)
    # while date < datetime.datetime(2022, 12, 14):
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
            download_articles(a)
            last_download = datetime.datetime.now()
        date = date + datetime.timedelta(days=1)

    # calculate_articles_rank()
    # calculate_publisher_rank()


if __name__ == "__main__":
    sys.exit(main())
