#serch author by url
import requests
import json

institutu_author_json_path ='data/institutes/All_authors_titles.json'
#Request URL: https://dblp.uni-trier.de/search/publ/api?
# callback=jQuery311006330389956735472_1573771797215&
# q=author%3AMartial_Hebert%3A&
# compl=type&
# p=2&
# h=0&
# c=10&
# format=jsonp&
# _=1573771797217

def urldblp_to_coauthorurl(url):
    url_base='https://dblp.uni-trier.de/search/publ/api?callback=jQuery311006330389956735472_1573771797215&'
    comp='compl=author&'
    p='p=2&'
    h='h=0&'
    c='c=10&'
    format='format=json&'
    #callback='callback=jQuery311006330389956735472_1573771797215&'
    url_array = url.split('/')
    name = url_array[6]
    name=name.split(':')
    name=name[1]+'_'+name[0]
    q='author%3A'+name+'%3A&'
    #concatenate name url
    #url_coauthor='https://dblp.uni-trier.de/search/publ/api?compl=author&q=author%3A'+name+'%3A&format=jsonp'
    url_coauthor = url_base+q+comp+p+h+c+format
    return url_coauthor

def get_json_by_url(url):
    response = requests.request("GET", url)
    j = json.loads(response.content)
    return j

def get_coauthor(author,coworkers):
    result=[]
    for worker in coworkers:
        worker_name = worker['text'].split(':')[3]
        if worker_name!=author:
            result.append(worker_name)
    return result

def get_name_in_json(json_author):
    return json_author['result']['completions']['c'][0]['text'].split(':')[3]

def get_names_coauthors_in_json(json_author):
    return json_author['result']['completions']['c']

def create_coauthor_json(json_author):
    coauthor_json={}
    name = get_name_in_json(json_author)
    coworker_data = get_names_coauthors_in_json(json_author)
    coworkers =  get_coauthor(name,coworker_data)
    coauthor_json[name]=coworkers
    return coauthor_json

def coautor_list_to_edge(coauthors):
    result=[]
    for key,value in coauthors.items():
        result = [(key,val) for  val in value]
    return result

def authors_titles_by_url_to_coauthor_edge(authors_titles_json):
    edges=[]
    errors=[]
    for values in authors_titles_json.values():
        if 'dblp_url' in values.keys():
            print(values['name'])
            url = urldblp_to_coauthorurl(values['dblp_url'])
            json_author = get_json_by_url(url)
            coauthor_json = create_coauthor_json(json_author)
            edge = coautor_list_to_edge(coauthor_json)
            edges.extend(edge)
        else:
            print('error',(values['name'])
)
            errors.append(('error',values))
    return edges

url_dblp = 'https://dblp.uni-trier.de/pers/hd/l/Lo:Andrew'
url_dblp2='https://dblp.uni-trier.de/pers/hd/h/Hebert:Martial'
url_test='https://dblp.uni-trier.de/pers/hd/s/Smaragdis:Paris'

# url = urldblp_to_coauthorurl(url_test)
# json_author = get_json_by_url(url)
# coworkers=json_author['result']['completions']['c']
# name=json_author['result']['completions']['c'][0]['text'].split(':')[3]
#print(get_coauthor(name,coworkers))
#print(get_name_in_json(json_author))
#print(create_coauthor_json(json_author))
#print(coautor_list_to_edge(create_coauthor_json(json_author)))



# with open(institutu_author_json_path)as authors_titles_file_json:
#     authors_titles_json = json.loads(authors_titles_file_json.read())
#     authors_json = authors_titles_by_url_to_coauthor_edge(authors_titles_json)
#     with open()
#     for edge in authors_json:
#         print(edge)




