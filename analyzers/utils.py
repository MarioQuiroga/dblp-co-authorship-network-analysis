import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from os import scandir, getcwd

def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]


def load_networks(path):
    files = ls(path)
    graphs = {}
    full = nx.Graph()
    
    for file in files:
        name = file.split('_')[-1].split('.')[0]
        g = nx.read_weighted_edgelist(path+'/'+file, delimiter=',')        
        coauthors = set()
        full = nx.compose(full, g)
        with open(path+'/'+file) as f:
            lines = f.readlines()
            for line in lines:
                author = line.split(',')[0]
                coauthors.add(author)
            g = g.subgraph(coauthors)            
        graphs[name] = g   
        
    coauthors = set()    
    for _, graph in graphs.items():
        for coauthor in graph.nodes():
            coauthors.add(coauthor) 
    full_filtred = full.subgraph(coauthors)
        
    graphs['Todas'] = full_filtred
    return graphs

'''
    Structural properties
'''
# Average degree
def compute_avg_degree(g):
    degress = g.degree()
    s = 0
    for _, d in degress:
        s = s + d
    return s/len(degress) 

# Compute histogram
def hist(array, bins):
    b = dict()
    for bin in bins:
        b[bin] = 0
    for a in array:
        b[a] = b[a] + 1
    return zip(*b.items())

# SCC 
def compute_scc(g):
    largest_cc = max(nx.connected_components(g), key=len)
    m_scc = g.subgraph(largest_cc)
    '''
    #scc = nx.weakly_connected_component_subgraphs(g)
    # Select max SCC 
    m_scc = []
    count = 0
    for x in scc:
        count = count + 1
        if len(x) > len(m_scc):
            m_scc = x
    print("Cantidad de componentes fuertemente conectados:", count)
    print("El componente gigante tiene", str(len(m_scc)), "nodos")
    '''
    return m_scc

# Distribución de grado
def compute_degree_distribution(name,graph):
    degrees = [i for _, i in graph.degree()]
    for _, i in graph.degree():
        degrees.append(i)
    bins, dist = hist(degrees, np.arange(max([d for n, d in graph.degree()])+1))
    x = []
    y = []
    # Remove values in zero
    for i in range(0, len(dist)):
        if (int(dist[i]) != 0) and (bins[i] != 0):
            x.append(bins[i])
            y.append(dist[i])
    # Exponente de la power law
    
    # Log scale
    log_x = np.log(x)
    log_y = np.log(y)

    # Compute model(curva ajustada) polyfit numpy
    # ajuste = np.polyfit(x log, y log, grado del polinomio = 1) retorna los coeficientes del polinomio [coef grado 1 alfa, coef grado 0 c]
    ajuste = np.polyfit(log_x, log_y, deg=1)
    rect = np.poly1d(ajuste) #internamente representa un polinomio 
    #print("Recta de ajuste:", rect)
    print("Exponente de la power law: %2.3f" %(rect[1]))
    
    # Gráfico del ajuste
    #y_pred = rect(log_x)
    plt.title("Histograma de grado " + name) 
    plt.xlabel("k") 
    plt.ylabel("Cantidad") 
    plt.bar(x,y) 
    #plt.plot(log_x, log_y, log_x, y_pred) 
    #plt.legend(('Curva real', 'Curva ajustada'),
    #prop = {'size':10}, loc = 'upper right')
    plt.show()

    
# Distribucion coeficiente de clustering
def compute_coef_clustering_distribution(name,graph):
    clusterings = nx.clustering(graph)
    keys, values = zip(*clusterings.items())
    seq = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    hist, bins = np.histogram(values, bins=seq)
    plt.title("Distribución del coeficiente de clustering " + name) 
    plt.xlabel("Coeficiente de clustering") 
    plt.ylabel("Cantidad") 
    plt.plot(bins[:-1], hist) 
    plt.show()    

    
# Distribucion coeficiente de clustering
def compute_coef_clustering_distributions(graphs):    
    names = []    
    seq = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for name, g in graphs.items():
        clusterings = nx.clustering(g)
        keys, values = zip(*clusterings.items())
        hist, bins = np.histogram(values, bins=seq)
        plt.plot(bins[:-1], hist) 
        names.append(name)
    plt.title("Comparación distribución del coeficiente de clustering ") 
    plt.xlabel("Coeficiente de clustering") 
    plt.ylabel("Cantidad") 
    plt.legend(names, prop = {'size':10}, loc = 'upper right')
    plt.show()    

    
'''
    Most important
'''
def most_important_authors(name, graph, top):
    # Degree centrality
    print("Grafo:", name)
    degrees = graph.degree(weight='weight')
    sorted_degrees = sorted(degrees, key=lambda degree: degree[1],reverse = True)
    print("Top "+str(top)+" de autores por su grado")
    print("Autor , Grado")
    for i in range(0,top):
      print(sorted_degrees[i])    
    print("-----------------------------------------")
    # PageRank centrality
    a = 0.3
    pr = nx.pagerank(graph, alpha=a)
    sorted_pr = sorted(pr, key=pr.__getitem__ ,reverse = True)
    print("Top "+str(top)+" de autores por su PageRank")
    print("Autor ,  Pagerank")
    for i in range(0,top):
      print(sorted_pr[i], " %2.5f"%(pr[sorted_pr[i]]))
    print("-----------------------------------------")
    
    
def most_important_coauthors(name, graph, top):
    print("Grafo:", name)
    print("Top "+str(top)+" de coautores.")
    print("autor --- autor --- peso")
    authors = []
    for a, b, data in sorted(graph.edges(data=True), key=lambda x: x[2]['weight'], reverse = True):
        #print('{a} {b} {w}'.format(a=a, b=b, w=data['weight']))
        authors.append('{a}---{b}---{w}'.format(a=a, b=b, w=data['weight']))
    for i in range(0,top):
        print(authors[i])
    
def top_betweenness(name, graph, top):
    print("Grafo:", name)
    print("Top "+str(top)+" de autores por betweenness centrality.")
    print("autor   betweenness")
    bw_centrality = nx.betweenness_centrality(graph, normalized=False)
    bw = []
    import operator
    sorted_x = sorted(bw_centrality.items(), key=operator.itemgetter(1), reverse=True)
    for a, b in sorted_x:
        bw.append('{key}    {value}'.format(key=a, value=b))
    for i in range(0,top):
        print(bw[i])

    
    
'''
    Homophilia
'''
def compute_degree_correlation(name, g):
    degrees = g.degree()
    # Make correlation matrix    
    max_degree = max([d for n, d in degrees])
    corr_matrix = np.zeros((max_degree+1,max_degree+1))    
    for node in g.nodes():            
        neighbors = g.neighbors(node)
        for neighbor in neighbors:
            corr_matrix[degrees[node]][degrees[neighbor]]+= 1            
    
    # Plot correlation matrix
    #f = plt.figure(figsize=(10, 10))
    #f = plt.figure()
    #plt.imshow(corr_matrix, fignum=f.number, origin='lower', cmap='Reds', interpolation='none')
    plt.imshow(corr_matrix[:15,:15], origin='lower', cmap='Reds', interpolation='none')
    print(corr_matrix[:15,:15])
    spl=1
    if(max_degree>25):
        spl=10
    ax = plt.xticks(range(0,15), range(0,15), fontsize=7)    
    plt.yticks(range(0,15), range(0,15), fontsize=7)
    plt.colorbar().ax.tick_params(labelsize=7, length=5, width=2)
    plt.title('Matriz de correlación de grado del grafo: '+ name, fontsize=10);
    plt.xlabel("K") 
    plt.ylabel("K") 
    plt.show()
    
    
'''
    Communities
'''

