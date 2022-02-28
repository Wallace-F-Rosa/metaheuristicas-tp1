import tsplib95 as tsplib
from evaluate import evaluate
import random

def valid_route(graph, route):
    """
    Função que valida se uma rota é valida no grafo.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.
        route (list): lista de nós a serem percorridos na rota

    Return:
        bool: True se a rota é valida e False se contrário.
    """
    for i in range(len(route)-1):
        if route[i+1] not in graph[route[i]]:
            return False
    return True

def neighborhood_2opt(graph, sol):
    """
    Função que calcula vizinhança 2-opt.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.
        sol (list): Solução inicial, rota (lista de nós
        a serem visitados) inicial.

    Return:
        list: lista de vizinhos da solução fornecida.
    """
    neighbors = []
    neighbor = sol.copy()
    for i in range(0, len(sol)-3):
        for j in range(i+2, len(sol)-(i==0)):
            jf = (j+1)%len(sol)
            if sol[j] in graph[sol[i]] and sol[jf] in graph[sol[i+1]]:
                neighbor[i+1], neighbor[j] = neighbor[j], neighbor[i+1]
                neighbors.append(neighbor.copy())
                neighbor[i+1], neighbor[j] = neighbor[j], neighbor[i+1]
            
    return neighbors

def nearest_neighbor2(graph):
    """
    Função que calcula solução (rota) inicial do TSPd usando heurística do
    vizinho mais próximo. Esta versão adiciona cidades no inicio e final da rota.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.

    Return:
        list: rota com as cidades que devem ser visitadas
    """
    s = []
    g = graph
    nodes = list(g.nodes)
    s.append(nodes[0])
    visited = {
        nodes[0]: True
    }
    while len(visited) != len(nodes):
        beg = s[0]
        i = s[len(s)-1]
        j = None
        k = None

        # seleciona primeiro visinho
        for neighbor in g[i]:
            if neighbor not in visited:
                j = neighbor
                break

        for neighbor in g[beg]:
            if neighbor not in visited:
                k = neighbor
                break

        # encontra o vizinho mais próximo
        for neighbor in g[i]:
            if neighbor not in visited:
                if g[i][neighbor]['weight'] < g[i][j]['weight']:
                    j = neighbor

        for neighbor in g[beg]:
            if neighbor not in visited:
                if g[neighbor][beg]['weight'] < g[k][beg]['weight']:
                    k = neighbor
            
        if g[i][j]['weight'] < g[k][beg]['weight']:
            visited[j] = True
            # adiciona o vizinho mais próximo na solução
            s.append(j)
        elif g[k][beg]['weight'] < g[i][j]['weight']:
            visited[k] = True
            s.insert(0,k)
        else:
            r = random.choice([j,k])
            if r == j:
                s.append(r)
            else:
                s.insert(0,r)
            visited[r] = True

    return s

def nearest_neighbor1(graph):
    """
    Função que calcula solução (rota) inicial do TSPd usando heurística do
    vizinho mais próximo. Esta versão só adiciona cidades considerando 
    o final da rota.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.

    Return:
        list: rota com as cidades que devem ser visitadas
    """
    s = []
    g = graph
    nodes = list(g.nodes)
    s.append(nodes[0])
    visited = {
        nodes[0]: True
    }
    while len(visited) != len(nodes):
        i = s[len(s)-1]
        j = None

        # seleciona primeiro visinho
        for neighbor in g[i]:
            if neighbor not in visited:
                j = neighbor
                break

        # encontra o vizinho mais próximo
        for neighbor in g[i]:
            if neighbor not in visited:
                if g[i][neighbor]['weight'] < g[i][j]['weight']:
                    j = neighbor
        
        visited[j] = True
        # adiciona o vizinho mais próximo na solução
        s.append(j)
    return s
