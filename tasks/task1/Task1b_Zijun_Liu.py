#Name: Zijun Liu
#Task 1 B
import csv
import logging
import sys
import string
import numpy as np
import pandas as pd
import matplotlib.patches as patches
import matplotlib.pyplot as plt

if len(sys.argv) >= 3:
    from PIL import Image

def get_all_capitalized_word():
	source = open(sys.argv[1],'r')
	source_1 = source.read().splitlines()
	list_1 = []
	i = 0
	while i< len(source_1):
		split = source_1[i].split(",")
		list_1.append(split)
		i += 1
	
	num_list=[]

	i = 0
	while i < len(list_1):
		num_list.append(list_1[i][1])
		num_list.append(list_1[i][2])
		num_list.append(list_1[i][3])
		num_list.append(list_1[i][4])
		num_list.append(list_1[i][-2])
		i+=1
	
	result = []
	j = 0
	while j < len(num_list):
		if num_list[j+4].isupper() == True:
			result.append(num_list[j: j+5])
		j += 5
	return result

def get_one_column_company_name():
	result2 = get_all_capitalized_word()
	result1 = np.array(result2)
	k = 0
	one_column_company_name = []
	while k < len(result1[k]):
		if 6800 <= (int(result1[k+1][0])+int(result1[k+1][1]))/2 <= 7200:
			one_column_company_name.append(result1[k][4])
			one_column_company_name.append(result1[k+1][4])
			one_column_company_name.append(result1[k+2][4])
		if 6800 <= (int(result1[k+1][0])+int(result1[k+2][1]))/2 <= 7200:
			one_column_company_name.append(result1[k][4])
			one_column_company_name.append(result1[k+1][4])
			one_column_company_name.append(result1[k+2][4])
			one_column_company_name.append(result1[k+3][4])
		k += 1


	print (one_column_company_name)

get_one_column_company_name()




