import unicodedata as ud
import csv
import os

path= os.getcwd()+'/data'
file_all_authors=path+'/Authors.csv'
file_all_authors_save=path+'/Authoers_normalize.csv'
normalize_authors=[]

with open(file_all_authors,'r')as authors:
    csv_reader = csv.reader(authors, delimiter=',')
    for author in csv_reader:
        normalize_authors.append((ud.normalize('NFD', author[0]).encode('ascii', 'ignore').decode(),author[1]))

with open(file_all_authors_save,'w') as file_save:
    for author,org in normalize_authors:
        file_save.write(author+','+org+'\n')