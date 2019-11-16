#imports
import json
from tools.dblp_author_url_serch import *
#from .tools.dblp_author_url_serch import *

 #declare paths
institute_author_json_path ='data/institutes/All_authors_titles.json'
institute_coauthors_edges_path = 'data/institutes/All_authors_titles.csv'
#read json authors and extract coauthors
authors_json=[]
with open(institute_author_json_path)as authors_titles_file_json:
    authors_titles_json = json.loads(authors_titles_file_json.read())
    authors_json = authors_titles_by_url_to_coauthor_edge(authors_titles_json)

with open(institute_coauthors_edges_path,'wb')as intitute_csv_file:
    for edge in authors_json:
        # print(edge)



