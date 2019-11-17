#imports
import csv
import json
from tools.dblp_author_url_serch import *
#from .tools.dblp_author_url_serch import *

 #declare paths
institute_author_json_path ='data/institutes/All_authors_titles.json'
institute_coauthors_edges_path = 'data/institutes/authors_titles_'
#read json authors and extract coauthors
authors_json=[]

institutes_dict={}

with open(institute_author_json_path)as authors_titles_file_json:
    authors_titles_json = json.loads(authors_titles_file_json.read())

    for key,val in authors_titles_json.items():
        if val['afiliation'] in institutes_dict:
            institutes_dict[val['afiliation']][key]=val
        else:
            institutes_dict[val['afiliation']]={key:val}
            
    authors_json = authors_titles_by_url_to_coauthor_edge(authors_titles_json)

for inst in institutes_dict.keys():
    authors_json = authors_titles_by_url_to_coauthor_edge(institutes_dict[inst])
    with open(institute_coauthors_edges_path+inst+'.csv','w')as intitute_csv_file:
    #for author,coauthor in authors_json:   
        writer = csv.writer(intitute_csv_file)
        writer.writerows(authors_json)  

print(institutes_dict)

print(authors_json)
with open(institute_coauthors_edges_path+'.csv','w')as intitute_csv_file:
    #for author,coauthor in authors_json:   
    writer = csv.writer(intitute_csv_file)
    writer.writerows(authors_json)    





