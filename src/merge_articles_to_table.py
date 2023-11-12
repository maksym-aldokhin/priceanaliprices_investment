import sys
import os
import json
import datetime

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

    start_date = datetime.datetime(2000, 1, 1)
    end_date = datetime.datetime(2023, 9, 10)

    date = start_date
    while date <= end_date:
        worksheet.write((date - start_date).days + 1, 0, date.strftime('%m/%d/%Y'))
        date = date + datetime.timedelta(days=1)

    company_i = 0
    for company in data:
        worksheet.write(0, company_i + 1, company.name)

        date = start_date
        while date <= end_date:
            if date in company.getDates():
                worksheet.write((date - start_date).days + 1, company_i + 1, str(company.getDates()[date]))
            else:
                worksheet.write((date - start_date).days + 1, company_i + 1, str(0))
            date = date + datetime.timedelta(days=1)

        company_i += 1

    workbook.close()


class Company:
    def __init__(self, name):
        self._name = name
        self._dates = {}

    @property
    def name(self):
        return self._name

    def addDate(self, date, value):
        self._dates[date] = value

    def getDates(self):
        return self._dates


def main():
    options = Options()

    print("input company: ", options.company)

    companes = []

    for company_path in os.listdir(options.path_to_storage):
        company = Company(company_path)

        company_path = options.path_to_storage + "/" + company_path
        if os.path.isfile(company_path):
            continue

        for date_path in os.listdir(company_path):
            date_path_full = company_path + "/" + date_path
            if not os.path.isfile(date_path_full):
                date = datetime.datetime.strptime(date_path, "%Y-%m-%d")

                path_to_meta = date_path_full + "/meta.json"
                if not os.path.exists(path_to_meta):
                    print("meta not exists: ", path_to_meta)
                    continue

                text = ""
                with open(path_to_meta, "r", encoding='utf-8') as f:
                    articles = json.load(f)

                    for a in articles:
                        with open(path_to_meta, "r", encoding='utf-8') as f:
                            path_to_file = date_path_full + "/" + str(a["index"]) + ".txt"

                            if not os.path.exists(path_to_file):
                                print("Not fined: ", path_to_file)
                                continue

                            try:
                                with open(path_to_file, "r", encoding='utf-8', errors='ignore') as f:
                                    text += f.read() + " "
                                    f.close()
                            except:
                                continue

                company.addDate(date, text)

        companes.append(company)

    path_to_report = options.path_to_storage + "article.xlsx"
    write_report(path_to_report, companes)


if __name__ == "__main__":
    sys.exit(main())