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

def neighborhood_swap(graph, sol, tabu={}):
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
            edge = (neighbor[j], neighbor[i+1])
            isNeighbor = sol[j] in graph[sol[i]] and sol[jf] in graph[sol[i+1]]
            isTabu = True if edge in tabu and tabu[edge] > 0 else False
            if isNeighbor and not isTabu:
                neighbor[i+1], neighbor[j] = neighbor[j], neighbor[i+1]
                neighbors.append(neighbor.copy())
                neighbor[i+1], neighbor[j] = neighbor[j], neighbor[i+1]
            
    return neighbors

def neighborhood_2opt(graph, sol, tabu={}):
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
            tabuOpt = False
            neighbor = sol.copy()
            jf = (j+1)%len(sol)
            isNeighbor = sol[j] in graph[sol[i]] and sol[jf] in graph[sol[i+1]]
            if isNeighbor:
                beg = i+1
                end = jf
                while beg < end:
                    neighbor[beg], neighbor[end] = neighbor[end], neighbor[beg]
                    edge = (neighbor[beg], neighbor[end])
                    isTabu = True if edge in tabu and tabu[edge] > 0 else False
                    if isTabu:
                        tabuOpt = True
                        break
                    beg +=1
                    end -=1
                if not tabuOpt:
                    neighbors.append(neighbor)
            
    return neighbors
