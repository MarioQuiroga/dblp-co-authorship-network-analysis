import json
import requests
import os
import csv
import dryscrape
import time
import re
import unicodedata as ud

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver
from bs4 import BeautifulSoup
from typing import Sized, Iterable, Iterator

#publicatios url
url_publications='https://ai.google/static/data/publications.json'
#authors url 
url = "https://ai.google/static/data/authors.json"
#save name organization
organitation= 'Google'
#url base to get papers title 
url_titles = 'https://ai.google/research/people/'
#os.getcwd()
#publications json
publications_json = os.getcwd()+'/data/google/publications.json'
#json file 
authors_titles = os.getcwd()+'/data/google/google_authors_titles.json'
#json authors titles 
savefile = os.getcwd()+'/data/google/google_authors.json'
#csv file (name,organitation)
savecsv= os.getcwd()+'/data/google/google_authors.csv'

def google_authors_titles(dic_publications):
    authors_pub={}
    for pub in dic_publications['publications']:
        
        for author in pub['authors']:
            normalize_author = name_normalize(author['name'])
            if normalize_author in authors_pub.keys():
                if author['at_google']:
                    authors_pub[normalize_author].append(pub['title'])
            else:
                if author['at_google']:
                    authors_pub[normalize_author]=[pub['title']]
    return authors_pub

def name_normalize(name):
    name = re.sub(r'\([^()]*\)', '',name)
    name = re.sub(r'[^A-Za-z]+', ' ', ud.normalize('NFD', name).encode('ascii', 'ignore').decode())
    name = name.replace('  ',' ')
    return name

response = requests.request("GET", url)
print(response.status_code)
content =response.content
jsoncontent = json.loads(content)

with open(savefile, 'wb') as f:
    f.write(content)
print("file saved")


authors_json={}
authorscsv=[]
for author in jsoncontent['authors']:
    data = {}
    path_author = author['filename_html'].replace('.html','')
    name = name_normalize(author['name'])
    authorscsv.append([name,organitation])
    data['afiliation']=organitation
    data['url_titles']= url_titles+path_author
    authors_json[name]=data


response = requests.request("GET", url_publications)
print(response.status_code)
content =response.content
jsoncontent = json.loads(content)
publications_authors = google_authors_titles(jsoncontent)

with open(authors_titles, 'w') as jsonfile:
    json.dump(authors_json, jsonfile) 


with open(publications_json, 'w') as jsonfile:
    json.dump(publications_authors, jsonfile) 

i=1
s=1
for author,pubs in publications_authors.items():
    if author in authors_json.keys():
        authors_json[author]['publications']=pubs
        #print(author)
        print("CORRECTO:",author,"CON",s)
        s+=1
    else:
        print("ERROR:",author,"CON",i)
    i+=1
print(s)
with open(savecsv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authorscsv)    



