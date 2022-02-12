import argparse
import tsplib95 as tsplib
from evaluate import evaluate
from nearest_neighbor2 import nearest_neighbor
import random

def neighborhood_2opt(sol):
    neighbors = []
    return neighbors

def local_search(graph, s0):
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

    Return:
        list: Solução encontrada pela busca local; rota com as cidades que devem
        ser visitadas.
    """

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

    sol = local_search(g, sol, args.k, args.v)
