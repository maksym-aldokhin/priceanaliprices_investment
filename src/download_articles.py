# import xml.sax
# import xml.sax.saxutils
from lxml import etree
import requests
import datetime
import os
import json
from concurrent import futures
# from dateutil import parser
import sys
from argparse import ArgumentParser

g_class_article_name = "NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"
g_class_publisher_name = "wEwyrc"
g_class_title_name = "DY5T1d RZIKme"
g_class_date_name = "WW6dff uQIVzc Sksgp slhocf"

class Article:
    def __init__(self, title : str, url : str, publisher : str, index : int, date : str):
        self._title = title
        self._url = url
        self._publisher = publisher
        self._index = index

        date_parsed = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

        self._date = date_parsed

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def publisher(self) -> str:
        return self._publisher

    @property
    def index(self) -> int:
        return self._index

    @property
    def date(self) -> str:
        return self._date


class ArticleSet:
    def __init__(self):
        self._articles = list()

    def add_article(self, a):
        self._articles.append(a)

    def update_article(self, title, a):
        for i in range(len(self._articles)):
            if self._articles[i].title == title:
                self._articles[i] = a

    def remove_article(self, title):
        i = 0
        for a in self._articles:
            if a.title == title:
                del self._articles[i]
                return
            i += 1

    @property
    def articles(self) -> [Article]:
        return self._articles


def pars_urs_to_main_page(path : str) -> ArticleSet:
    article_set = ArticleSet()

    with open(path, "r", encoding='utf-8') as f:
        content = f.read()
        f.close()

    tree = etree.HTML(content)

    articles = tree.xpath('//div[@class="' + g_class_article_name + '"]')

    i = 0
    for article in articles:
        publisherPars = article.xpath('.//a[@class="' + g_class_publisher_name + '"]')
        if len(publisherPars) == 1:
            publisher = publisherPars[0].text

        titlePars = article.xpath('.//a[@class="' + g_class_title_name + '"]')
        if len(titlePars) == 1:
            title = titlePars[0].text

        urlToArticlePars = article.xpath('.//a[@class="' + g_class_title_name + '"]/@href')
        if len(urlToArticlePars) == 1:
            urlToArticle = urlToArticlePars[0]

        date_time_pars = article.xpath('.//time[@class="' + g_class_date_name + '"]/@datetime')
        if len(date_time_pars) == 1:
            date_time = date_time_pars[0]

        a = Article(title, urlToArticle, publisher, i, date_time)
        article_set.add_article(a)
        i += 1

    return article_set


def download_and_save_page(url : str, path_to_save : str, title : str):
    url = url.replace('.', 'https://news.google.com')
    try:
        response = requests.get(url, timeout=20)
    except:
        print("Can't download:", url)
        return title

    if len(response.content ) < 5000:
        return title

    with open(path_to_save, "wb") as f:
        f.write(response.content)
        print('Download completed:', url)
    return ""


def write_articles_meta_data(article_set : ArticleSet, path_to_save : str):
    articles = []
    for a in article_set.articles:
        dick = {}
        dick["title"] = a.title
        dick["publisher"] = a.publisher
        dick["url"] = a.url
        dick["index"] = a.index
        dick["date"] = a.date.strftime("%Y-%m-%dT%H:%M:%SZ")
        articles.append(dick)
    json_object = json.dumps(articles, indent=4)

    with open(path_to_save, "w") as outfile:
        outfile.write(json_object)


def download_articles(path : str):
    article_set = pars_urs_to_main_page(path)

    path_to_save = os.path.splitext(path)[0]

    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    n_cores = os.cpu_count()

    i = 0
    to_remove = []

    with futures.ProcessPoolExecutor(n_cores) as executor:
        to_do = []

        for a in article_set.articles:
            path_out = path_to_save + "/" + str(a.index) + ".html"
            future = executor.submit(download_and_save_page, a.url, path_out, a.title)
            to_do.append(future)
            i += 1

        for future in futures.as_completed(to_do):
            if not future.done():
                print("Finished with failed!")
            title = future.result()
            if title != "":
                to_remove.append(title)

    print("to_remove: ", to_remove)
    for a in to_remove:
        article_set.remove_article(a)

    if len(article_set.articles) == 0:
        os.rmdir(path_to_save)
        return

    path_to_meta = path_to_save + "/meta.json"
    write_articles_meta_data(article_set, path_to_meta)


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

    for company_path in os.listdir(options.path_to_storage):
        if not company_path in options.company:
            continue

        company_path = options.path_to_storage + company_path

        for date_path in os.listdir(company_path):
            date = datetime.datetime.strptime(date_path, "%Y-%m-%d")

            if date > options.start_date and date <= options.end_date:
                date_path = company_path + "/" + date_path
                if os.path.isfile(date_path):
                    print(date_path)
                    download_articles(date_path)


if __name__ == "__main__":
    sys.exit(main())