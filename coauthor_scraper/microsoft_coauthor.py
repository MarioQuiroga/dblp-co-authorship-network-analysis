#imports
import csv
import json
from tools.dblp_author_url_serch import *
import time


 #declare paths
microsoft_author_json_path ='data/microsoft/microsoft_authors_titles.json'
microsoft_coauthors_edges_path = 'data/microsoft/authors_titles_microsoft.csv'
#read json authors and extract coauthors
authors_json=[]



with open(microsoft_author_json_path)as authors_titles_file_json:
    authors_titles_json = json.loads(authors_titles_file_json.read())

dic_aux={}
dic1=dict(list(authors_titles_json.items())[:300])
dic2=dict(list(authors_titles_json.items())[301:600])
dic3=dict(list(authors_titles_json.items())[601:])
#
dics=[dic1,dic2,dic3]

#authors_json = authors_titles_by_url_to_coauthor_edge(authors_titles_json)
with open(microsoft_coauthors_edges_path,'a')as intitute_csv_file:
#for author,coauthor in authors_json:
    
    for dic in dics:
        print (len(dic.keys()))
        authors_json = authors_titles_by_url_to_coauthor_edge(dic)
        writer = csv.writer(intitute_csv_file)
        writer.writerows(authors_json)  
        print("esperando")
        time.sleep(50)