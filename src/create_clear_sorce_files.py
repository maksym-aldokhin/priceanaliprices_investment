import os
import re
import json
import sys
import shutil

from bs4 import BeautifulSoup

import nltk
# nltk.download('stopwords')

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from concurrent import futures

from random import shuffle

from argparse import ArgumentParser

import negative_articles_set
import positive_articles_set
import neutral_articles_set


class Options:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--company", help="list of company ", type=str)
        parser.add_argument("--path", help="path to storage", type=str)
        parser.add_argument("--path-to-save", help="path to storage", type=str)
        parsed = parser.parse_args()

        if not (',' in parsed.company):
            self.company = [parsed.company]
        else:
            self.company = parsed.company.split(',')

        self.path_to_storage = parsed.path
        self.path_to_save = parsed.path_to_save


need_to_remove = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', '_', '-', '=', '\'', '\"', '`', '*', '/', '\\', '|', '@', '#', '%', '&', '(', ')', '$', '^', '[', ']', '©', '–', '•', '?', '¢', ':', ';', '<', '>', '—', '’', '“', '”', '+']


nltk.download('stopwords')


def extract_features(word_list):
    return dict([(word, True) for word in word_list])


def preprocess_text(text):
    # Tokenization
    words = word_tokenize(text)

    # Stopword removal
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    return ' '.join(words)


def filter_word(text : str) -> str:
    #remove simbvoles
    # for s in need_to_remove:
    #     text = text.replace(s, '')

    #remove new lines
    text = text.replace('\n', ' ')

    #remove tabs
    text = text.replace('\t', ' ')

    #remove space
    text = re.sub(' +', ' ', text)
    return text


def extract_features(word_list):
    return dict([(word, True) for word in word_list])


def calculate_article_rank(article_path : str) -> str:
    try:
        with open(article_path, "r", encoding='utf-8', errors='ignore') as f:
            content = f.read()
            f.close()
    except:
        return ""

    content = clear_file(content)
    content = filter_word(content)

    return content


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def clear_file(content : str) -> str:

    cleantext = BeautifulSoup(content, "lxml").text

    return os.linesep.join([s for s in cleantext.splitlines() if s])

    path_to_save = os.path.splitext(path)[0] + "_clear.txt"
    with open(path_to_save, "w", encoding="utf-8") as f:
        f.write(cleantext)

def write_to_file(text : str, path : str):
    try:
        with open(path, "w", encoding='utf-8', errors='ignore') as f:
            f.write(text)
            f.close()
    except:
        return


def clear_date(path, path_to_save):
    path_to_meta = path + "/meta.json"
    if not os.path.exists(path_to_meta):
        print("Not fined: ", path_to_meta)
        return

    shutil.copyfile(os.path.normpath(path_to_meta), os.path.normpath(path_to_save + "/meta.json"))

    with open(path_to_meta, "r+", encoding='utf-8') as f:
        articles = json.load(f)
        for i in range(len(articles)):
            path_to_file = path + "/" + str(articles[i]["index"]) + ".html"
            if not os.path.exists(path):
                print("Not fined: ", path_to_file)
                continue

            clear_text = calculate_article_rank(path_to_file)
            if clear_text == "":
                continue
            path_to_save_file = path_to_save + "/" + str(articles[i]["index"]) + ".txt"
            write_to_file(clear_text, path_to_save_file)
        f.close()

def clear_date_set(paths, number_of_thread, path_to_save):
    print("thread:", number_of_thread, "len:", len(paths))
    i = 0
    for path in paths:
        path_to_save_date = path_to_save + "/" + os.path.basename(os.path.normpath(path))
        create_dir(path_to_save_date)
        print("start: " + path, " - ", str(int(i / len(paths) * 100)), "thread:", number_of_thread)
        clear_date(path, path_to_save_date)
        i += 1
        print("finish: " + path, " - ", str(int(i / len(paths) * 100)), "thread:", number_of_thread)


def splitting_array(input_arr, count):
    out = []

    if len(input_arr) < count or len(input_arr) == count:
        for t in input_arr:
            t_thread = [t]
            out.append(t_thread)
    else:
        k, m = divmod(len(input_arr), count)
        out = (input_arr[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(count))

    return out


def main():
    options = Options()

    path_to_storage = os.path.normpath(options.path_to_storage)
    path_to_save = os.path.normpath(options.path_to_save)

    n_cores = 24

    for company_name in os.listdir(path_to_storage):
        if not company_name in options.company:
            print("skip: ", company_name)
            continue

        company_path = path_to_storage + "/" + company_name
        print("company_path:", company_path)

        count_date = 0
        for path in os.listdir(company_path):
            # check if current path is a file
            if not os.path.isfile(os.path.join(company_path, path)):
                count_date += 1

        pathes_all = []
        for date_path in os.listdir(company_path):
            date_path = company_path + "/" + date_path
            if os.path.isfile(date_path):
                continue
            pathes_all.append(date_path)

        shuffle(pathes_all)

        pathes_set = splitting_array(pathes_all, n_cores)
        i = 0
        path_to_save_company = path_to_save + "/" + company_name
        create_dir(path_to_save_company)

        with futures.ProcessPoolExecutor(n_cores) as executor:
            to_do = []
            for pathes in pathes_set:
                future_to_do = executor.submit(clear_date_set, pathes, len(to_do), path_to_save_company)
                to_do.append(future_to_do)

            for future in futures.as_completed(to_do):
                future.result()
                if not future.done():
                    print("Finished with failed!")
                i += 1
                print("finished: ", i/count_date * 100, "%")

    print("finish")


if __name__ == "__main__":
    sys.exit(main())