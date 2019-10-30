import json
import requests
import os
import csv

url = "https://ai.google/static/data/authors.json"
organitation= 'Google'
url_titles = 'https://ai.google/research/people/'
os.getcwd()

#json file 
savefile = os.getcwd()+'/data/google/google_authors.json'
#csv file (name,organitation)
savecsv= os.getcwd()+'/data/google/google_authors.csv'

response = requests.request("GET", url)

print(response.status_code)
print(response.headers['content-type'])
print(response.encoding)

content =response.content
jsoncontent = json.loads(response.content)

with open(savefile, 'wb') as f:
    f.write(response.content)
print("file saved")


authors_json={}
authorscsv=[]
for author in jsoncontent['authors']:
    data = {}
    authorscsv.append([author['name'],organitation,author['filename_html']])
    data['afiliation']=organitation
    data['html']=author['filename_html']
    authors_json[author['name']]=data
    print(author['name'],organitation,author['filename_html'])

with open(savecsv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authorscsv)    



