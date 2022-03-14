import random
"""
    Functions related to the solution of the TSDp problem, e.g. finding
    a initial solution, adding noise to an existing solution, etc.
"""
def nearest_neighbor2(graph, start_node = 0):
    """
    Função que calcula solução (rota) inicial do TSPd usando heurística do
    vizinho mais próximo. Esta versão adiciona cidades no inicio e final da rota.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.
        start_node (int): Vértice de inicio, valor default é o vértice 0.

    Return:
        list: rota com as cidades que devem ser visitadas
    """
    s = []
    g = graph
    nodes = list(g.nodes)
    s.append(nodes[start_node])
    visited = {
        nodes[0]: True }
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

def nearest_neighbor1(graph, start_node = 0):
    """
    Função que calcula solução (rota) inicial do TSPd usando heurística do
    vizinho mais próximo. Esta versão só adiciona cidades considerando 
    o final da rota.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.
        start_node (int): Vértice de inicio, valor default é o vértice 0.

    Return:
        list: rota com as cidades que devem ser visitadas
    """
    s = []
    g = graph
    nodes = list(g.nodes)
    s.append(nodes[start_node])
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

