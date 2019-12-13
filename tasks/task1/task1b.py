import numpy as np
import pandas as pd
import sys

def companyname(filepath):
    df = pd.read_csv(filepath, header=0)
    df.dropna(subset=df.columns[[15]], inplace=True)
    words = df.iloc[:, 15].tolist()
    x_1 = df.iloc[:, 1].tolist()
    x_2 = df.iloc[:, 2].tolist()
    y_1 = df.iloc[:, 3].tolist()
    y_2 = df.iloc[:, 4].tolist()
    length = len(words)
    begin = 0
    company_name = []
    x1_words = []
    x2_words = []
    y1_words = []
    y2_words = []
    for i in range(1, length):
        # TODO Why comparing against a function (lambda is always true)
        if words[i].isupper() is False and (lambda: words[i - 1].isupper(
        ) or length > (i + 1) and words[i + 1].isupper()):
            if len(words[begin:i]) >= 2:
                company_name.append(words[begin:i])
                x1_words.append(x_1[begin:i])
                x2_words.append(x_2[begin:i])
                y1_words.append(y_1[begin:i])
                y2_words.append(y_2[begin:i])
            begin = i + 1
    mean = []
    y1 = []
    y2 = []
    y_length = [a - b for a, b in zip(y_2, y_1)]
    for i in range(0, len(company_name)):
        if abs(np.mean(x_1) -
               np.mean(x1_words[i])) < 0.1 * np.mean(x_1) and abs(
                   np.mean(x_2) - np.mean(x2_words[i])) < 0.1 * np.mean(x_2):
            mean.append(company_name[i])
            y1.append(y1_words[i])
            y2.append(y2_words[i])
    y_diff = []
    for a, b in zip(y2, y1):
        diffs = []
        y_diff.append(diffs)
        for x, y in zip(a, b):
            try:
                diffs.append(abs((float(x) - float(y))))
            except ValueError:
                diffs.append([y, x])
    final = []
    for i in range(0, len(mean)):
        if np.mean(y_diff[i]) > np.quantile(y_length, .75):
            final.append(mean[i])
    letter = []
    for i in range(0, len(final)):
        if len(final[i]) == 2:
            for j in range(0, len(final[i]) - 1):
                if len(final[i][j]) == 1:
                    letter.append(final[i])
    res = [i for i in final if i not in letter]
    print(res)


companyname(sys.argv[1])
