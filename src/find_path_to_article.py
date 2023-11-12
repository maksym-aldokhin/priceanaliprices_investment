import os
import json


def find_article_with_title(path, title):
    for file_name in os.listdir(path):
        path_to_files = path + file_name
        if not os.path.isfile(path_to_files):
            continue

        if file_name == "meta.json":
            continue

        with open(path_to_files, "r+", encoding='utf-8') as f:
            data = f.read()

            if title in data:
                return file_name
    return ""


def find_path_to_article(options):
    path = options.path_to_storage

    for company_path in os.listdir(path):
        company_path = path + company_path
        for date_path in os.listdir(company_path):
            date_path = company_path + "/" + date_path
            if os.path.isfile(date_path):
                continue

            path_to_meta = date_path + "/meta.json"

            title_to_remove = []
            with open(path_to_meta, "r+", encoding='utf-8') as f:
                articles = json.load(f)
                for i in range(len(articles)):
                    # print(i)
                    path_to_article = find_article_with_title(date_path, articles[i]["title"])
                    if path_to_article == "":
                        title_to_remove.append(articles[i]["title"])
                        continue
                    articles[i]["path"] = path_to_article

                if len(title_to_remove) > 0:
                    for idx, obj in enumerate(articles):
                        if obj['title'] in title_to_remove:
                            articles.pop(idx)

                f.seek(0)
                json.dump(articles, f, indent=4)
                print("writed: ", path_to_meta)
                f.truncate()