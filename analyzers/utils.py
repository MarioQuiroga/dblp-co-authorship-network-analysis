import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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
def compute_scc(g)
    scc = nx.strongly_connected_component_subgraphs(g)
    # Select max SCC 
    m_scc = []
    count = 0
    for x in scc:
        count = count + 1
        if len(x) > len(m_scc):
            m_scc = x
    print("Cantidad de componentes fuertemente conectados:", count)
    print("El componente gigante tiene", str(len(m_scc)), "nodos")
    return m_scc

# Distribución de grado
def compute_degree_distribution(graph):
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
            y.append(dist[i]/graph.number_of_nodes())
    # Exponente de la power law
    # Log scale
    log_x = np.log(x)
    log_y = np.log(y)

    # Compute model(curva ajustada) polyfit numpy
    # ajuste = np.polyfit(x log, y log, grado del polinomio = 1) retorna los coeficientes del polinomio [coef grado 1 alfa, coef grado 0 c]
    ajuste = np.polyfit(log_x, log_y, deg=1)
    rect = np.poly1d(ajuste) #internamente representa un polinomio 
    print("Recta de ajuste:", rect)
    print("Exponente de la power law: %2.3f" %(rect[1]))

    # Gráfico del ajuste
    y_pred = rect(log_x)
    plt.title("Gráfico comparación del modelo obtenido y datos reales") 
    plt.xlabel("log(k)") 
    plt.ylabel("log(Pk)") 
    plt.plot(log_x, log_y, log_x, y_pred) 
    plt.legend(('Curva real', 'Curva ajustada'),
    prop = {'size':10}, loc = 'upper right')
    plt.show()

    
# Distribucion coeficiente de clustering
def compute_coef_clustering_distribution(graph):
    clusterings = nx.clustering(graph)
    keys, values = zip(*clusterings.items())
    seq = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    hist, bins = np.histogram(values, bins=seq)
    plt.title("Distribución del coeficiente de clustering") 
    plt.xlabel("Coeficiente de clustering") 
    plt.ylabel("Cantidad") 
    plt.plot(bins[:-1], hist) 
    plt.show()    

    
'''
    Most important
'''
def most_important_authors(name, graph, top):
    # Degree centrality
    print("Grafo:", name)
    degrees = graph.degree()
    sorted_degrees = sorted(degrees, key=lambda degree: degree[1],reverse = True)
    print("Top "+str(top)+" de autores por su grado")
    print("Autor , Grado")
    top_ten = []
    for i in range(0,top):
      top_ten.append(sorted_degrees[i])
      print(sorted_degrees[i])    
        
    # PageRank centrality
    a = 0.3
    pr = nx.pagerank(graph, alpha=a)
    sorted_pr = sorted(pr, key=pr.__getitem__ ,reverse = True)
    print("Top "+str(top)+" de autores por su PageRank")
    print("Autor ,  Pagerank")
    for i in range(0,top):
      print(sorted_pr[i], " %2.5f"%(pr[sorted_pr[i]]))
    
    
def most_important_coauthors(name, graph, top):
    print("Grafo:", name)
    print("Top "+str(top)+" de coautores.")
    print("autor     autor    peso")
    authors = []
    for a, b, data in sorted(graph.edges(data=True), key=lambda x: x[2]['weight']):
        #print('{a} {b} {w}'.format(a=a, b=b, w=data['weight']))
        authors.append('{a} {b} {w}'.format(a=a, b=b, w=data['weight']))
    for i in range(0,top):
        print(authors[i])
    
def top_betweenness(name, graph, top):
    print("Grafo:", name)
    print("Top "+str(top)+" de autores por betweenness centrality.")
    print("autor   betweenness")
    bw_centrality = nx.betweenness_centrality(graph, normalized=False)
    bw = []
    for key, value in bw_centrality.items():
        bw.append('{key} {value}'.format(key=key, value=value))
    for i in range(0,top)
        print(bw[i])

    
    
'''
    Homophilia
'''
def compute_degree_correlation(name, g):
    degrees = g.degree()
    # Make correlation matrix
    max_degree = max([d for n, d in degrees])
    corr_matrix = np.zeros((max_degree,max_degree))
    for node in g.nodes():
        neighbors = g.neighbors(node)        
        for neighbor in neighbors:
            corr_matrix[degrees[node]][degrees[neighbor]] += 1
            
    # Plot correlation matrix
    f = plt.figure(figsize=(19, 15))
    plt.matshow(corr_matrix, fignum=f.number, origin='lower')
    plt.xticks(range(corr_matrix.shape[1]), range(max_degree), fontsize=14)
    plt.yticks(range(corr_matrix.shape[1]), range(max_degree), fontsize=14)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14)
    plt.title('Matriz de correlación de grado del grafo: '+ name, fontsize=16);
    plt.gca().xaxis.tick_bottom()
    plt.show()
    
    
'''
    Communities
'''

