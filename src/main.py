import sys
from argparse import ArgumentParser
import datetime
import time
import os

from concurrent import futures

from random import shuffle

from search_articles import search_articles
from download_articles import download_articles
from article_rank import calculate_articles_rank
# from publisher_rank import calculate_publisher_rank
from split_array import splitting_array

from find_path_to_article import find_path_to_article
class Options:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--company", help="list of company ", type=str)
        parser.add_argument("--path", help="path to storage", type=str)
        parsed = parser.parse_args()

        if not (',' in parsed.company):
            self.company = [parsed.company]
        else:
            self.company = parsed.company.split(',')

        self.path_to_storage = parsed.path


def download_for_date_set(paths):
    # print("thread:", number_of_thread, "len:", len(paths))
    for path in paths:
        # print("start: " + path, " - ", number_of_thread / len(paths), "thread:", number_of_thread)
        download_articles(path)
        # print("finish: " + path, " - ", number_of_thread / len(paths), "thread:", number_of_thread)


def main():
    options = Options()

    print("input company: ", options.company)

    date = datetime.datetime(2000, 1, 1)
    while date < datetime.datetime(2023, 9, 10):
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
        date = date + datetime.timedelta(days=1)3
    n_cores = 24

    # for company_path in os.listdir(options.path_to_storage):
    #     if not company_path in options.company:
    #         continue

    #     company_path = options.path_to_storage + company_path

        # pathes_all = []
        # for date_path in os.listdir(company_path):
        #     date_path = company_path + "/" + date_path
        #     if not os.path.isfile(date_path):
        #         continue
        #     pathes_all.append(date_path)

        # shuffle(pathes_all)

        # pathes_set = splitting_array(pathes_all, n_cores)

        # with futures.ProcessPoolExecutor(n_cores) as executor:
        #     to_do = []
        #     for pathes in pathes_set:
        #         future_to_do = executor.submit(download_for_date_set, pathes)
        #         to_do.append(future_to_do)

        #     for future in futures.as_completed(to_do):
        #         future.result()
        #         if not future.done():
        #             print("Finished with failed!")
                # i += 1
                # print("finished: ", i/count_date * 100, "%")

        # for date_path in os.listdir(company_path):
        #     date_path = company_path + "/" + date_path
        #     if os.path.isfile(date_path):
        #         print(date_path)
        #         download_articles(date_path)

    calculate_articles_rank(options)
    # calculate_publisher_rank(options)

    # find_path_to_article(options)


if __name__ == "__main__":
    sys.exit(main())
