import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

'''
    Structural properties
'''
# Load network 
def load_networks(files_list):
    return None

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

    
    
'''
    Most important
'''


'''
    Homophilia
'''


'''
    Communities
'''

