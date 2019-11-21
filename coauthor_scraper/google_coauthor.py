#imports
# import csv
# import json
# from tools.dblp_author_url_serch import *

#get authors from file json

# title_search = "Estimating the size of online social networks"
# author = "Shaozhi Ye"
# author = "eYS ohahzi"
#json_auth='{"Ashwin Ganti": {"original_name": "Ashwin Ganti", "afiliation": "Google", "url_titles": "https://ai.google/research/people/author37533", "is_diferent": true, "publications": ["Plan 9 Authentication in Linux"]}}'
# json_auth = json.loads(json_auth)
# print (get_authors_titles('itle Crafting a lexicon of referential expressions for NLG applications'))
# a = get_authors_titles('Plan 9 Authentication in Linux')
# print(a)
# b= get_author_url_comparing_name(author,a)
#print(b)
# print(authors_titles_by_url_to_coauthor_edge(json_auth))

#imports
import csv
import json
from tools.dblp_author_url_serch import *
import time


 #declare paths
google_author_json_path ='data/google/google_authors_titles.json'
google_coauthors_edges_path = 'data/google/authors_titles_google.csv'
#read json authors and extract coauthors
authors_json=[]


# def chunks(data, SIZE=10000):
#     it = iter(data)
#     for i in range(0, len(data), SIZE):
#         yield {k:data[k] for k in islice(it, SIZE)}



with open(google_author_json_path)as authors_titles_file_json:
    authors_titles_json = json.loads(authors_titles_file_json.read())


dic_aux={}
dic1=dict(list(authors_titles_json.items())[:300])
dic2=dict(list(authors_titles_json.items())[301:600])
dic3=dict(list(authors_titles_json.items())[601:900])
dic4=dict(list(authors_titles_json.items())[901:1200])
dic5=dict(list(authors_titles_json.items())[1201:1500])
dic6=dict(list(authors_titles_json.items())[1501:1800])
dic7=dict(list(authors_titles_json.items())[1801:])
dic8 = dict(list(authors_titles_json.items())[1761:1800])
#listos dic1 dic2 dic3 dic 4 dic5 dic6
dics=[dic1, dic2, dic3, dic4, dic5, dic6,dic7]

with open(google_coauthors_edges_path,'a')as intitute_csv_file:
#for author,coauthor in authors_json:
    for dic in dics:
        authors_json = authors_titles_by_url_to_coauthor_edge(dic)
        writer = csv.writer(intitute_csv_file)
        writer.writerows(authors_json)  
        print("esperando")
        time.sleep(50)


