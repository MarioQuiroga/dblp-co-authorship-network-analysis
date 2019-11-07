import requests
import csv
from bs4 import BeautifulSoup
import re
import dryscrape
#parameters
url = "http://csrankings.org/csrankings.csv"
url_index= 'http://csrankings.org/#/index?all&world'
folder = "data/institutes"
type='authors'

Institutes=['Carnegie Mellon University','Massachusetts Institute of Technology','Univ. of Illinois at Urbana-Champaign']

Institutes_athorships={} 


#request to csranking
payload = ""
response = requests.request("GET", url, data=payload)

author_decoded = response.content

authors_csv = csv.reader(author_decoded.splitlines(), delimiter=',')

#transformation

for institute in Institutes:
    Institutes_athorships[institute]=[]

authors_list = list(authors_csv)

for author in authors_list:
    if len(author) > 0:
        if author[1] in Institutes:
            Institutes_athorships[author[1]].append(author[0])
            

for intitute in Institutes_athorships.keys():
    
    authrs_in_institutes= Institutes_athorships[institute]
    # add intitute name at each author
    author_institute_csv = [ (author,intitute ) for author in authrs_in_institutes]
    
    institute_name = intitute.replace(' ', '')
    #save in file the institute authors

    with open (folder+'/'+institute_name+"_" +type+".csv",'wb') as institute_file:
        writer = csv.writer(institute_file)
        writer.writerows(author_institute_csv)             
    institute_file.close()     

session = dryscrape.Session()
session.visit(url_index)
response = session.body()
soup = BeautifulSoup(response,features="lxml")
#soup.find_all("a",'href')

#for author ,institute in author_institute_csv:
for tr in soup.find_all("tr"):

    for a in tr.find_all('a',href=True):
        if a.text:
            if not re.match("^[0-9 -]+$", a.text):
                author = a.text
            else:
                author=''
        if 'dblp' in a['href'] and author not in '':
                print(a['href'],author)
                

            
