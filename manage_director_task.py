 # coding = utf8
'''
    Arthor: Zijun Liu
            Jie Wang
'''
import os
import json
import difflib
import re
import pandas as pd



def exists_sem(middle_list):
    for i in middle_list:
        if i[-1] == ";":
            return True
    return False


def clean_list(result_list):
    a = []
    for i in result_list:
        if i.strip()[:3] == 'and':
            a[-1] = a[-1] + i
            continue
        if i == "":
            continue
        a.append(i)
    return a

def get_title(temp_list):  
    con_list = ' '.join(temp_list)
    pattern = re.compile(r';(.*?);')
    result = pattern.findall(con_list)
    new_result = []
    for i in result:

        if  'DIRECTORE' in i:
            i = ' '.join(i.split(".",2)[:2]) 
            new_result.append(i)
            break
        new_result.append(i)
    print(new_result)
    return new_result


def get_name(temp_list):
    a = list(temp_list[0])
    a[-1]=';'
    new_first_element = "".join(a)
    temp_list[0] = new_first_element
    
    con_list = ' '.join(temp_list)


    pattern = re.compile(r';(.*?);')
    result = pattern.findall(con_list)
    new_result = []
    for i in result:
        if  'DIRECTORE' in i:
            i = ' '.join(i.split(".",2)[:2]) 
            new_result.append(i)
            break
        new_result.append(i)
    print(new_result)
    return new_result



# put all staff into list d
files = os.listdir("DAY")
for i in files:
    # jump out .csv folder
    if ".csv" in i:
        continue
    # find a repository for .day file
    path = f"DAY/{i}"

    # temp list
    temp_list = []
    # 0 is not start, 1 is start
    flag = 0
    # loop each line for .day file
    with open(path, "r")as f:
        for j in f:
            
            # based on "," to seperate file
            word = j.strip().split(",")
            '''
            1. find management, if yes, marked it as 1 and jump out the loop
            2. store it into temp_list
            3. end with comparative
            4. If it is comparative, it will stop
            '''
            if word[-1].lower().strip() == 'management':
                temp_list = []
                flag = 1
                continue
            if word[-1].lower().strip() == 'comparative' and flag == 1:
                break
            if flag == 0:
                continue
            else:
                temp_list.append(word[-2].strip())

    title_list = get_title(temp_list)
    name_list = get_name(temp_list)[:len(title_list)]
    df = pd.DataFrame(list(zip(name_list, title_list)), 
               columns =['Name', 'title']) 
    df.to_csv(f"{i}.csv")

    
    







