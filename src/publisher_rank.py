import sys
import os
import json
from argparse import ArgumentParser


class Options:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--path", help="path to storage", type=str)
        parsed = parser.parse_args()

        self.path_to_storage = parsed.path


publisher_1_class = ['forbes', 'bloomberg', 'cnn', 'times', 'cnbc', 'businessinsider', 'linkedin', 'msn', 'bbc', 'cbs', 'nbc']
publisher_2_class = ['foxnews', 'post', 'yahoo', 'people', 'washingtonpost', 'dailymail', 'usatoday', 'espn']
publisher_3_class = ['reuters', 'politico', 'the-sun', 'buzzfeed', 'apnews', 'wsj', 'theguardian', 'npr']


def calculate_rank(publisher : str) -> int:
    publisher = publisher.lower()

    for p in publisher_1_class:
        if p in publisher:
            return 5
    for p in publisher_2_class:
        if p in publisher:
            return 3
    for p in publisher_3_class:
        if p in publisher:
            return 2
    return 1


def read_write_and_calulate(path : str):
    path = path + "/meta.json"
    if not os.path.exists(path):
        return
    with open(path, "r+", encoding='utf-8') as f:
        articles = json.load(f)

        for i in range(len(articles)):
            articles[i]["publisher_rank"] = calculate_rank(articles[i]["publisher"])

        f.seek(0)
        json.dump(articles, f, indent=4)
        f.truncate()


def calculate_publisher_rank(options):
    path = options.path_to_storage

    for company_path in os.listdir(path):
        company_path = path + company_path
        if os.path.isfile(company_path):
            continue
        for date_path in os.listdir(company_path):
            date_path = company_path + "/" + date_path
            if os.path.isfile(date_path):
                continue
            print("start: " + date_path)
            read_write_and_calulate(date_path)
            print("finish: " + date_path)

def main():
    options = Options()

    calculate_publisher_rank(options)


if __name__ == "__main__":
    sys.exit(main())