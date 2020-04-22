 # coding = utf8
'''
    Arthor: Zijun Liu
'''
import os
import json
import difflib
import re
import pandas as pd
import stanza
#stanza.download('en')

with open('citylist.txt') as f:
    city_list = f.read().splitlines()

with open('jobslist.txt') as f:
    job_list = f.read().splitlines()

nlp = stanza.Pipeline(lang = 'en', processors = 'tokenize,ner')


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


def get_city_list(new_first_element,temp_list):
    #check by stanza
    doc_1 = nlp(new_first_element)#geo-political-entity GPE
    z = [(ent.text,ent.type) for k,sent in enumerate(doc_1.sentences) for w,ent in enumerate(sent.ents)]
    u = []
    for i in z:
        if i[1] == 'GPE':
            u.append(i[0])    
    
    result = []

    concate_list = [(temp_list[i] +' '+ temp_list[i + 1],i) for i in range(len(temp_list) - 1)]
    for t, i in enumerate(concate_list):
        new_string = i[0].replace(";", "")
        newer_string = new_string.replace(".","")
        #print(newer_string)
        if newer_string in city_list and newer_string in u:
            #double check 
            result.append((i[1],newer_string))
    return result


def get_name_list(temp_list):
    name_list = []
    new_bo = []
    lalal = []
    bo = [None]*1000
    for w,i in enumerate(temp_list[1:]):
        new_string = i.replace(";", "")
        newer_string = new_string.replace(".","")
        lalal.append(newer_string)
        if newer_string not in job_list:
            #print("not in")
            name_list.append(newer_string)
        else:
            #print('ininin')
            #print(w)
            new_bo.append([name_list,newer_string,w,'N/A'])

            bo[w] = new_bo
            name_list = []
    name_title = [x for x in bo if x is not None]
    print(name_title[1])
    return name_title[1]




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
    print(temp_list)
    new_first_element = " ".join(temp_list)

    result_name = get_name_list(temp_list)
    result_city = get_city_list(new_first_element,temp_list)
    for q in result_city:
        for j in result_name:
            if q[0]-2 == j[2]:
                #use city sub N/A
                j[3] = q[1]

    title_list = []
    name_list = []
    location_list = []
    for z in result_name:
        name_list.append(z[0])
        title_list.append(z[1])
        location_list.append(z[3])
    df = pd.DataFrame(list(zip(name_list, title_list, location_list)), 
                   columns =['Name', 'title','location']) 

    df.to_csv(f"{i}.csv")

    
    







