'''
	Scraper co-authorship network in dblp: https://dblp.org/
'''
import csv
import os
import time
import requests
from bs4 import BeautifulSoup as Soup
import json

SPECIAL_CHARS = ['"', '“', '”', '\'', '’', '´', '-', '_', '(', ')', '.', '[', ']', ':', ';', ',','–', '|', '°', '¬', '!', '\\','?','¿','¡', '朱', '曉', '耕', '&', '鄭','又','中']

# Read csv data
csv_file = os.getcwd()+'/data/google/google_authors.csv'
save_csv= os.getcwd()+'/data/edges_list/google.csv'
save_csv_not_founds = os.getcwd()+'/data/not_founds_names_google.csv'
rows = []
with open(csv_file, 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        rows.append(row)

# Scraping coautorship rows
names, inst = zip(*rows)
not_founds = []
edges_list = []
for row in rows:
    # Search in dblp
    
    for char in SPECIAL_CHARS:
        row[0] = row[0].replace(char, ' ')    
    row[0] = row[0].replace('  ',' ')
    spl = row[0].split(' ')
    if len(spl) > 1:
        name = spl[0].strip()
        last = spl[1].strip()
        print(row[0])
        url = 'https://dblp.org/search/author/api?q='+row[0]+'&format=json'
        print('Search:', url)
        response = requests.request('GET', url)
        json_content = j = json.loads(response.content)
        url_author = ''
        if int(j['result']['hits']['@total']) != 0:
            # Scrap coautorship user
            url_author = j['result']['hits']['hit'][0]['info']['url']+'.xml'
            response_coaut = requests.request('GET', url_author)
            if response_coaut.status_code == 200:
                # Get author url
                url_author = response_coaut.history[len(response_coaut.history)-1].headers['Location']
                # Get coauthor url
                #print(url_author)
                url_coauthors = url_author.replace('xx','xc') + '.xml'
                print('Url coauthors',url_coauthors)
                response_coaut = requests.request('GET', url_coauthors)
                print('name found')
                #print(response_coaut.content)
                for author in Soup(response_coaut.content.decode()).find_all('author'):
                    if row[0] in names:
                        edges_list.append([row[0], author.string, author['count']])
                        print(row[0], author.string, author['count'])   
        else:
            print('Search not found')
            not_founds.append([row[0],row[1]])
        time.sleep(1)
    else:
        print('Bad name')
        not_founds.append([row[0],row[1]])
    

# Store data
with open(save_csv_not_founds, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(not_founds)

with open(save_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(edges_list)

print('success')
