import os
import re
import json
import sys

from argparse import ArgumentParser

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

import negative_articles_set
import positive_articles_set
import neutral_articles_set


need_to_remove = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', '_', '-', '=', '\'', '\"', '`', '*', '/', '\\', '|', '@', '#', '%', '&', '(', ')', '$', '^', '[', ']', '©', '–', '•', '?', '¢', ':', ';', '<', '>', '—', '’', '“', '”', '+']


nltk.download('punkt')
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


def learn_classifier():
    positive_dataset = list(set(positive_articles_set.pos_articles))
    negative_dataset = list(set(negative_articles_set.negative_articles))
    neutral_dataset = list(set(neutral_articles_set.neu_articles))

    # Preprocess your datasets
    positive_data = [preprocess_text(text) for text in positive_dataset]
    negative_data = [preprocess_text(text) for text in negative_dataset]
    neutral_data = [preprocess_text(text) for text in neutral_dataset]

    from sklearn.feature_extraction.text import TfidfVectorizer

    # Combine all data and labels
    all_data = positive_data + negative_data + neutral_data
    labels = ['positive'] * len(positive_data) + ['negative'] * len(negative_data) + ['neutral'] * len(neutral_data)

    # TF-IDF vectorization
    tfidf_vectorizer = TfidfVectorizer()
    X = tfidf_vectorizer.fit_transform(all_data)

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

    # Train a logistic regression model
    model = LogisticRegression(max_iter=10000)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    from sklearn.metrics import accuracy_score

    # Evaluate the model
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")
    return model, tfidf_vectorizer


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


def calculate_title_rank(text, classifier, tfidf_vectorizer) -> int:
    preprocessed_text = preprocess_text(text)
    text_vectorized = tfidf_vectorizer.transform([preprocessed_text])
    prediction = classifier.predict(text_vectorized)

    if prediction[0] == "positive":
        return 1
    if prediction[0] == "neutral":
        return 0
    if prediction[0] == "negative":
        return -1


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
        print("write_ranks:", len(articles), " : ", len(ranks))
        for i in range(len(articles)):
            # print(i)
            if i > len(ranks):
                print("error")
                continue
            articles[i]["article_rank"] = ranks[i]

        f.seek(0)
        json.dump(articles, f, indent=4)
        print("writed: ", path)
        f.truncate()


def rank_for_date(path, classifier, tfidf_vectorizer):
    path_to_meta = path + "/meta.json"
    if not os.path.exists(path_to_meta):
        print("Not fined: ", path_to_meta)
        return

    with open(path_to_meta, "r+", encoding='utf-8') as f:
        articles = json.load(f)
        for i in range(len(articles)):
            if len(str(articles[i]["title"])) < 10:
                articles[i]["title_rank"] = 0
                continue
            rank = calculate_title_rank(str(articles[i]["title"]), classifier, tfidf_vectorizer)
            articles[i]["title_rank"] = rank
        f.seek(0)
        json.dump(articles, f, indent=4)
        print("writed: ", path)
        f.truncate()


def rank_for_date_set(paths, classifier, tfidf_vectorizer, number_of_thread):
    print("thread:", number_of_thread, "len:", len(paths))
    i = 0
    for path in paths:
        print("start: " + path, " - ", i / len(paths), "thread:", number_of_thread)
        rank_for_date(path, classifier, tfidf_vectorizer)
        print("finish: " + path, " - ", i / len(paths), "thread:", number_of_thread)
        i += 1


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


def calculate_title_rank_for_set(options):
    classifier, tfidf_vectorizer = learn_classifier()

    path_to_storage = options.path_to_storage

    n_cores = 24

    for company_path in os.listdir(path_to_storage):
        if not company_path in options.company:
            print("skip: ", company_path)
            continue

        company_path = path_to_storage + company_path
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

        with futures.ProcessPoolExecutor(n_cores) as executor:
            to_do = []
            for pathes in pathes_set:
                future_to_do = executor.submit(rank_for_date_set, pathes, classifier, tfidf_vectorizer, len(to_do))
                to_do.append(future_to_do)

            for future in futures.as_completed(to_do):
                future.result()
                if not future.done():
                    print("Finished with failed!")
                i += 1
                print("finished: ", i/count_date * 100, "%")

    print("finish")


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


def main():
    options = Options()

    print("input company: ", options.company)
    calculate_title_rank_for_set(options)


if __name__ == "__main__":
    sys.exit(main())