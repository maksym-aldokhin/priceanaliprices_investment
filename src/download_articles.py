# import xml.sax
# import xml.sax.saxutils
from lxml import etree
import requests
import os
import json
from concurrent import futures

g_class_article_name = "NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"
g_class_publisher_name = "wEwyrc"
g_class_title_name = "DY5T1d RZIKme"

class Article:
    def __init__(self, title : str, url : str, publisher : str):
        self._title = title
        self._url = url
        self._publisher = publisher

    # def set_title(self, title : str):
    #     self._title = title

    @property
    def title(self) -> str:
        return self._title

    # def set_url(self, url : str):
    #     self._url = url

    @property
    def url(self) -> str:
        return self._url

    # def set_publisher(self, publisher : str):
    #     self._publisher = publisher

    @property
    def publisher(self) -> str:
        return self._publisher


class ArticleSet:
    def __init__(self):
        self._articles = list()

    def add_article(self, a):
        self._articles.append(a)

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

        a = Article(title, urlToArticle, publisher)
        article_set.add_article(a)

    return article_set


def download_and_save_page(url : str, path_to_save : str, title : str):
    url = url.replace('.', 'https://news.google.com')
    try:
        response = requests.get(url, timeout=20)
    except:
        print("Can't download:", url)
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
        articles.append(dick)

    json_object = json.dumps(articles, indent=4)

    # Writing to sample.json
    with open(path_to_save, "w") as outfile:
        outfile.write(json_object)


def download_articles(path : str):
    article_set = pars_urs_to_main_page(path)

    path_to_save = os.path.splitext(path)[0]

    if not os.path.exists(path_to_save
                          ):
        os.makedirs(path_to_save)
    n_cores = os.cpu_count()
    print("Found logical cpu cores: ", n_cores)

    i = 0
    to_remove = []

    with futures.ProcessPoolExecutor(n_cores) as executor:
        to_do = []

        for a in article_set.articles:
            path = path_to_save + "/" + str(i) + ".html"
            future = executor.submit(download_and_save_page, a.url, path, a.title)
            to_do.append(future)
            i += 1

        for future in futures.as_completed(to_do):
            if not future.done():
                print("Finished with failed!")
            res = future.result()
            if res != "":
                to_remove.append(res)

    print(to_remove)
    for a in to_remove:
        article_set.remove_article(a)

    path_to_meta = path_to_save + "/meta.json"
    write_articles_meta_data(article_set, path_to_meta)