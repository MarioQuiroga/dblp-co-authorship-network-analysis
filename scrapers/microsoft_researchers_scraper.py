'''
	Scraper to get researcher names from https://www.microsoft.com/en-us/research/people/ website
'''
import json
import requests
import os
import csv

def get_url_publications(content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    script = soup.find_all('div', class_="publications-accordion")
    spl = str(script).split('\'')
    return spl[len(spl)-2]

def get_publications(content):
    import json
    json_pub = json.loads(content)
    pubs = json_pub['content']['publications']
    res = []
    for key, pub in pubs.items():
        res.append(pub['title'])
    return res
    

save_csv= os.getcwd()+'/data/microsoft/microsoft_authors.csv'
save_csv_not_found= os.getcwd()+'/data/microsoft/microsoft_authors_not_found.csv'
save_json= os.getcwd()+'/data/microsoft/microsoft_authors_titles.json'
org = 'Microsoft'
print('Microsoft')
authors_list = []
authors_json = {}
authors_not_founds = []
more_pages = True
cur_page = 1
count_not_found = 0
count = 0
while(more_pages):
    url = 'https://www.microsoft.com/en-us/research/wp-json/microsoft-research/v1/researchers?type_search=&search=&paged='+str(cur_page)+'&item_template=person'
    response = requests.request('GET', url)
    json_content = json.loads(response.content)
    more_pages = json_content['more_pages']
    cur_page = cur_page + 1
    for i in json_content['researchers']:
        count = count + 1
        # Get json publications if exists page
        print(i['display_name'])
        profile_url = i['profile_url'] + 'publications'    
        print(profile_url)    
        publications = requests.request('GET', profile_url)
        if publications.status_code == 200:            
            url_json_publications = get_url_publications(publications.content)
            if (len(url_json_publications)>2):
                json_content_response = requests.request('GET', url_json_publications)
                if (str(json_content_response.content.decode("utf-8"))!='""'):
                    publications_list = get_publications(json_content_response.content)                        
                    authors_list.append([i['display_name'], org])
                    authors_json[i['display_name']] = {}
                    authors_json[i['display_name']]['publications'] = publications_list
                    authors_json[i['display_name']]['afiliation'] = org
                    print('Found:', i['display_name'])
                else:
                    authors_not_founds.append([i['display_name'], org])
                    count_not_found = count_not_found + 1

print('Total', count)
print('Found authors: ',len(authors_list))
print('Authors whitout publications', count_not_found)
with open(save_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authors_list)

with open(save_csv_not_found, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authors_not_founds)

with open(save_json, 'w') as f:
    json.dump(authors_json, f) 
