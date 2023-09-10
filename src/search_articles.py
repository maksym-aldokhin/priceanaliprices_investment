import requests
import pandas as pd
import datetime
import os
from bs4 import BeautifulSoup

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




