'''
	Scraper to get researcher names from https://research.fb.com/people/ website
'''
from bs4 import BeautifulSoup
import requests
import os
import csv
import json

org = 'Facebook'
count_pages = 35

def get_url_scholar_google(content):
    soup = BeautifulSoup(content, 'html.parser')
    div = soup.find('div', class_='col-12 col-4-lrg hide-on-mobile')
    links = div.find_all('a', class_='btn btn--blue')
    res = None
    for link in links:
        if (link['href'][:22]=='https://scholar.google'):
            res = link['href']
    return res

save_csv= os.getcwd()+'/data/facebook/facebook_authors.csv'
save_csv_not_found= os.getcwd()+'/data/facebook/facebook_authors_not_found.csv'
save_json= os.getcwd()+'/data/facebook/facebook_authors.json'
authors_list = []
authors_list_not_found = []
authors_json = {}
count = 0
for i in range(count_pages):
    url = 'https://research.fb.com/people/page/'+str(i+1)+'/?paginated=true'
    response = requests.request("GET",url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a', 'clearfix'):
        print(a['title'])
        print(a['href'])
        count = count + 1
        url_profile = a['href']
        response_profile = requests.request('GET', url_profile)
        soup_profile = BeautifulSoup(response_profile.content, 'html.parser')
        div = soup_profile.find('section', class_='grid card-wrapper latest-publication-section')        
        if not (div is None):
            # Have lastest publications section
            print('Lastest')
            publications = []
            authors_json[a['title']] = {}
            pub = div.find_all('a')
            for link in pub:
                publications.append(link['title'])
            authors_json[a['title']]['publications'] = publications
            authors_json[a['title']]['afiliation'] = org
            authors_list.append([a['title'], org])
        elif not (get_url_scholar_google(response_profile.content) is None):
            print('Scholar google')
            # See if have link to google scholar
            url_scholar_google = get_url_scholar_google(response_profile.content)            
            authors_json[a['title']] = {}
            publication = []
            res_g = requests.request('GET', url_scholar_google)
            s_g = BeautifulSoup(res_g.content, 'html.parser')
            links = s_g.find_all('a', class_='gsc_a_at')      
            for link in links:
                publications.append(link.string)
            authors_json[a['title']]['publications'] = publications
            authors_json[a['title']]['afiliation'] = org
            authors_list.append([a['title'], org])
        else:
            print('Not found')
            # Researcher not have publications
            authors_list_not_found.append([a['title'], org])

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