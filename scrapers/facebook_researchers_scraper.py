'''
	Scraper to get researcher names from https://research.fb.com/people/ website
'''
from bs4 import BeautifulSoup
import requests
import os
import csv

org = 'Facebook'
count_pages = 35

save_csv= os.getcwd()+'data/facebook/facebook_authors.csv'
authors = []
for i in range(count_pages):
    url = 'https://research.fb.com/people/page/'+str(i+1)+'/?paginated=true'
    response = requests.request("GET",url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a', 'clearfix'):
        authors.append([a['title'], org])

print(len(authors))
with open(save_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authors)

