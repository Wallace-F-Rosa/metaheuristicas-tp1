import argparse
import tsplib95 as tsplib
from evaluate import evaluate
import random

def nearest_neighbor(graph):
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Programa lê uma instância da tsplib '+
        'e gera solução inicial utilizando a heurística do vizinho mais '+
        'próximo. Versão 1: adiciona cidades somente no final da solução.'
    )
    parser.add_argument(
        '--file',
        '-f',
        type=str,
        required=True,
        help='Caminho até instância da tsplib.'
    )
    parser.add_argument(
        '-k',
        type=int,
        default=0,
        required=True,
        help='Número de entregas do Tspd.'
    )
    
    parser.add_argument(
        '-v',
        type=int,
        default=0,
        required=True,
        help='Valor de cada entrega do Tspd.'
    )

    parser.add_argument(
        '--solution',
        '-s',
        type=list,
        action='append',
        required=False,
        help='Solução para o problema(lista de vértices a serem visitados).'+
        ' Default: solução em ordem.'
    )
    
    args = parser.parse_args()
    solution = []
    if args.solution is not None:
        solution = args.solution

    problem = tsplib.load(args.file)
    g = problem.get_graph()
    sol = nearest_neighbor(g)
    print(sol)
    cost = evaluate(g, sol, args.k, args.v)
    print(cost)
