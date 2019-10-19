import os
import glob
import csv

extension = 'csv'
type ='authors'
path= os.getcwd()+'/data'
file_all_authors=path+'/Authors.csv'

print(path)
files_csv=[]
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        print(file,"added")
        if extension in file and type in file:
            files_csv.append(os.path.join(r, file))



for author_file in files_csv:
    with open(author_file,'r') as author: 
        csv_reader = csv.reader(author, delimiter=',')
        with open(file_all_authors,'a') as file_save:
            writer = csv.writer(file_save)
            writer.writerows(csv_reader)                     