import requests
import csv
from bs4 import BeautifulSoup
import re
import dryscrape
import os
import json
import unicodedata as ud

#parameters
url = "http://csrankings.org/csrankings.csv"
url_index= 'http://csrankings.org/#/index?all&world'
folder = "data/institutes"
type='authors'

authors_titles = os.getcwd()+'/data/institutes/All_authors_titles.json'

Institutes=['Carnegie Mellon University','Massachusetts Institute of Technology','Univ. of Illinois at Urbana-Champaign']


Institutes_athorships={} 
#list of tuples (authors intitute) 
author_institute_csv=[]
#dblp url's dic 
authors_dblp={}
#json authors description
csRanking_authors={}

#request to csranking
payload = ""
response = requests.request("GET", url, data=payload)

author_decoded = response.content

authors_csv = csv.reader(author_decoded.splitlines(), delimiter=',')

def name_normalize(name):
    
    name = re.sub(r'\([^()]*\)', '',name)
    #ud.normalize('NFD', str(name)).encode('ascii', 'ignore').decode()
    name.replace(r'(([A-Za-z]+))\.',' ')
    name = re.sub(r'[^A-Za-z]+', ' ',name)
    name = name.replace('   ',' ')
    name = name.replace('  ',' ')
    return name.rstrip()


#transformation

for institute in Institutes:
    Institutes_athorships[institute]=[]

#authors_list = list(authors_csv)

for author in list(authors_csv):
    
    if len(author) > 0:
        if author[1] in Institutes:
            #print(author[0],author[1],"csv")
            Institutes_athorships[author[1]].append(name_normalize(author[0]))
            


for institute,authors in Institutes_athorships.items():
    # print(institute,authors)
    for author in authors:     
        author_institute_csv.append((author,institute))
    #print(author_institute_csv)
    institute_name = institute.replace(' ', '')
    

    with open (folder+'/'+institute_name+"_" +type+".csv",'wb') as institute_file:
        csv_out=csv.writer(institute_file)
        for row in author_institute_csv:
            print(row)
            if institute == row[1]:
                csv_out.writerow(row)

    #     writer = csv.writer(institute_file)
    #     writer.writerows(author_institute_csv)             
    # institute_file.close()     

# for author,inst in author_institute_csv:
#     print(author,inst,"casa")


session = dryscrape.Session()
session.visit(url_index)
response = session.body()
soup = BeautifulSoup(response,features="lxml")

institute_name=""
for tr in soup.find_all("tr"):
    for a in tr.find_all('a',href=True):
        if a.text:
            #filter numeber 
            if not re.match("^[0-9 -]+$", a.text):
                author = a.text
            else:
                author=''
        if 'dblp' in a['href'] and author not in '':
            authors_dblp[name_normalize(author)]=a['href']
            #(a['href'],author)


for author,institute in author_institute_csv:
    data={}
    if name_normalize(author) in authors_dblp.keys():
        data['name']=author
        data['dblp_url']=authors_dblp[name_normalize(author)]
        data['afiliation']=institute
        
    else:
        data['name']=author
        #data['dblp_url']=authors_dblp[name_normalize(author)]
        data['afiliation']=institute

    csRanking_authors[author]=data

for institute in Institutes:
    with open(authors_titles, 'w') as jsonfile:
        json.dump(csRanking_authors, jsonfile)

print('finished')