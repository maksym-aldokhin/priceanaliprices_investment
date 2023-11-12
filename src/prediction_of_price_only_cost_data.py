import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import os
import sys

from argparse import ArgumentParser

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

    for c in options.company:
        path_to_file = options.path_to_storage + c + ".xlsx"

        if not os.path.exists(path_to_file):
            print("Can't fined: ", path_to_file)
            continue

        data = pd.read_excel(path_to_file)

        features = ['Open', 'High', 'Low', 'Adj Close', 'Close', 'Volume']
        target = 'Close'

        X = data[features][:-2]
        y = data[target][1:-1]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the linear regression model
        model = LinearRegression()

        # Fit the model to the training data
        model.fit(X_train, y_train)

        # Predict on the test set
        predictions = model.predict(X_test)

        # Evaluate the model using Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, predictions)
        print('Mean Squared Error:', mse)

        # Now you can use the model to make predictions for new data
        # For example, if you have new features for a company, you can predict its closing price:
        new_features = [329.5299988,330.4400024,324.5299988,325.4700012,325.4700012,1416800]
        predicted_closing_price = model.predict([new_features])
        print(predicted_closing_price)


if __name__ == "__main__":
    sys.exit(main())