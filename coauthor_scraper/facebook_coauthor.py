#imports
import csv
import json
from tools.dblp_author_url_serch import *
import time


 #declare paths
facebook_author_json_path ='data/facebook/facebook_authors_titles.json'
facebook_coauthors_edges_path = 'data/facebook/authors_titles_facebook.csv'
#read json authors and extract coauthors
authors_json=[]



with open(facebook_author_json_path)as authors_titles_file_json:
    authors_titles_json = json.loads(authors_titles_file_json.read())


authors_json = authors_titles_by_url_to_coauthor_edge(authors_titles_json)
with open(facebook_coauthors_edges_path,'a')as intitute_csv_file:
#for author,coauthor in authors_json:
    
    
    writer = csv.writer(intitute_csv_file)
    writer.writerows(authors_json)  