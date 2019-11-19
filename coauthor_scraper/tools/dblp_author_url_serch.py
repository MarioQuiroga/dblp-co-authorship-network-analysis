#serch author by url
import requests
import json
import dryscrape
from bs4 import BeautifulSoup
import jellyfish


#institutu_author_json_path ='data/institutes/All_authors_titles.json'
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

    url_base='https://dblp.uni-trier.de/search/publ/api?'
    comp='compl=author&'
    p='p=2&'
    h='h=0&'
    c='c=10&'
    format='format=json&'
    url_array = url.split('/')
    print(url_array,url)
    name = url_array[6]
    name=name.split(':')
    name=name[1]+'_'+name[0]
    name = name.replace("=",".")
    q='q=author%3A'+name+'%3A&'
    url_coauthor = url_base+q+comp+p+h+c+format
    return url_coauthor

def get_json_by_url(url):
    response = requests.request("GET", url)
    content = response.content
    j = json.loads(content)
    return j

def get_coauthor(author,coworkers):
    result=[]
    for worker in coworkers:
        worker_name = worker['text'].split(':')[3]
        
        if worker_name!=author:
            a = int(worker['@oc'])
            #for i in range(1,a):
                #<print(worker_name)
            result.append([worker_name,a])
    return result

def get_name_in_json(json_author):
    if "c" in json_author['result']['completions'].keys():
        return json_author['result']['completions']['c'][0]['text'].split(':')[3]
    else:
        return False

def get_names_coauthors_in_json(json_author):   
    if "c" in json_author['result']['completions'].keys(): 
        return json_author['result']['completions']['c']
    else:
        return []    

def create_coauthor_json(json_author):
    coauthor_json={}
    name = get_name_in_json(json_author)
    coworker_data = get_names_coauthors_in_json(json_author)
    coworkers =  get_coauthor(name,coworker_data)
    coauthor_json[name]=coworkers
    return coauthor_json

def coautor_list_to_edge(name,coauthors):
    result=[]
    result = [[name,val,count] for  val,count in coauthors]
    return result

def authors_titles_by_url_to_coauthor_edge(authors_titles_json):
    edges=[]
    errors=[]
    for values in authors_titles_json.values():
        if 'dblp_url' in values.keys():
            url = urldblp_to_coauthorurl(values['dblp_url'])
            json_author = get_json_by_url(url)
            name = get_name_in_json(json_author)
            if name:
                coworkers=get_names_coauthors_in_json(json_author)           
                coworkers=get_coauthor(name,coworkers)
                edge = coautor_list_to_edge(name,coworkers)
                edges.extend(edge)
            else:
                print("name not found")
        elif('publications'in values.keys()):
            #mejorar la busqueda por publicaciones a intentar en otro titulo si no hay 100%
            title = values['publications'][0]
            title = title.replace('–','')
            print("title",title)
            authors = get_authors_titles(title)
            if authors:
                dblp_url = get_author_url_comparing_name(values['original_name'],authors)
                url = urldblp_to_coauthorurl(dblp_url)
                json_author = get_json_by_url(url)
                name = get_name_in_json(json_author)
                if name:
                    coworkers=get_names_coauthors_in_json(json_author)           
                    coworkers=get_coauthor(name,coworkers)
                    edge = coautor_list_to_edge(name,coworkers)
                    edges.extend(edge)
            else:
                print("name not found")
            #print('error',(values['name']))
            #errors.append(('error',values))
    return edges




#function to search title
def get_authors_titles(title):
    url_base = 'https://dblp.uni-trier.de/search/publ?q='
    #query='Estimating the size of online social networks'
    query=title
    url_query=url_base+query
    session = dryscrape.Session()
    session.visit(url_query)
    response = session.body()
    soup = BeautifulSoup(response,features="lxml")
    span =soup.find_all("span",{"itemprop":"author"})
    
    authors=[]
    for a in span:
        ahref=a.find("a")['href']
        aname=a.find("a").text
        authors.append([aname,ahref])
    return authors

def get_author_url_comparing_name(name, name_url_list):
    max_sim=0
    url_author=''
    for author in name_url_list:
        if name == author[0]:
            return author[1]
        else:
            distance= jellyfish.jaro_distance(name,author[0])
            if distance > max_sim:
                max_sim=distance
                url_author = author[1]
    return url_author