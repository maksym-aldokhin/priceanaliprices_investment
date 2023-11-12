import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import os
import sys

from argparse import ArgumentParser

from concurrent import futures

max_words = 10000
max_sequence_length = 1000

class Options:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--company", help="list of company ", type=str)
        parser.add_argument("--file-name", help="list of company ", type=str)
        parser.add_argument("--path", help="path to storage", type=str)
        parsed = parser.parse_args()

        if not (',' in parsed.company):
            self.company = [parsed.company]
        else:
            self.company = parsed.company.split(',')

        self.path_to_storage = parsed.path
        self.file_name = parsed.file_name


def tokenith_company_articles(company, path_to_data, dates):
    path_to_company = path_to_data + "/" + company
    if not os.path.exists(path_to_company):
        return company, []

    text_on_date = []
    for date in dates:
        # print(date)

        date_str = date.strftime("%Y-%m-%d")
        path_to_company_date = path_to_company + "/" + date_str
        if not os.path.exists(path_to_company_date):
            text_on_date.append("")
            continue

        path_to_meta = path_to_company_date + "/meta.json"
        if not os.path.exists(path_to_meta):
            print("meta not exists: ", path_to_meta)
            text_on_date.append("")
            continue

        text = ""
        with open(path_to_meta, "r", encoding='utf-8') as f:
            articles = json.load(f)

            for a in articles:
                with open(path_to_meta, "r", encoding='utf-8') as f:
                    path_to_file = path_to_company_date + "/" + str(a["index"]) + ".txt"

                    if not os.path.exists(path_to_file):
                        print("Not fined: ", path_to_file)
                        continue

                    try:
                        with open(path_to_file, "r", encoding='utf-8', errors='ignore') as f:
                            text += f.read() + " "
                            f.close()
                    except:
                        continue
        text_on_date.append(text)

    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(text_on_date)
    # tokenizers.append(tokenizer)
    sequences = tokenizer.texts_to_sequences(text_on_date)
    return company, sequences


def main():
    options = Options()

    # companys = []
    # all_sequences = []

    # with futures.ProcessPoolExecutor(12) as executor:
    #     to_do = []

    #     for i, company in enumerate(os.listdir(options.path_to_data)):
    #         future = executor.submit(tokenith_company_articles, company, options.path_to_data, data['Date'])
    #         to_do.append(future)

    #     for future in futures.as_completed(to_do):
    #         if not future.done():
    #             print("Finished with failed!")
    #         company, sequences = future.result()
    #         companys.append(company)
    #         all_sequences.append(sequences)
    # padded_sequences_list = [pad_sequences(seq, maxlen=max_sequence_length) for seq in all_sequences]

    # X_news = np.concatenate(padded_sequences_list, axis=1)

    X_news = np.load(options.path_to_storage + "/" + "X_news.npy")

    for company in options.company:
        path_to_file = options.path_to_storage + "/" + options.file_name + ".xlsx"

        if not os.path.exists(path_to_file):
            print("Can't fined: ", path_to_file)
            continue

        data = pd.read_excel(path_to_file)
        features = []

        for c in data.columns:
            if c != "Date":
                features.append(c)
        target = company + ' Close'

        data['Date'] = pd.to_datetime(data['Date'])
        data['DayOfWeek'] = data['Date'].dt.dayofweek
        data['Month'] = data['Date'].dt.month

        features.append('DayOfWeek')
        features.append('Month')

        X = data[features][:-6]
        y = data[target][1: -5]
        X_news_short = X_news[:-6]

        # Split the data into training and testing sets
        X_prices_train, X_prices_test, X_news_train, X_news_test, y_train, y_test = train_test_split(X, X_news_short, y, test_size=0.2, random_state=42)

        # Initialize the linear regression model
        # model = LinearRegression()
        model = RandomForestRegressor(n_estimators=100, random_state=42)

        # Fit the model to the training data
        X_combined_train = np.concatenate((X_prices_train, X_news_train), axis=1)
        model.fit(X_combined_train, y_train)

        # Predict on the test set
        X_combined_test = np.concatenate((X_prices_test, X_news_test), axis=1)
        predictions = model.predict(X_combined_test)

        # Evaluate the model using Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, predictions)
        print('Mean Squared Error:', mse)


if __name__ == "__main__":
    sys.exit(main())