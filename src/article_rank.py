import os
import re
import json

from bs4 import BeautifulSoup

import nltk
# nltk.download('stopwords')

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


need_to_remove = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', '_', '-', '=', '\'', '\"', '`', '*', '/', '\\', '|', '@', '#', '%', '&', '(', ')', '$', '^', '[', ']', '©', '–', '•', '?', '¢', ':', ';', '<', '>', '—', '’', '“', '”', '+']


def extract_features(word_list):
    return dict([(word, True) for word in word_list])

def learn_classifier():
    nltk.download('movie_reviews')
    from nltk.corpus import movie_reviews

    # Load positive and negative reviews
    positive_fileids = movie_reviews.fileids('pos')
    negative_fileids = movie_reviews.fileids('neg')

    features_positive = [(extract_features(movie_reviews.words(fileids=[f])),'Positive') for f in positive_fileids]
    features_negative = [(extract_features(movie_reviews.words(fileids=[f])),'Negative') for f in negative_fileids]


    # Split the data into train and test (80/20)
    threshold_factor = 1
    threshold_positive = int(threshold_factor * len(features_positive))
    threshold_negative = int(threshold_factor * len(features_negative))

    features_train = features_positive[:threshold_positive]+features_negative[:threshold_negative]
    # features_test = features_positive[threshold_positive:]+features_negative[threshold_negative:]

    # print("Number of training datapoints: ", len(features_train))
    # print("Number of test datapoints: ", len(features_test))

    classifier = NaiveBayesClassifier.train(features_train)
    # print("Accuracy of the classifier: ", nltk.classify.util.accuracy(classifier, features_test))
    return classifier


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


# def claer_stop_word(text : str) -> str:
#     text_tokens = word_tokenize(text)
#     tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
#     return tokens_without_sw


def extract_features(word_list):
    return dict([(word, True) for word in word_list])


def calculate_article_rank(article_path : str, classifier) -> float:
    with open(article_path, "r", encoding='utf-8') as f:
        content = f.read()
        f.close()

    content = clear_file(content)
    content = filter_word(content)
    # content = claer_stop_word(content)

    probdist = classifier.prob_classify(extract_features(content.split()))
    pred_sentiment = probdist.max()
    if pred_sentiment is "Positive":
        return round(probdist.prob(pred_sentiment), 2)
    else:
        return round(probdist.prob(pred_sentiment), 2) * -1.0


def clear_file(content : str) -> str:

    cleantext = BeautifulSoup(content, "lxml").text

    return os.linesep.join([s for s in cleantext.splitlines() if s])

    path_to_save = os.path.splitext(path)[0] + "_clear.txt"
    with open(path_to_save, "w", encoding="utf-8") as f:
        f.write(cleantext)


def write_ranks(ranks, path : str):
    path = path + "/meta.json"
    with open(path, "r+", encoding='utf-8') as f:
        articles = json.load(f)
        # f.close()

        for i in range(len(articles)):
            print(i)
            if i > len(ranks):
                print("error")
                continue
            articles[i]["article_rank"] = ranks[i]

        f.seek(0)
        json.dump(articles, f, indent=4)
        f.truncate()


def calculate_articles_rank():
    classifier = learn_classifier()

    path = os.getcwd() + "/temp/"

    for company_path in os.listdir(path):
        company_path = path + company_path
        for date_path in os.listdir(company_path):
            date_path = company_path + "/" + date_path
            if os.path.isfile(date_path):
                continue
            print("start: " + date_path)

            ranks = list()

            for article_path in os.listdir(date_path):
                article_path = date_path + "/" + article_path
                if os.path.isfile(article_path) and ".html" in article_path:
                    rank = calculate_article_rank(article_path, classifier)
                    ranks.append(rank)
                    print(rank)

            print(ranks)
            write_ranks(ranks, date_path)
            print("finish: " + date_path)