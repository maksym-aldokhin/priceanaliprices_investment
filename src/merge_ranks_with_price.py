import os
import sys
import xlsxwriter
import pandas as pd

from argparse import ArgumentParser

class Options:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument("--path-to-reports", help="list of company ", type=str)
        parser.add_argument("--path-output", help="path to storage", type=str)
        parsed = parser.parse_args()

        if not (',' in parsed.path_to_reports):
            self.pathes_to_reports = [parsed.path_to_reports]
        else:
            self.pathes_to_reports = parsed.path_to_reports.split(',')

        self.path_output = parsed.path_output


def main():
    options = Options()
    dfs = []

    for p in options.pathes_to_reports:
        path_to_file = p

        if not os.path.exists(path_to_file):
            print("Can't fined: ", path_to_file)
            continue

        read_data = pd.read_excel(path_to_file)
        # print(read_data.columns)
        coloms_names = []
        for i in read_data.columns:
            if i == "Date":
                coloms_names.append(i)
            else:
                coloms_names.append(os.path.basename(p) + " " + i)
        read_data.columns = coloms_names
        try:
            read_data['Date'] = pd.to_datetime(read_data['Date'], format='%Y-%m-%d')
        except:
            read_data['Date'] = pd.to_datetime(read_data['Date'], format='%m/%d/%Y')

        print(coloms_names)

        dfs.append(read_data)

    # Merge the DataFrames based on the 'date' column
    merged_df = pd.concat([df.set_index('Date') for df in dfs], axis=1)

    merged_df.fillna(method='ffill', inplace=True)
    # Reset the index to make 'date' a column again
    merged_df.reset_index(inplace=True)

    # Write the merged data to a new Excel file
    merged_df.to_excel(options.path_output, index=False)


if __name__ == "__main__":
    sys.exit(main())