import numpy as np
import pandas as pd


def companyname(filepath="OCRoutputIndustrial19300006-000970.day"):
    df = pd.read_csv(filepath, header=0)
    # remove any row with empty value
    df.dropna(subset=df.columns[[15]], inplace=True)
    # words without punctuation
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
        if not words[i].isupper():
            # checking truth value of a (lambda) function is always true
            # and (lambda: words[i - 1].isupper() or length > (i + 1) and
            #    words[i + 1].isupper()):
            if len(words[begin:i]) >= 2:
                company_name.append(words[begin:i])
                x1_words.append(x_1[begin:i])
                x2_words.append(x_2[begin:i])
                y1_words.append(y_1[begin:i])
                y2_words.append(y_2[begin:i])
            begin = i + 1
    mean = []
    for i in range(0, len(company_name)):
        if abs(np.mean(x_1) -
               np.mean(x1_words[i])) < 0.1 * np.mean(x_1) and abs(
                   np.mean(x_2) - np.mean(x2_words[i])) < 0.1 * np.mean(x_2):
            mean.append(company_name[i])
    # drop any lists with length of 2 contains only single letters
    letter = []
    for i in range(0, len(mean)):
        if len(mean[i]) == 2:
            for j in range(0, len(mean[i]) - 1):
                if len(mean[i][j]) == 1:
                    letter.append(mean[i])
    res = [i for i in mean if i not in letter]
    print(res)


companyname("OCRoutputIndustrial19300006-000970.day")
