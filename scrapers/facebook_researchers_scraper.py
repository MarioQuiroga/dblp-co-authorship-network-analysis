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
save_csv_not_found= os.getcwd()+'data/facebook/facebook_authors_not_found.csv'
save_json= os.getcwd()+'data/facebook/facebook_authors.json'
authors_list = []
authors_list_not_found = []
authors_json = {}
count = 0
for i in range(count_pages):
    url = 'https://research.fb.com/people/page/'+str(i+1)+'/?paginated=true'
    response = requests.request("GET",url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a', 'clearfix'):
        count = count + 1
        url_profile = [a['href']
        response_profile = requests.request('GET', url_profile)
        soup_profile = BeautifulSoup(response_profile.content, 'html.parser')
        div = soup.find('section', class_='grid card-wrapper latest-publication-section')        
        if (div is not None):
            # Have lastest publications section
            publications = []
            authors_json[a['title']] = {}
            pub = div.find('a')
            for link in pub:
                publications.append(link['title'])
            authors_json[a['title']]['publications'] = publications
            authors_json[a['title']]['afiliation'] = org
            authors_list.append([a['title'], org])
        elif:
            # See if have link to google scholar

        else:
            # Researcher not have publications
            authors_list_not_found.append(a['title'], org)


print('Total:', count)
print('Found authors: ',len(authors_list))
print('Authors whitout publications', len(authors_list_not_found))
with open(save_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authors_list)

with open(save_csv_not_found, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authors_list_not_found)

with open(save_json, 'w') as f:
    json.dump(authors_json, f) 