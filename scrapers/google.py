import json
import requests
import os
import csv

url = "https://ai.google/static/data/authors.json"
organitation= 'Google'
os.getcwd()

#json file 
savefile = os.getcwd()+'/../Data/google/google_authors.json'
#csv file (name,organitation)
savecsv= os.getcwd()+'/../Data/google/google_authors.csv'

response = requests.request("GET", url)

print(response.status_code)
print(response.headers['content-type'])
print(response.encoding)

content =response.content
jsoncontent = json.loads(response.content)

authorscsv=[]
for author in jsoncontent['authors']:
    authorscsv.append([author['name'],organitation])
    print(author['name'],organitation)

with open(savecsv, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(authorscsv)    


with open(savefile, 'wb') as f:
    f.write(response.content)
print("file saved")

