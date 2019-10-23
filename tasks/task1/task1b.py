import csv
import logging
import sys
import string
import numpy as np

logging.basicConfig(level=logging.INFO)

def main():
    with open('mastercolumns1930.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        list = []
        for row in reader:
            if float(row['0'])== 1:
            	#since we are doing 1 column page, default column name for image name is 'Industrial19300001-0001.tif'
                list.append((row['Industrial19300001-0001.tif']))
    print(list[:15])

    with open('OCRoutputIndustrial19300006-000170.day') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cn=[]
        test=[]

        for line in csv_reader:
            textwp=line[15]
            #if len(textwp)>1:
            test.append(textwp)
    tt = [x for x in test if x != '']
    length = len(tt)
    begin = 0
    list1 = []
    final=[]

    for i in range(1, length):
        if tt[i].isupper()==False and (lambda: tt[i-1].isupper()==True or 
                    length>(i+1) and tt[i+1].isupper()==True):
            list1.append(tt[begin: i])
            begin=i+1
    #get rid of empyty list
    list2 = [x for x in list1 if x != [''] if x != []]
    #list3 = [x for x in list2 if x != []]
    #if the length of the list is smaller than 2, get rid of it, mostly is not a company name
    for i in range(0,len(list2)):
        if len(list2[i])>2:
            final.append(list2[i])
    #print(list2) 
    print(final) 

if __name__ == "__main__":
    main()