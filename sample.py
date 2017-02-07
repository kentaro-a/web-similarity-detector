import re, csv
import time
from pprint import pprint
from WebSimilarityDetector import WebSimilarityDetector


WD = WebSimilarityDetector()

with open("./files/f1.txt", "r") as f:
    cont = f.read()

targets = WD.makeDivisions(cont, min_word_count=20)

results = []
for t in targets:
    # You must take some interval between each requests for the Google search engine Servers.
    time.sleep(10)

    ret = WD.crawlGoogle(t)
    if ret:
        results.append(ret)

    if len(results) >= 3:
        break

with open('./results/result10.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(["類似率","文節","サイト内文章","サイトURL"])

    total_similarity = 0
    index = 0
    for ret in results:
        for r in ret:
            index = index + 1
            total_similarity += r["ratio"]
            writer.writerow([r["ratio"],r["query"],r["desc"],r["url"]])

    average_ratio = (total_similarity / index) if index > 0 else 0
    summary = [
        ["","","",""],
        ["平均類似率",average_ratio,"",""],
    ]
    writer.writerows(summary)
