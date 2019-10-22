'''
	Scraper co-authorship network in dblp: https://dblp.org/
'''
import csv
import os
import time
import requests
from bs4 import BeautifulSoup as Soup

# Read csv data
csv_file = os.getcwd()+'/../data/Authors.csv'
save_csv= os.getcwd()+'../data/edges_list.csv'
save_csv_not_founds = os.getcwd()+'../data/not_founds_names.csv'
rows = []
with open(csv_file, 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        rows.append(row)

# Scraping coautorship rows
names, inst = zip(*rows)
not_founds = []
edges_list = []
#print(names)
for row in rows:
    spl = row[0].split(' ')
    if len(spl) > 1:
        name = spl[0]
        last = spl[1]
        url = 'https://dblp.org/pers/xc/'+last[0].lower()+'/'+last+':'+name+'.xml'
        print(url)
        response = requests.request('GET', url)
        if response.status_code == 200:
            for author in Soup(response.content.decode()).find_all('author'):
                if row[0] in names:
                    edges_list.append([row[0], author.string, author['count']])
                    print(row[0], author.string, author['count'])
        else:
            not_founds.append([row[0],row[1])
        time.sleep(2)
    else:
        not_founds.append([row[0],row[1])

with open(save_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(not_founds)

with open(save_csv_not_founds, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(edges_list)
