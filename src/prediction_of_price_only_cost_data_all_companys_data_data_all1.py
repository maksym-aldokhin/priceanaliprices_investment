import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import os
import sys

from argparse import ArgumentParser

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


def main():
    options = Options()

    for company in options.company:
        path_to_file = options.path_to_storage + options.file_name + ".xlsx"

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

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        # Initialize the linear regression model
        # model = LinearRegression()
        model = RandomForestRegressor(n_estimators=100, random_state=42)

        # Fit the model to the training data
        model.fit(X_train, y_train)

        # Predict on the test set
        predictions = model.predict(X_test)

        # Evaluate the model using Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, predictions)
        print('Mean Squared Error:', mse)

        # Now you can use the model to make predictions for new data
        # For example, if you have new features for a company, you can predict its closing price:
        new_features = [0.628571429, 0.8, 0.461538462, 0.587301587, 0.47826087, 0.420289855, 0.564705882, 0.841269841, 0.407894737, 0.384615385, 0.659574468, 0.517241379, 0.627118644, 0.412698413, 0.454545455, 0.333333333, 0.26984127, 0.470588235, 0.551020408, 0.418918919, 0.583333333, 0.656716418, 0.698630137, 0.782608696, 0.661971831, 0.638297872, 0.483333333, 0.493670886, 0.319444444, 0.588235294, 0.589041096, 0.526315789, 0.575757576, 0.573529412, 0.715909091, 0.515151515, 0.5, 1.257142857, 1.338461538, 1.461538462, 2.031746032, 1.550724638, 1.31884058, 1.764705882, 1.26984127, 1.394736842, 1.461538462, 1.340425532, 1.068965517, 1.372881356, 1.603174603, 2.181818182, 1, 1.634920635, 1.529411765, 1.448979592, 1.364864865, 1.5, 1.388059701, 1.356164384, 1.31884058, 1.661971831, 1.553191489, 1.25, 1.455696203, 1.819444444, 1.470588235, 1.301369863, 1.789473684, 1.545454545, 1.220588235, 2.477272727, 1.348484848, 1.614285714, 0.171428571, -0.015384615, 0, -0.111111111, -0.666666667, -0.043478261, -0.141176471, 0.126984127, -0.197368421, -0.057692308, 0.085106383, -0.24137931, -0.169491525, -0.619047619, -0.636363636, 0.166666667, -0.222222222, 0.014705882, 0.163265306, -0.108108108, -0.180555556, 0.104477612, -0.082191781, -0.289855072, 0.098591549, 0.085106383, -0.1, -0.088607595, -0.430555556, 0.117647059, -0.150684932, -0.157894737, -0.136363636, -0.176470588, -0.045454545, -0.075757576, -0.2, 323.8999939, 329.0400085, 323.230011, 328.2000122, 328.2000122, 1533000, 180.8999939, 180.8999939, 174.1000061, 176.0800018, 176.0800018, 623186, 133.8000031, 137.1999969, 133.5200043, 136.4199982, 136.4199982, 869871, 91.63999939, 91.76000214, 88.95500183, 89.97000122, 89.97000122, 18667200, 133.8999939, 138.0299988, 133.1600037, 137.8500061, 137.8500061, 48498900, 106.1399994, 107.6900024, 105.0899963, 106.5899963, 106.5899963, 49080100, 175.1799927, 178.2100067, 173.5399933, 177.5599976, 177.5599976, 112488800, 50.06999969, 50.47000122, 49.99000168, 50.24000168, 50.24000168, 1453861, 25748.3125, 26409.30273, 25608.20117, 26240.19531, 26240.19531, 11088307100, 217.5, 220.5500031, 214.8600006, 216.0500031, 216.0500031, 4929600, 19275.15039, 19395, 19171, 19293, 19293, 11157, 71.08000183, 71.37999725, 70.76999664, 71.25, 71.25, 2328400, 54.75, 54.93999863, 53.52000046, 54.09999847, 54.09999847, 4275500, 20.77000046, 20.80999947, 20.38999939, 20.39999962, 20.39999962, 3311100, 134.6000061, 136.5800018, 133.9600067, 136.1999969, 136.1999969, 16976000, 148.1300049, 148.7799988, 147.3999939, 147.5200043, 147.5200043, 3332900, 36.83000183, 38.34000015, 36.75, 38.18000031, 38.18000031, 67659700, 66.04000092, 66.44999695, 65.30000305, 65.30000305, 65.30000305, 2146909, 331.2900085, 333.0799866, 329.0299988, 329.9100037, 329.9100037, 18381000, 441.1499939, 444.6000061, 436.7000122, 443.1400146, 443.1400146, 2922700, 4.760000229, 4.920000076, 4.760000229, 4.840000153, 4.840000153, 9500, 455.25, 463.4400024, 451.519989, 462.4100037, 462.4100037, 43333000, 123.8300018, 125.9599991, 122.5899963, 125.0899963, 125.0899963, 11864400, 70000, 70600, 69600, 70400, 70400, 13741241, 136.1799927, 138.1199951, 135.9199982, 136.4600067, 136.4600067, 1216437, 84.97000122, 85.36000061, 84.75, 85.23000336, 85.23000336, 594900, 2.220000029, 2.269999981, 2.119999886, 2.200000048, 2.200000048, 504000, 245.0700073, 252.8099976, 243.2700043, 251.4900055, 251.4900055, 115312900, 178.3500061, 179.1900024, 177.8000031, 178.8699951, 178.8699951, 260700, 59.18999863, 59.18999863, 57.06000137, 57.45999908, 57.14990616, 83006, 107, 108.0999985, 105.6399994, 105.7600021, 105.7600021, 1031029, 6, 9]
        predicted_closing_price = model.predict([new_features])
        print(company, ": ", predicted_closing_price)


if __name__ == "__main__":
    sys.exit(main())