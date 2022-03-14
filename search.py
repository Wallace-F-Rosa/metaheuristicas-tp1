import tsplib95 as tsplib
from evaluate import evaluate
import random
from neighborhoods import neighborhood_2opt

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

    sol_cost = evaluate(graph, sol, k, v)
    if sol_cost < best_cost:
        return None, 0

    return best, best_cost

def local_search(graph, s0, k, v, iter_max, iter_no_improve_max, tabu=[]):
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
        candidates = neighborhood_2opt(graph, s, tabu=tabu)
        s1, s1_cost = best_improvement(graph, s, candidates, k, v)

        if s1 == None:
            break

        improv_rate = abs(s1_cost/s_cost - 1)
        s = s1
        s_cost = s1_cost
        if improv_rate < 0.01:
            it_no_improve += 1
        it += 1
    return s, s_cost
