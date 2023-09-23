import sys
import os
import json

from argparse import ArgumentParser
import xlsxwriter


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


def write_report(path, data):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    ranks = ["positive", "neutral", "negative"]

    for i in range(len(ranks)):
        worksheet.write(i + 1, 0, ranks[i])

    company_i = 0
    for company in data:
        worksheet.write(0, company_i + 1, company.name)

        for i in range(len(ranks)):
            worksheet.write(i + 1, company_i + 1, str(company.data[ranks[i]]))

        company_i += 1

    workbook.close()


class Company:
    def __init__(self, name):
        self._name = name
        self._data = {}
        self._data["positive"] = 0
        self._data["neutral"] = 0
        self._data["negative"] = 0

    @property
    def name(self):
        return self._name

    def addData(self, tag, value):
        self._data[tag] = value

    def addPoitive(self):
        self._data["positive"] += 1

    def addNeutral(self):
        self._data["neutral"] += 1

    def addNegative(self):
        self._data["negative"] += 1

    @property
    def data(self):
        return self._data


def main():
    options = Options()

    print("input company: ", options.company)

    companes = []

    for company_path in os.listdir(options.path_to_storage):
        company = Company(company_path)

        company_path = options.path_to_storage + company_path
        if os.path.isfile(company_path):
            continue

        for date_path in os.listdir(company_path):
            date_path_full = company_path + "/" + date_path
            if not os.path.isfile(date_path_full):

                path_to_meta = date_path_full + "/meta.json"
                if not os.path.exists(path_to_meta):
                    print("meta not exists: ", path_to_meta)
                    continue

                with open(path_to_meta, "r", encoding='utf-8') as f:
                    articles = json.load(f)

                    for a in articles:
                        rank = a["title_rank"]

                        if rank == 1:
                            company.addPoitive()
                        if rank == 0:
                            company.addNeutral()
                        if rank == -1:
                            company.addNegative()

        companes.append(company)

    path_to_report = options.path_to_storage + "semantic_title_rank_report.xlsx"
    write_report(path_to_report, companes)


if __name__ == "__main__":
    sys.exit(main())