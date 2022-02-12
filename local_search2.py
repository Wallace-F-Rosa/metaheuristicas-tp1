import argparse
import tsplib95 as tsplib
from evaluate import evaluate
from nearest_neighbor2 import nearest_neighbor
import random

def best_improvement(graph, sol, candidates, k, v):
    best = sol
    best_cost = evaluate(graph, best, k, v)
    for c in candidates:
        cost = evaluate(graph, c, k, v)
        if cost < best_cost:
            best = c
            best_cost = cost
        elif cost == best_cost:
            best = random.choice([best,c])
            if best == c:
                best_cost = cost

    return best, best_cost

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
        if route[i+1] not in graph[i]:
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
    for i in range(0, len(sol)-3):
        neighbor = sol.copy()
        for j in range(i+2, len(sol)-1):
            neighbor[i+1], neighbor[j] = neighbor[j], neighbor[i+1]

        if valid_route(graph, neighbor):
            neighbors.append(neighbor)
    
    # print(neighbors)
            
    return neighbors

def local_search(graph, s0, k, v, iter_max, iter_no_impro_max):
    """
    Função que calcula solução (rota) utilizando busca local com vizinhança
    2-opt.

    Args:
        graph (NetworkX.Graph): Grafo do problema. Estrutura suportada pela 
    NetworkX lib.
        s0 (list): Solução inicial para busca local, rota (lista de nós
        a serem visitados) inicial.
        k (int): Número de entregas no TSPd
        v (int): Valor das entregas no TSPd.
        iter_max (int): Valor máximo de iterações da busca local.
        iter_no_improve_max (int): Valor máximo de iterações sem melhora da
        busca local.

    Return:
        list, float: Solução encontrada pela busca local(rota com as cidades que devem
        ser visitadas) e custo da solução.
    """
    it = 0
    it_no_improve = 0
    s = s0.copy()
    s_cost = evaluate(graph, s, k, v)
    while it < iter_max and it_no_improve < iter_no_improve_max:
        candidates = neighborhood_2opt(graph, s)
        s1, s1_cost = best_improvement(graph, s, candidates, k, v)
        
        if s1_cost != s_cost:
            improv_rate = abs(s1_cost/s_cost - 1)
            s = s1
            s_cost = s1_cost
            if improv_rate < 0.01:
                it_no_improve += 1
        else:
            it_no_improve +=1
            
            if s1 == s:
            # nenhum vizinho é melhor
                break
    return s, s_cost

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

    iter_max = 10**6
    iter_no_improve_max = 100
    sol, cost = local_search(g, sol, args.k, args.v, iter_max, iter_no_improve_max)
    print(sol)
    print(cost)
