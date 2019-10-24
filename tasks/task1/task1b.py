import csv
import logging
import sys
import string
import numpy as np
import pandas as pd
import matplotlib.patches as patches
import matplotlib.pyplot as plt

def companyname(filepath="OCRoutputIndustrial19300006-000970.day"):
    df=pd.read_csv(filepath,header=0)
    #remove any row with empty value
    df.dropna(subset=df.columns[[15]],inplace=True)
    #words without punctuation
    words=df.iloc[:,15].tolist()
    x_1=df.iloc[:,1].tolist()
    x_2=df.iloc[:,2].tolist()
    y_1=df.iloc[:,3].tolist()
    y_2=df.iloc[:,4].tolist()
    length = len(words)
    begin = 0
    company_name = []
    x1_words=[]
    x2_words=[]
    y1_words=[]
    y2_words=[]
    for i in range(1, length):
        if words[i].isupper()==False and (lambda: words[i-1].isupper()==True or 
                    length>(i+1) and words[i+1].isupper()==True):
            if len(words[begin: i])>=2:
                company_name.append(words[begin: i])
                x1_words.append(x_1[begin: i])
                x2_words.append(x_2[begin: i])
                y1_words.append(y_1[begin: i])
                y2_words.append(y_2[begin: i])
            begin=i+1
    mean=[]
    for i in range(0,len(company_name)):
        if abs(np.mean(x_1)-np.mean(x1_words[i]))<0.1*np.mean(x_1) and abs(np.mean(x_2)-np.mean(x2_words[i]))<0.1*np.mean(x_2):
            mean.append(company_name[i])
    print(mean)
    #TODO: drop any lists with length of 2 contains only single letters
companyname(filepath="OCRoutputIndustrial19300006-000970.day")