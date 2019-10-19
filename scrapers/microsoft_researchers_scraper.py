'''
	Scraper to get researcher names from https://www.microsoft.com/en-us/research/people/ website
'''
import json
import requests
import os
import csv

save_csv= os.getcwd()+'data/microsoft/microsoft_authors.csv'
org = 'Microsoft'
authors = []
more_pages = True
cur_page = 1
while(more_pages):
    url = 'https://www.microsoft.com/en-us/research/wp-json/microsoft-research/v1/researchers?type_search=&search=&paged='+str(cur_page)+'&item_template=person'
    response = requests.request('GET', url)
    json_content = json.loads(response.content)
    more_pages = json_content['more_pages']
    cur_page = cur_page + 1
    for i in json_content['researchers']:
        authors.append([i['display_name'], org])
        print(i['display_name'])
print(len(authors))
with open(save_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authors)
