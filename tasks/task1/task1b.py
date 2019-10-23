import csv
import logging
import sys
import string
import numpy as np

logging.basicConfig(level=logging.INFO)

def main():

    with open('OCRoutputIndustrial19300006-001370.day') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cn=[]
        test=[]

        for line in csv_reader:
            textwp=line[15]
            #if len(textwp)>1:
            test.append(textwp)
    wlist = [x for x in test if x != '']

    length = len(wlist)
    begin = 0
    list1 = []
    final=[]

    for i in range(1, length):
        if wlist[i].isupper()==False and (lambda: wlist[i-1].isupper()==True or 
                    length>(i+1) and wlist[i+1].isupper()==True):
            list1.append(wlist[begin: i])
            begin=i+1
    #get rid of empyty list/empty item
    list2 = [x for x in list1 if x != [''] if x != []]
    #list3 = [x for x in list2 if x != []]
    for i in range(0,len(list2)):
        if len(list2[i])>2:
            final.append(list2[i])
    #print(list2) 
    print(final) 

if __name__ == "__main__":
    main()